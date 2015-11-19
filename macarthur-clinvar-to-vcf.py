#!/usr/bin/env python

"""Make a VCF file from the MacArthurs lab nice clinvar txt file"""
import argparse
import logging

import sys

from vcf_parser import VCFParser
from vcf_parser.utils import build_info_string

__author__ = 'dankle'
__VERSION = '0.0.2'


def main():
    opts = parse_cli()
    setup_logging(opts.loglevel)

    logging.debug("Using clinvar {}".format(opts.clinvar))
    logging.debug("Writing to vcf {}".format(opts.V))

    logging.debug("Opening files")
    my_vcf = VCFParser(fileformat='VCFv4.2')
    output = open(opts.V, 'w')

    clinvar_flat = open(opts.clinvar, 'r')
    number_of_variants_written = 0

    logging.debug("Setting up INFO in header")
    my_vcf.metadata.add_info(info_id='MEASURESET', number='1', entry_type='String', description="Measure set")
    my_vcf.metadata.add_info(info_id='HGNC', number='1', entry_type='String', description="HGNC Symbol")
    my_vcf.metadata.add_info(info_id='CLNSIGSTR', number='.', entry_type='String', description="Clinical Significance")
    my_vcf.metadata.add_info(info_id='REVSTAT', number='1', entry_type='String', description="Review Status")
    my_vcf.metadata.add_info(info_id='HGVSC', number='.', entry_type='String', description="HGVS-c")
    my_vcf.metadata.add_info(info_id='HGVSP', number='.', entry_type='String', description="HGVS-p")
    my_vcf.metadata.add_info(info_id='ALLSUBM', number='.', entry_type='String', description="All submitters")
    my_vcf.metadata.add_info(info_id='ALLTRAITS', number='.', entry_type='String', description="All traits associated with this variant")
    my_vcf.metadata.add_info(info_id='ALLPMID', number='.', entry_type='String', description="All pubmed IDs")
    my_vcf.metadata.add_info(info_id='PATHOGENIC', number='0', entry_type='Flag', description="Set if the variant has ever been asserted Pathogenic or Likely pathogenic by any submitter for any phenotype, and unset otherwise")
    my_vcf.metadata.add_info(info_id='CONFLICTED', number='0', entry_type='Flag', description="Set if the variant has ever been asserted Pathogenic or Likely pathogenic by any submitter for any phenotype, and has also been asserted Benign or Likely benign by any submitter for any phenotype, and unser otherwise. Note that having one assertion of pathogenic and one of uncertain significance does not count as conflicted for this column.")

    for header_line in my_vcf.metadata.print_header():
        logging.debug("Writing header line {}".format(header_line))
        output.write(header_line+"\n")

    header_elements = ["CHROM", "POS", "ID", "REF", "ALT", "QUAL", "FILTER", "INFO"]

    logging.debug("Parsing clinvar tsv")
    for line in clinvar_flat:
        if line.startswith("chrom") or line.strip() == "":
            continue

        elements = line.strip().split("\t")
        chrom=elements[0]
        pos=elements[1]
        ref=elements[2]
        alt=elements[3]
        mut=elements[4]
        measure_set = elements[5].replace(" ", "_").split(";")
        symbol = elements[6].replace(" ", "_").split(";")
        clnsigstr = elements[7].replace(" ", "_").split(";")
        review_status = elements[8].replace(" ", "_").split(";")
        hgvs_c = elements[9].replace(" ", "_").split(";")
        hgvs_p = elements[10].replace(" ", "_").split(";")
        all_submitters = elements[11].replace(" ", "_").split(";")
        all_traits = elements[12].replace(" ", "_").split(";")
        all_pubmed_ids = elements[13].replace(" ", "_").split(";")
        pathogenic = elements[14]
        conflicted = elements[15]

        info_dict = dict(MEASURESET=measure_set,
                         HGNC=symbol,
                         CLNSIGSTR=clnsigstr,
                         REVSTAT=review_status,
                         HGVSC=hgvs_c,
                         HGVSP=hgvs_p,
                         ALLSUBM=all_submitters,
                         ALLTRAITS=all_traits,
                         ALLPMID=all_pubmed_ids)

        # special treatment for flags
        if pathogenic == "1":
            info_dict['PATHOGENIC'] = 0

        if conflicted == "1":
            info_dict['CONFLICTED'] = 0

        info_string = build_info_string(info_dict)

        variant = dict(CHROM=chrom,
                       POS=pos,
                       ID='.',
                       REF=ref,
                       ALT=alt,
                       QUAL='.',
                       FILTER='.',
                       INFO=info_string
                       )

        variant_string = "\t".join([variant[key] for key in header_elements])
        logging.debug("Writing variant {}:{} {}/{}".format(chrom, pos, ref, alt))
        output.write(variant_string + "\n")
        number_of_variants_written += 1

    logging.info("Written {} variants to {}.".format(number_of_variants_written, opts.V))


def parse_cli():
    """
    Parse command line argument
    :return: a Namespace object from argparse.parse_args()
    """
    ap = argparse.ArgumentParser()
    ap.add_argument('--clinvar', help="ClinVar flat file from https://github.com/macarthur-lab/clinvar", action="store", required=True)
    ap.add_argument('-V', help="input VCF file", action="store", required=True)
    ap.add_argument("--loglevel", help="level of logging", default='INFO', type=str,
                    choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'])

    return ap.parse_args()


def setup_logging(loglevel="INFO"):
    """
    Set up logging
    :param loglevel:
    :return:
    """
    numeric_level = getattr(logging, loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(level=numeric_level,
                        format='%(levelname)s %(asctime)s %(funcName)s - %(message)s')
    logging.info("Started log with loglevel %(loglevel)s" % {"loglevel": loglevel})

if __name__ == "__main__":
    sys.exit(main())

