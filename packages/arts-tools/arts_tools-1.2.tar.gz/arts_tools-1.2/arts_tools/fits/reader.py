#!/usr/bin/env python

import sys
from codecs import decode

from astropy.io import fits


def read_header(fname, hdu=None):
    """
    Read fits header

    :param str fname: Path to fits file
    :param int/str hdu: HDU to read header from (default: all)
    :return: header (astropy.io.fits.header.Header) or
        list of headers if hdu is not specified
    """
    with fits.open(fname) as f:
        if hdu is None:
            header = [h.header for h in f]
        else:
            header = f[hdu].header

    return header


def read_parameterset(fname):
    """
    Read observation parameterset from fits file

    :param str fname: Path to fits file
    :return: parameterset (dict)
    """

    # read parset key from header
    header = read_header(fname, hdu='PRIMARY')
    raw_parset = header['PARSET']
    # parset is encoded as bz2, then hex
    # also convert to string
    parset = decode(decode(raw_parset, 'hex'), 'bz2').decode()
    # key/value pairs my be separated by ' = ' or '='
    parset.replace(' = ', '=')
    # convert to dict
    parset_dict = {}
    for line in parset.split('\n'):
        # ignore empty lines
        if not line:
            continue
        # parse key/value paris
        try:
            key, value = line.split('=')
        except Exception as e:
            print("Failed to read key/value pair from '{}', ignoring line".format(line))
            pass
        else:
            parset_dict[key] = value
    return parset_dict
