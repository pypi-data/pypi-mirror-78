#!/usr/bin/env python3

import sys

import argparse
import warnings

import numpy as np
import astropy.units as u
from astropy.coordinates import SkyCoord
from psrqpy import QueryATNF

from arts_tools import tools
from arts_tools.constants import CB_HPBW, REF_FREQ, NCB


def get_half_power_width(freq):
    """
    Calculate compound beam half-power width, assuming linear scaling with frequency

    :param Quantity freq: Frequency
    :return: half-power width (Quantity)
    """
    scaling = freq / REF_FREQ
    hpbw = CB_HPBW * scaling
    return hpbw.to(u.arcmin)


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                     description="For a given pointing, determine which pulsars are in the field and "
                                                 "in which compound beam they are.")

    parser.add_argument('--ra', required=True, help="Right Ascension of pointing in hh:mm:ss.s format")
    parser.add_argument('--dec', required=True, help="Declination of pointing in dd:mm:ss.s format")
    parser.add_argument('--freq', type=float, default=1370,
                        help="Observing frequency (MHz), used to determine size of compound beams. "
                             "Ignored if max_dist is used."
                             "(Default: %(default)s)")
    parser.add_argument('--max_dist', type=float, help="Maximum distance from CB center (arcmin) to be considered "
                                                       "in the CB. (Default: twice half-power width)")
    parser.add_argument('--more_info', action='store_true', help='Add pulsar parameters to output')

    # print help if no arguments are given
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    args = parser.parse_args()

    # pulsar parameters to query
    params = ['NAME', 'RAJ', 'DECJ', 'DM', 'P0', 'S1400']

    # set max dist if not given
    if args.max_dist is None:
        args.max_dist = 2 * get_half_power_width(args.freq * u.MHz).to(u.arcmin).value

    # query ATNF for pulsars in a 4x4 degree FoV, which covers more than the entire Apertif FoV
    bound = [args.ra, args.dec, 4]
    # for some reason the query gives a RuntimeWarning, suppress it
    print("Querying ATNF")
    with warnings.catch_warnings():
        warnings.simplefilter('ignore', category=RuntimeWarning)
        results = QueryATNF(params=params, circular_boundary=bound)

    if len(results) == 0:
        print("No pulsars found")
        sys.exit()

    # find the pointing of each CB
    pointing = SkyCoord(args.ra, args.dec, unit=(u.hourangle, u.deg))
    cb_pointings = []
    for cb in range(NCB):
        cb_ra, cb_dec = tools.cb_index_to_pointing(cb, pointing.ra, pointing.dec)
        cb_pointings.append(SkyCoord(cb_ra, cb_dec))

    # check the closest CB for each pulsar
    output = []
    pulsar_found = False
    print("Locating pulsars in Apertif Compound Beams")
    for psr in results.table:
        psr_coord = SkyCoord(psr['RAJ'], psr['DECJ'], unit=(u.hourangle, u.deg))
        # get separation from each CB and find minimum
        separations = [psr_coord.separation(beam).to(u.arcmin).value for beam in cb_pointings]
        # index of lowest separation is best CB
        best_cb = np.argmin(separations)
        # check the separation itself
        sep = separations[best_cb]
        # if too far away, skip this pulsar
        # sep must be in acrmin here
        if sep > args.max_dist:
            continue
        # a good pulsar was found
        pulsar_found = True
        # store info
        output.append([best_cb, sep, psr])

    if not pulsar_found:
        print("No pulsars found")
        sys.exit()

    # print info sorted by CB
    output = np.array(output)
    order = np.argsort(output[:, 0])

    print("Pulsars found:")
    for cb, sep, psr in output[order]:
        print(f"PSR {psr['NAME']} in CB{cb:02d}, separation from CB centre: {sep:.2f}\'")
        if args.more_info:
            for p in params:
                # get value and unit
                value = psr[p]
                unit = psr.columns[p].unit
                dtype = psr.columns[p].dtype
                # format according to dtype
                if dtype == np.float:
                    formatted_value = f' {p} = {value:.2f}'
                else:
                    formatted_value = f' {p} = {value}'
                # add unit
                if unit is not None:
                    formatted_value += f' {unit}'
                # add newline
                print(formatted_value)
            print()
