"""Waylay SDK command line interface"""
import argparse
import logging

logging.basicConfig()
parser = argparse.ArgumentParser(
    prog='waylay', description='Command line interface to the Waylay Python SDK'
)
args = parser.parse_args()
parser.print_help()
