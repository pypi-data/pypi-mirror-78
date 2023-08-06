import argparse
import logging
import sys

from siv.scripts.parsehlk import scan_folder

def get_parser():
    parser = argparse.ArgumentParser(description='biostool')
    parser.add_argument("--folder", default=r"//WIN-6HNS1UBI6D7.hf.intel.com/HLKLogs/6-25-2020")
    return parser

def main():
    logging.basicConfig(format="%(asctime)s %(levelname)s: %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p",
        level=logging.INFO,
        stream=sys.stdout)
    logger = logging.getLogger()

    parser = get_parser()
    args = parser.parse_args()

    scan_folder(args.folder)
