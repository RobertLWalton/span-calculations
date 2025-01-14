#!/bin/python3
#
# Boardwalk Weight Per Foot and Berring Width Calculator
#
# File:         weight.py
# Authors:      Bob Walton (walton@acm.org)
# Date:         Tue Jan 14 01:43:29 AM EST 2025
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
spans = [ 6, 8, 10, 12, 14, 16, 18, 20, 22, 24 ]


# Design Reference Values
#
WOOD = "No 1 Standard"
CM = 0.85
Fb = { "2x4": 1500, "4x4": 1500,
       "2x6": 1350, "4x6": 1350,
       "2x8": 1250, "4x8": 1250,
       "2x10": 1050, "4x10": 1050,
       "2x12": 1000, "4x10": 1000 }
Fv = 175
E = 1600000
limit = 240

reference = """
Reference Section Values:

wood = {}
CM (wet factor ) = {}
bending force (Fb) = {} psi
sheer force (Fv) = {} psi
elastic modulus = {} psi
deflection limit = 1/{}

"""
print ( reference.format
          ( WOOD, CM, Fb, Fv, E, limit ) )



# Main Program

# Standard Method

print ( "\f" )
print ( "(1) ALLOWED WEIGHT IN LBF/FT BY MOMENT"
           " CAPACITY" )
print ( '(2) ALLOWED WEIGHT IN LBF/FT BY SHEER' )
print ( '(3) ALLOWED WEIGHT IN LBF/FT BY DEFLECTION' )
print ( '(4) BEARING LENGTH IN IN' )
print ( '                     H' )
print ( ' SPAN      |', end='' )
separator = "-----------+----------------------------" \
            "--------------------"
for d in dimensions:
    print ( "{:>8s}".format ( d ), end='' )
print ()
print ( separator )
for s in spans:
    print ( "{:6.0f} (1) |".format ( s ), end='' )
    for d in dimensions:
        w = widths[d]
        h = heights[d]
        Fb_ = CM * Fb[d]  # psi
        Sx = ( w * h ** 2 ) / 6  # in^3
        M_ = ( Sx * Fb_ ) / 12  # ft lbf
        # M_ = Mload = W * ( s^2 / 6 )
        W = M_ * 6 / s**2
        print ( "{:8.2f}".format ( W ), end='' )
    print ();
    print ( "       (2) |", end='' )
    for d in dimensions:
        w = widths[d]
        h = heights[d]
        Fv_ = CM * Fv
        # Vload = W * ( s / 2 )
        # Fv_ = ( 3 * Vload ) / ( 2 * w * h )
        W = ( Fv_ * 2 * w * h ) / ( 3 * ( s / 2 ) )
        print ( "{:8.2f}".format ( W ), end='' )
    print ();
    print ( "       (3) |", end='' )
    for d in dimensions:
        w = widths[d]
        h = heights[d]
        # 1 / limit = ( 5 * W * s^3 * 12 )
        #           / ( 384 * E * ( w * h^3 ) )
        W = ( 12 * 384 * E * w * h**3 ) \
          / ( limit * 5 * ( 12 * s )**3 * 12 )
        print ( "{:8.2f}".format ( W ), end='' )
    print ( ); print ( separator )
