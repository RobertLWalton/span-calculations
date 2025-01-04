#!/bin/python3
#
# Boardwalk Span Factor Calculator
#
# File:         span.py
# Authors:      Bob Walton (walton@acm.org)
# Date:         Sat Jan  4 06:02:08 PM EST 2025
#
# The authors have placed this program in the public
# domain; they make no warranty and accept no liability
# for this program.

import sys
import math
import re

document = """
Program to compute spans of boardwalks with different
stringer numbers, cross-sections, and wood quality.

Command: python3 span.py

""";

if len ( sys.argv ) > 1:
    print ( document )
    exit ( 1 )

method = """
Method:

Hold deflection/span and weight per square foot constant
and compute how the span changes when the boardwalk
section parameters change relative to the reference
boardwalk section.

For each parameter that is changed, the span is
multiplied by a factor dependent on the changed
parameter value.  Multiple parameter changes produce
multiple factors that are multiplied together before
multiplying by the reference section span.

According to the NDS equations for joists, for fixed
weight per square foot:

    deflection/span is directly proportional to:
        the cube of the span
        and
        the length of the tread
    and inversely proportional to:
        the actual width of the stringer
        and
        the cube of the actual height of the stringer
        and
        the number of stringers
        and
        the elastic modulus of the wood
"""
print ( method )

# Data



# Reference Section Values
#
WxH = "2x8" # cross-section dimension
W = 1.5 # actual cross-section width
H = 7.25 # actual cross-section height
L = 8 # length in feet
N = 2 # number of stringers
WOOD = "No 1 Standard"
E = 1600000 # No 1 Modulus of Elasticity
WIDTH = 36 # tread length

reference = """
Reference Section Values:

span = {}ft
cross section = {}, actual {:.2f}in x {:.2f}in
number of stringers = {}
tread length = {}in
elastic modulus = {} for {}

"""
print ( reference.format
          ( L, WxH, W, H, N, WIDTH, E, WOOD ) )

# Cross-section catalog
#
# ["wxh", w, h]
#
cross = [
    [ "2x4", 1.5, 3.5 ],
    [ "2x6", 1.5, 5.5 ],
    [ "2x8", 1.5, 7.25 ],
    [ "2x10", 1.5, 9.25 ],
    [ "2x12", 1.5, 11.25 ],
    [ "4x4", 3.5, 3.5 ],
    [ "4x6", 3.5, 5.5 ],
    [ "4x8", 3.5, 7.25 ],
    [ "4x10", 3.5, 9.25 ],
    [ "4x12", 3.5, 11.25 ],
    [ "6x4", 5.5, 3.5 ],
    [ "6x6", 5.5, 5.5 ],
    [ "6x8", 5.5, 7.25 ],
    [ "6x10", 5.5, 9.25 ],
    [ "6x12", 5.5, 11.25 ],
    [ "8x4", 7.25, 3.5 ],
    [ "8x6", 7.25, 5.5 ],
    [ "8x8", 7.25, 7.25 ],
    [ "8x10", 7.25, 9.25 ],
    [ "8x12", 7.25, 11.25 ]
]

stringers = [ 2, 3, 4, 5, 6, 7, 8, 9,
              10, 11, 12, 16, 24, 32 ]

reference = [
    [ "No 1 Dense", 1800000 ],
    [ "No 1", 1600000 ],
    [ "No 1 Non-Dense", 1400000 ]
]

widths = [ 24, 36, 44, 48 ]


# Main Program

print ( "CROSS SECTION FACTORS" )
print ( " WxH    H      W     factor length" )
for c in cross:
    wxh = c[0]
    w = c[1]
    h =  c[2]
    f = ( ( w / W ) * ( h / H ) ** 3 ) ** (1.0 / 3.0 )
    l = f * L
    print ( "{0} {1:4.2f}in {2:5.2f}in {3:6.2f} {4:5.2f}ft"
            .format ( wxh.rjust(4), w, h, f, l ) )

print ( "" )
print ( "NUMBER OF STRINGERS (N) FACTORS" )
print ( " N factor  length" )
for n in stringers:
    f = ( n / N ) ** ( 1.0 / 3.0 )
    l = f * L
    print ( "{0:2d} {1:5.2f}  {2:5.2f}ft"
            .format ( n, f, l ) )

print ( "" )
print ( "MODULUS OF ELASTICITY FACTORS" )
print ( "       type        E  factor  length" )
for r in reference:
    type = r[0]
    e = r[1]
    f = ( float( e ) / E ) ** ( 1.0 / 3.0 )
    l = f * L
    print ( "{0} {1:7d} {2:5.2f}  {3:5.2f}ft"
            .format ( type.rjust(15), e, f, l ) )

print ( "" )
print ( "TREAD WIDTH FACTORS" )
print ( "width   factor  length" )
for width in widths:
    f = ( WIDTH / width ) ** ( 1.0 / 3.0 )
    l = f * L
    print ( "{0:2d}in {1:5.2f}  {2:5.2f}ft"
            .format ( width, f, l ) )
