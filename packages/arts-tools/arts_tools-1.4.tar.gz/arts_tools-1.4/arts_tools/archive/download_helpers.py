#!/usr/bin/env python3

import os
import urllib
import ssl

import numpy as np

try:
    from irods.session import iRODSSession
    from irods.exception import DataObjectDoesNotExist
    from irods.keywords import FORCE_FLAG_KW
    have_irods = True
except ImportError:
    have_irods = False


# to keep track of printing download progress
last_percent_printed = None


def format_bytes(nbytes):
    """
    Format a number in bytes with a prefix

    :param int nbytes: number of bytes (>0)
    :return: number of MB/GB etc (float), unit (MB/GB etc) (str)
    """
    # prefixes up to exabyte
    prefix_letters = ' kMGTPE'

    if nbytes < 1:
        # special case, because log10(nbytes) < 0 for nbytes < 1
        prefix_tier = 0
    else:
        prefix_tier = int(np.log10(nbytes) / 3)  # 3 = log10(1000)

    try:
        letter = prefix_letters[prefix_tier]
        scaling = 1000 ** prefix_tier
    except IndexError:
        # unlikely to run into files over 1000 exabytes, but we wouldn't want an unexplained
        # IndexError when someone puts in a very large number
        letter = prefix_letters[-1]
        scaling = 1000 ** (len(prefix_letters) - 1)
    # do the scaling
    return nbytes / scaling, letter + 'B'


def print_progress(nblock, nbyte_per_block, nbyte_total, step=5):
    """
    Print download progress of urllib.request.urlretrieve command

    :param nblock:
    :param nbyte_per_block:
    :param total_bytes:
    :param int step: progress is only printed if the percentage is a multiple of step
    """
    global last_percent_printed
    nbyte_done = nblock * nbyte_per_block
    percent_done = int(100 * nbyte_done / nbyte_total)

    # print only if not done already and multiple of step
    if last_percent_printed != percent_done and int(percent_done % step) == 0:
        # get scaled value prefix to use for output (kB, MB etc)
        done_scaled, done_unit = format_bytes(nbyte_done)
        total_scaled, total_unit = format_bytes(nbyte_total)

        print(f"{done_scaled:.0f} {done_unit} / {total_scaled:.0f} {total_unit} ({percent_done:.0f}%)")
        last_percent_printed = percent_done
    return


def download_url(url, output_folder=None, overwrite=False, verbose=False):
    """
    Download file from given url

    :param url: URL to download file from
    :param str output_folder: Output folder (Default: current directory)
    :param bool overwrite: Overwrite output file if it already exists
    :param bool verbose: Print download progress
    """
    # create output folder and get full path to output file
    if output_folder is None:
        output_folder = os.getcwd()
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, os.path.basename(url))

    # check if the file already exists
    if os.path.isfile(output_file) and not overwrite:
        print(f"File already exists: {output_file}")
        return

    # set report hook if verbose output
    if verbose:
        hook = print_progress
    else:
        hook = None

    # download the file
    try:
        urllib.request.urlretrieve(url, filename=output_file, reporthook=hook)
    except urllib.error.HTTPError as e:
        # add filename to error message
        e.msg = f"URL not found: {url}"
        raise
    return


def download_irods(path, output_folder=None, overwrite=False):
    """
    Download file from ALTA using iRODS

    :param path: Path to file on iRODS server
    :param str output_folder: Output folder (Default: current directory)
    :param bool overwrite: Overwrite output file if it already exists
    """
    # check if iRODS tools are available
    if not have_irods:
        print("iRODS tools not available; reinstall arts_tools "
              "with pip install --upgrade arts_tools[irods]")
        return

    # get the irods environment file
    try:
        env_file = os.environ['IRODS_ENVIRONMENT_FILE']
    except KeyError:
        env_file = os.path.expanduser('~/.irods/irods_environment.json')
    if not os.path.isfile(env_file):
        print("iRODS environment file not found. Set IRODS_ENVIRONMENT_FILE if the file is not in the default "
              "location. Also make sure your iRODS environment is set up properly (with iinit)")
        return

    # create output folder and get full path to output file
    if output_folder is None:
        output_folder = os.getcwd()
    os.makedirs(output_folder, exist_ok=True)
    output_file = os.path.join(output_folder, os.path.basename(path))

    # check if the file already exists
    if os.path.isfile(output_file) and not overwrite:
        print(f"File already exists: {output_file}")
        return
    if overwrite:
        download_options = {FORCE_FLAG_KW: ''}
    else:
        download_options = {}

    # create SSL context
    ssl_context = ssl.create_default_context(purpose=ssl.Purpose.SERVER_AUTH, cafile=None, capath=None, cadata=None)
    # open an iRODS session
    with iRODSSession(irods_env_file=env_file, ssl_context=ssl_context) as session:
        try:
            session.data_objects.get(path, output_folder, **download_options)
        except DataObjectDoesNotExist:
            # add filename to error message
            raise DataObjectDoesNotExist(f"File not found: {path}")
