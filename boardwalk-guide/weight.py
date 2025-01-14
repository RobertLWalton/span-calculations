#!/bin/python3
#
# Boardwalk Weight Per Foot and Berring Width Calculator
#
# File:         weight.py
# Authors:      Bob Walton (walton@acm.org)
# Date:         Sun Jan 12 01:23:56 PM EST 2025
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



# Design Reference Values
#
width = 1.5
WOOD = "No 1 Standard"
CM = 0.85
Fb = 1000
Fv = 175
E = 1600000
limit = 240

reference = """
Reference Section Values:

stringer width = {} in
wood = {}
CM (wet factor ) = {}
bending force (Fb) = {} psi
sheer force (Fv) = {} psi
elastic modulus = {} psi
deflection limit = 1/{}

"""
print ( reference.format
          ( width, WOOD, CM, Fb, Fv, E, limit ) )



spans = [ 6, 8, 10, 12 ]
heights = [ 5.5, 7.25, 9.25, 11.25 ]

# Main Program

# Standard Method

print ( "\f" )
print ( '  ALLOWED WEIGHTS IN LBF/FT' )
print ( '  (1) BY MOMENT CAPACITY' )
print ( '  (2) BY SHEER' )
print ( '  (3) BY DEFLECTION' )
print ( '  (4) BEARING LENGTH IN IN' )
print ( '                     H' )
print ( ' SPAN      |', end='' )
for h in heights:
    print ( "{:7.2f}".format ( h ), end='' )
print ()
print ( '-----------+----------------------------' )
for s in spans:
    print ( "{:6.0f} (1) |".format ( s ), end='' )
    for h in heights:
        Fb_ = CM * Fb  # psi
        Sx = ( width * h ** 2 ) / 6  # in^3
        M_ = ( Sx * Fb_ ) / 12  # ft lbf
        # M_ = Mload = w * ( span^2 / 6 )
        w = M_ * 6 / s**2
        print ( "{:7.2f}".format ( w ), end='' )
    print ();
    print ( "       (2) |", end='' )
    for h in heights:
        Fv_ = CM * Fv  # psi
        # Vload = w * ( s / 2 )
        # Fv_ = ( 3 * Vload ) / ( 2 * width * h )
        w = ( Fv_ * 2 * width * h ) / ( 3 * ( s / 2 ) )
        print ( "{:7.2f}".format ( w ), end='' )
    print ();
    print ( "       (3) |", end='' )
    for h in heights:
        Fv_ = CM * Fv  # psi
        # 1 / limit = ( 5 * w * s^3 * 12 )
        #           / ( 384 * E * ( width * h^3 ) )
        w = ( 12 * 384 * E * width * h**3 ) \
          / ( limit * 5 * ( 12 * s )**3 * 12 )
        print ( "{:7.2f}".format ( w ), end='' )
    print ();
