#!/usr/bin/env python

"""Make a VCF file from the MacArthurs lab nice clinvar txt file"""
import argparse
import logging

import sys
from vcf_parser import VCFParser

__author__ = 'dankle'


def main():
    opts = parse_cli()
    setup_logging(opts.loglevel)

    logging.debug("Using clinvar {}".format(opts.clinvar))
    logging.debug("Writing to vcf {}".format(opts.V))

    logging.debug("Opening files")
    my_vcf = VCFParser(fileformat='VCFv4.2')

    logging.info("Done.")

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

