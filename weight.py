#!/bin/python3
#
# Boardwalk Weight Per Foot and Berring Width Calculator
#
# File:         weight.py
# Authors:      Bob Walton (walton@acm.org)
# Date:         Tue Mar 18 02:55:25 AM EDT 2025
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

Command: python3 weight.py

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
print ( standard_method, end='' )

# Data

# Dimensions
#
widths = { "2x4":  1.5, "4x4":  3.5,
           "2x6":  1.5, "4x6":  3.5,
           "2x8":  1.5, "4x8":  3.5,
           "2x10": 1.5, "4x10": 3.5,
           "2x12": 1.5, "4x12": 3.5 }
heights = { "2x4":  3.5,   "4x4":  3.5,
            "2x6":  5.5,   "4x6":  5.5,
            "2x8":  7.25,  "4x8":  7.25,
            "2x10": 9.25,  "4x10": 9.25,
            "2x12": 11.25, "4x12": 11.25 }
dimensions = [
    [ "2x4", "2x6", "2x8", "2x10", "2x12" ], # page group 1
    [ "4x4", "4x6", "4x8", "4x10", "4x12" ]  # page group 2
]
spans = [ [ 4, 5, 6, 7, 8, 9 ],         # subpage 1
          [ 10, 11, 12, 13, 14, 15 ],   # subpage 2
          [ 16, 17, 18, 19, 20, 21 ],   # subpage 3
          [ 22, 23, 24, 25, 26, 27 ] ]  # subpage 4


# Design Reference Values
#
WOOD = "No 1 Standard Southern Pine"
CM_Fb = 0.85  # for Fb > 1,150 psi
CM_Fv = 0.97
CM_E = 0.9
CM_Fcperp = 0.67
CD = 1.6 # for ten minutes
SnowLoad = 55 # lb/sqft for Acton MA
Fb = { "2x4": CM_Fb * 1500, "4x4": CM_Fb * 1500,
       "2x6": CM_Fb * 1350, "4x6": CM_Fb * 1350,
       "2x8": CM_Fb * 1250, "4x8": CM_Fb * 1250,
       "2x10": 1050, "4x10": 1050,
       "2x12": 1000, "4x12": 1000 }
       # CM_Fb included
Fv = 175
E = 1600000
Fc_perp = 565
limit = 360  # deflection limit = span / limit
bearing = 1.5 # inches design bearing

reference = """
Southern Yellow Pine Reference Design Values:

wood = {}
snow load = {} lb/sqft for Acton MA
load duration factor (CD) = {} for ten minutes
    Possible Values:    1.6  for ten minutes
                        1.25 for seven days
                        1.15 for two months (snow load)
                        0.9  for dead load
deflection limit = span/{}
design bearing length = {} inches
"""
print ( reference.format
            ( WOOD, SnowLoad, CD, limit, bearing ),
        end='' )



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
print ( """
Allowable
Weight      Is Proportional To
----  --------------------------------------------------
(1)   stringer width, CD, 1/span^2
(2)   stringer width, CD, 1/span
(3)   stringer width, deflection limit/span, 1/span^3
(4)   stringer width, bearing length, 1/span
""" )

print ( """
\f
NOTES: (1) LRDF for pedestrian bridges requires
           90 lbf / sqft, deflection limit = span/360
       (2) Bearing should be increased to
               2 inches for 2x10's
               2.5 inches for 2x12's
       (3) Loads (1) and (2) must be multiplied by
           CD-two-months/CD-10-minutes = 1.15/1.6 = 71%
           to accommodate snow load.  For 55 lb/sqft
           with 4 ft treads and 2 stringers, this load
           per string is 110 lb/ft = 71% * 155 lb/ft.
       (4) For two-stringer boardwalk sections with
           3 ft or 4 ft treads, this is met by
               2x4's for 4 ft span **
               2x6's for 6 ft span
               2x8's for 8 ft span
               2x10's for 10 ft span
               2x12's for 12 ft span
               4x4's for 5 ft span
               4x6's for 8 ft span
               4x8's for 10 ft span
               4x10's for 13.5 ft span
               4x12's for 16 ft span
           (** but NOT for 4 ft treads )
       (5) If you add a middle stringer (to 3 total)
           you can increase the span by a factor of
           the cube root of 1.5 = 1.14.
       (6) If you double the number of stringers (to 4)
           you can increase the span by a factor of
           the cube root of 2 = 1.26.
       (7) If you triple the number of stringers (to 6)
           you can increase the span by a factor of
           the cube root of 3 = 1.44.
""" )
separator = "-----------+----------------------------" \
            "--------------------"
for dlist in dimensions:
    for slist in spans:
        print ( "\f" )
        print ( ' SPAN FT   |', end='' )
        for d in dlist:
            print ( "{:>8s}".format ( d ), end='' )
        print ()
        print ( separator )
        for s in slist:
            print ( "{:6.0f} (1) |".format ( s ),
                    end='' )
            for d in dlist:
                w = widths[d]
                h = heights[d]
                Fb_ = CD * Fb[d] 
                    # psi, CM builtin to Fb[d]
                Sx = ( w * h ** 2 ) / 6  # in^3
                M_ = ( Sx * Fb_ ) / 12  # ft lbf
                # M_ = Mload = W * ( s^2 / 8 )
                W = M_ * 8 / s**2
                print ( "{:8.2f}".format ( W ), end='' )
            print ();
            print ( "       (2) |", end='' )
            for d in dlist:
                w = widths[d]
                h = heights[d]
                Fv_ = CM_Fv * CD * Fv
                # Vload = W * ( s / 2 )
                # Fv_ = ( 3 * Vload ) / ( 2 * w * h )
                W = ( Fv_ * 2 * w * h ) \
                  / ( 3 * ( s / 2 ) )
                print ( "{:8.2f}".format ( W ), end='' )
            print ();
            print ( "       (3) |", end='' )
            for d in dlist:
                w = widths[d]
                h = heights[d]
                E_ = CM_E * E
                # 1 / limit = ( 5 * W * s^3 * 12 )
                #           / ( 384 * E_ * ( w * h^3 ) )
                W = ( 12 * 384 * E_ * w * h**3 ) \
                  / ( limit * 5 * ( 12 * s )**3 * 12 )
                print ( "{:8.2f}".format ( W ), end='' )
            print ();
            print ( "       (4) |", end='' )
            for d in dlist:
                w = widths[d]
                Fc_perp_ = CM_Fcperp * Fc_perp
                # Pload = W * s / 2
                # area = Pload / Fc_perp_
                # bearing = area / w
                #         = W * s / ( 2 * Fc_perp_ * w )
                W = bearing * 2 * Fc_perp_ * w / s
                print ( "{:8.2f}".format ( W ), end='' )
            print (); print ( separator )
