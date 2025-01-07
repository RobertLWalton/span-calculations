#!/bin/python3
#
# Boardwalk Span Factor Calculator
#
# File:         span.py
# Authors:      Bob Walton (walton@acm.org)
# Date:         Tue Jan  7 12:52:52 PM EST 2025
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
SPAN LENGTH BY STANDARD NDS METHOD
---- ------ -- -------- --- ------

The standard NDS joist check limits the deflection/span
for a given weight per square foot.

Given this, our procedure here is:

    Hold deflection/span and weight per square foot
    constant and compute how the span changes when the
    boardwalk section parameters change relative to the
    reference boardwalk section.

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

For symplicity of output, we set:

H = effective height of stringers
  = actual height of a stringer if NOT truss
  = sum of actual heights of `stringers' if truss

W = sum of actual widths of stringers
    times reference tread length / tread length
    times elastic modulus / reference elastic modulue
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
W = {}
H = {}

"""
print ( reference.format
          ( L, WxH, W, H, N, WIDTH, E, WOOD,
            N*W, H ) )


reference = [
    [ "No 1 Dense", 1800000 ],
    [ "No 1", 1600000 ],
    [ "No 1 Non-Dense", 1400000 ]
]

widths = [ 24, 36, 44, 48 ]


# Main Program

print ( '                          SPAN LENGTH IN FEET' )
print ( '                                   W' )
print ( '   H  ', end='' )
for wx in range ( 10 ):
    w = 3.0 + 0.5 * wx
    print ( "{:6.2f}".format ( w ), end='' )
print ()
for hx in range ( 40 ):
    h = 3.0 + 0.5 * hx
    print ( "{:6.2f}".format ( h ), end='' )
    for wx in range ( 10 ):
        w = 3.0 + 0.5 * wx
        f = ( ( w / W ) * ( h / H ) ** 3 ) ** (1.0 / 3.0 )
        l = f * L
        print ( "{:6.2f}".format ( l ), end='' )
    print ();
print ();

print ( '                          SPAN LENGTH IN FEET' )
print ( '                                   W' )
print ( '   H  ', end='' )
for wx in range ( 10 ):
    w = 8.0 + 0.5 * wx
    print ( "{:6.2f}".format ( w ), end='' )
print ()
for hx in range ( 40 ):
    h = 3.0 + 0.5 * hx
    print ( "{:6.2f}".format ( h ), end='' )
    for wx in range ( 10 ):
        w = 3.0 + 0.5 * wx
        f = ( ( w / W ) * ( h / H ) ** 3 ) ** (1.0 / 3.0 )
        l = f * L
        print ( "{:6.2f}".format ( l ), end='' )
    print ();
