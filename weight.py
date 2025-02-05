#!/bin/python3
#
# Boardwalk Weight Per Foot and Berring Width Calculator
#
# File:         weight.py
# Authors:      Bob Walton (walton@acm.org)
# Date:         Wed Feb  5 08:11:59 AM EST 2025
#
# The authors have placed this program in the public
# domain; they make no warranty and accept no liability
# for this program.

import sys
import math
import re

document = """
Program to compute allowed weight per linear foot and
required bearing width of stringers with various
spans and cross-sections.

Command: python3 weithg.py

""";

if len ( sys.argv ) > 1:
    print ( document )
    exit ( 1 )

standard_method = """
FOR EQUATIONS SEE NATIONAL DESIGN STANDARD
--- --------- --- -------- ------ --------
``SPAN OF FLOOR JOIST'' EXAMPLE
------ -- ----- ------- -------
"""
print ( standard_method )

# Data

# Dimensions
#
widths = { "2x4":  1.5, "4x4":  3.5,
           "2x6":  1.5, "4x6":  3.5,
           "2x8":  1.5, "4x8":  3.5,
           "2x10": 1.5, "4x10": 3.5,
           "2x12": 1.5, "4x10": 3.5 }
heights = { "2x4":  3.5,   "4x4":  3.5,
            "2x6":  5.5,   "4x6":  5.5,
            "2x8":  7.25,  "4x8":  7.25,
            "2x10": 9.25,  "4x10": 9.25,
            "2x12": 11.25, "4x10": 11.25 }
dimensions = [ "4x4", "2x6", "4x6", "2x8",
               "2x10", "2x12" ]
spans = [ [ 6, 8, 10, 12, 14, 16 ],  # page 2
          [ 18, 20, 22, 24 ] ]       # page 3


# Design Reference Values
#
WOOD = "No 1 Standard Southern Pine"
CM_Fb = 0.85  # for Fb > 1,150 psi
CM_Fv = 0.97
CM_E = 0.9
CM_Fcperp = 0.67
CD = 1.6 # for 10 minute loads
Fb = { "2x4": CM_Fb * 1500, "4x4": CM_Fb * 1500,
       "2x6": CM_Fb * 1350, "4x6": CM_Fb * 1350,
       "2x8": CM_Fb * 1250, "4x8": CM_Fb * 1250,
       "2x10": 1050, "4x10": 1050,
       "2x12": 1000, "4x10": 1000 }
       # CM_Fb included
Fv = 175
E = 1600000
Fc_perp = 565
limit = 360  # deflection limit = span / limit
bearing = 1.5 # inches design bearing

reference = """
Southern Yellow Pine Reference Design Values:

wood = {}
load duration factor (CD) = {} for 10 minute loads
    Possible Values:    1.6  for ten minutes
                        1.25 for seven days
                        0.9  for dead load
deflection limit = span/{}
design bearing length = {} inches

"""
print ( reference.format ( WOOD, CD, limit, bearing ) )



# Main Program

# Standard Method

print ( """
TO GET ALLOWED WEIGHT PER SQUARE FOOT,
TAKE ALLOWED WEIGHT FOR ONE STRINGER PER FOOT,
MULITPLY BY THE NUMBER OF STRINGERS,
AND DIVIDE BY THE LENGTH OF THE TREAD IN FEET.
""" )
print ( "(1) ALLOWED WEIGHT IN LBF/FT BY MOMENT"
           " CAPACITY" )
print ( "(2) ALLOWED WEIGHT IN LBF/FT BY SHEAR" )
print ( "(3) ALLOWED WEIGHT IN LBF/FT BY DEFLECTION" )
print ( "(4) ALLOWED WEIGHT IN LBF/FT FOR 1.5 INCH"
           " BEARING" )
print ( "(5) MINIMUM OF ABOVE ALLOWED WEIGHTS"
           " IN LBF/FT" )
print ()
print ( """
Allowable weights (1) and (2) are proportional to CD.
Allowable weight (3) is proportional to
                     deflection limit.
Allowable weight (4) is proportional to
                     design bearing length.
""" )
separator = "-----------+----------------------------" \
            "--------------------"
min_W = {}
for slist in spans:
    print ( "\f" )
    print ( ' SPAN FT   |', end='' )
    for d in dimensions:
        print ( "{:>8s}".format ( d ), end='' )
    print ()
    print ( separator )
    for s in slist:
        for d in dimensions:
            min_W[d] = math.inf
        print ( "{:6.0f} (1) |".format ( s ), end='' )
        for d in dimensions:
            w = widths[d]
            h = heights[d]
            Fb_ = CD * Fb[d]  # psi, CM builtin to Fb[d]
            Sx = ( w * h ** 2 ) / 6  # in^3
            M_ = ( Sx * Fb_ ) / 12  # ft lbf
            # M_ = Mload = W * ( s^2 / 8 )
            W = M_ * 8 / s**2
            min_W[d] = min ( min_W[d], W )
            print ( "{:8.2f}".format ( W ), end='' )
        print ();
        print ( "       (2) |", end='' )
        for d in dimensions:
            w = widths[d]
            h = heights[d]
            Fv_ = CM_Fv * CD * Fv
            # Vload = W * ( s / 2 )
            # Fv_ = ( 3 * Vload ) / ( 2 * w * h )
            W = ( Fv_ * 2 * w * h ) / ( 3 * ( s / 2 ) )
            min_W[d] = min ( min_W[d], W )
            print ( "{:8.2f}".format ( W ), end='' )
        print ();
        print ( "       (3) |", end='' )
        for d in dimensions:
            w = widths[d]
            h = heights[d]
            E_ = CM_E * E
            # 1 / limit = ( 5 * W * s^3 * 12 )
            #           / ( 384 * E_ * ( w * h^3 ) )
            W = ( 12 * 384 * E_ * w * h**3 ) \
              / ( limit * 5 * ( 12 * s )**3 * 12 )
            min_W[d] = min ( min_W[d], W )
            print ( "{:8.2f}".format ( W ), end='' )
        print ();
        print ( "       (4) |", end='' )
        for d in dimensions:
            w = widths[d]
            Fc_perp_ = CM_Fcperp * Fc_perp
            # Pload = W * s / 2
            # area = Pload / Fc_perp_
            # bearing = area / w
            #         = W * s / ( 2 * Fc_perp_ * w )
            W = bearing * 2 * Fc_perp_ * w / s
            min_W[d] = min ( min_W[d], W )
            print ( "{:8.2f}".format ( W ), end='' )
        print ( );
        print ( "       (5) |", end='' )
        for d in dimensions:
            print ( "{:8.2f}".format ( min_W[d] ),
                    end='' )
        print (); print ( separator )

print ( """
\f
NOTES: (1) LRDF for pedestrian bridges requires
           90 lbf / sqft, deflection limit = span/360
       (2) For two stringer boardwalk sections with
           3 ft treads, this is met by
               2x6's for 6 ft span
               2x8's for 8 ft span
               2x10's for 10 ft span
               2x12's for 12 ft span
       (3) For 4 ft treads this is met by (2) if the
           bearing length is increased by 1 inch
           for 2x10's and 2x12's
""" )
