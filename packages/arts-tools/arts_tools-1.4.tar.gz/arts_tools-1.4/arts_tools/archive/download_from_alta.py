#!/usr/bin/env python3

import os
import sys
import argparse

from arts_tools.archive.download_helpers import download_url, download_irods
from arts_tools.constants import NTAB


def get_file_paths(release, taskid, cbs, tabs):
    """
    Construct path to files in ALTA

    :param str release: Data release (SVC or internal)
    :param str taskid: Observation taskid
    :param iterator cbs: compound beams to download
    :param iterator tabs: tied-array beams to download of each compound beam
    :return: list of file paths
    """
    # set prefix
    if release == "internal":
        prefix = "/altaZone/archive/arts_main/arts_sc4"
    elif release == "SVC":
        prefix = "https://alta.astron.nl/webdav/SVC_2019_TimeDomain"
    else:
        raise ValueError(f"Unknown release: {release}; valid options are SVC, internal")

    # construct full path for each CB and TAB
    files = [f"{prefix}/{taskid}/CB{cb:02d}/ARTS{taskid}_CB{cb:02d}_TAB{tab:02d}.fits" for cb in cbs for tab in tabs]
    return files


def main():
    data_releases = ["SVC", "internal"]

    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description="Download files of an observation from ALTA.\n"
                                                 "E.g. to download all files of task ID 20200101,\n"
                                                 "compound beam 0 and 17 to a folder 'fits':\n"
                                                 "arts_download_from_alta --taskid 20200101 --cbs 0 17 "
                                                 "--output_folder fits")
    parser.add_argument("--release", default="SVC", choices=data_releases,
                        help="Data release (Default: %(default)s).\n"
                             "Set to 'internal' to download non-released files (requires iRODS access to ALTA)")
    parser.add_argument("--taskid", required=True,
                        help="Task ID of observation (yymmddnnn)")
    parser.add_argument("--cbs", type=int, required=True, nargs="+",
                        help="Space-separated list of CBs to download")
    parser.add_argument("--tabs", type=int, nargs="+",
                        help="Space-separated list of TABs to download (Default: all)")
    parser.add_argument("--output_folder", default=os.getcwd(),
                        help="Folder to download files to (Default: current directory)")
    parser.add_argument("--verbose", action="store_true",
                        help="Verbose output")

    args = parser.parse_args()

    # task ID must have 9 characters (yymmddnnn)
    nchar = 9
    if len(args.taskid) != nchar:
        print(f"Task ID must have {nchar} characeters")
        sys.exit(1)

    # remove any duplicates from CB list
    if args.cbs is not None:
        args.cbs = set(args.cbs)

    if args.tabs is None:
        # download all TABs if unspecified
        args.tabs = range(NTAB)
    else:
        # remove any duplicates from TAB list
        args.tabs = set(args.tabs)

    # get list of files to download
    files = get_file_paths(args.release, args.taskid, args.cbs, args.tabs)

    # create the output folder
    os.makedirs(args.output_folder, exist_ok=True)

    # download the files
    for f in files:
        print(f"Will download {os.path.basename(f)}")
        # SVC data can be downloaded over http
        if args.release == "internal":
            download_irods(f, args.output_folder)
        elif args.release == "SVC":
            download_url(f, args.output_folder, verbose=args.verbose)
        else:
            raise ValueError(f"Unknown release: {args.release}; valid options are SVC, internal")
