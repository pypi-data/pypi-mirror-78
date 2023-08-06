#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
This is the wrapper that provides/is the py2cfg shell script.
"""
# Taylor 2019

import os
import sys
import argparse

# Relative and absolute version of the same thing for interpreter tolerance
sys.path.append("..")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# can be either pip or local relative dir
from py2cfg import CFGBuilder


def main():
    parser = argparse.ArgumentParser(
        description="Generate the control flow graph of a Python program"
    )
    parser.add_argument(
        "input_file",
        help="Path to a file containing a Python program for which the CFG must be generated",
    )

    args = parser.parse_args()
    cfg_name = args.input_file.split("/")[-1]
    cfg = CFGBuilder().build_from_file(cfg_name, args.input_file)

    # Some options for wrapping:
    # cfg.build_visual(cfg_name[:-3] + '_cfg', format='pdf', calls=True)
    cfg.build_visual(cfg_name[:-3] + "_cfg", format="png", calls=True, show=False)
    # cfg.build_visual('controlflowgraph', format='png', calls=True, show=False)

    # removes the CFG file, which maybe we could just turn off?
    os.remove(cfg_name[:-3] + "_cfg")


if __name__ == "__main__":
    main()
