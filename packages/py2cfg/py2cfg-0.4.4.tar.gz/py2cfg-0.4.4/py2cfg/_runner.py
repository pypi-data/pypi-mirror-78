#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
This is the wrapper that provides/is the py2cfg shell script.
"""

import os
import sys
import argparse

# Relative and absolute version of the same thing for interpreter tolerance
sys.path.append("..")
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# can be either pip or local relative dir
from py2cfg.builder import CFGBuilder


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate the control flow graph of a Python program"
    )
    parser.add_argument(
        "input_file",
        help="Path to a file containing a Python program for which the CFG must be generated",
    )
    parser.add_argument(
        "--short",
        nargs=1,
        type=bool,
        default=True,
        help="Shorten all strings above 20 characters",
    )
    parser.add_argument(
        "--format",
        nargs=1,
        type=str,
        default="svg",
        help="File format of the generated cfg",
    )
    parser.add_argument(
        "--calls", nargs=1, type=bool, default=True, help="Toggle call graph",
    )
    parser.add_argument(
        "--show", nargs=1, type=bool, default=False, help="Open CFG after generation"
    )

    args = parser.parse_args()
    cfg_name = args.input_file.split("/")[-1]
    cfg = CFGBuilder(args.short).build_from_file(cfg_name, args.input_file)

    # Some options for wrapping:
    # cfg.build_visual(cfg_name[:-3] + '_cfg', format='pdf', calls=True)
    # cfg.build_visual(cfg_name[:-3] + "_cfg", format="svg", calls=True, show=False)
    # cfg.build_visual(cfg_name[:-3] + "_cfg", format="png", calls=True, show=False)
    # cfg.build_visual('controlflowgraph', format='png', calls=True, show=False)
    cfg.build_visual(
        cfg_name[:-3] + "_cfg", format=args.format, calls=args.calls, show=args.show,
    )
    # removes the CFG file, which maybe we could just turn off?
    os.remove(cfg_name[:-3] + "_cfg")
