#!/usr/bin/env python3
#
# WSRT constants

import numpy as np
import astropy.units as u
from astropy.coordinates import EarthLocation

#: File with definition of CB offsets
CB_OFFSETS = 'square_39p1.cb_offsets'
#: CB half-power width
CB_HPBW = 28.0835088 * u.arcmin  # calculated from CB offsets file
#: Reference frequency for CB half-power width
REF_FREQ = 1770 * u.MHz  # for then it matches the measured width at 1420
#: Bandwidth
BANDWIDTH = 300 * u.MHz
#: Number of compound beams
NCB = 40

# WSRT position in ITRF coordinates
ARRAY_ITRF = np.array([3828630.63486200943589211, 443593.39226634375518188, 5064922.99755000043660402]) * u.meter
#: WSRT position
WSRT_LOC = EarthLocation.from_geocentric(*ARRAY_ITRF)
