#!/bin/python3
#
# Boardwalk Span Factor Calculator
#
# File:         span.py
# Authors:      Bob Walton (walton@acm.org)
# Date:         Wed Jan  8 01:43:47 AM EST 2025
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

standard_method = """
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
\f
For simplicity of output, we set:

H = effective height of stringers
  = actual height of a stringer if NOT truss
  = sum of actual heights of `stringers' if truss

W = sum of actual widths of stringers
    (typically number of stringers times actual
     width of one stringer)
"""
print ( standard_method )

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
LENGTH = 36 # tread length

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
          ( L, WxH, W, H, N, LENGTH, E, WOOD,
            N*W, H ) )


reference = [
    [ "No 1 Dense", 1800000 ],
    [ "No 1", 1600000 ],
    [ "No 1 Non-Dense", 1400000 ]
]

tread_lengths = [ 24, 36, 44, 48 ]

stringer_heights = [ 3.5, 5.5, 7.25, 9.25, 11.25 ]

effective_widths = [ 3.0, 3.5, 4.0, 4.5, 5.0, 5.5,
                     6.0, 6.5, 7.0, 7.5, 8.0, 8.5,
                     9.0, 16.0, 24.0, 36.0, 42.0, 48.0 ]

truss_heights = [ 11.0, 12.75, 14.5, 14.75,
                  16.5, 16.75, 18.5, 20.5, 22.5 ]

truss_effective_widths = [ 3.0, 6.0, 7.0, 10.0, 14.0 ]

W = N*W

# Main Program

# Standard Method

print ( "\f" )
print ( '  STANDARD NON-TRUSS SPAN LENGTH IN FEET' )
print ( '                     H' )
print ( '   W   |', end='' )
for h in stringer_heights:
    print ( "{:6.2f}".format ( h ), end='' )
print ()
print ( '-------+------------------------------' )
for w in effective_widths:
    print ( "{:6.2f} |".format ( w ), end='' )
    for h in stringer_heights:
        f =  ( ( w / W ) * ( h / H ) ** 3 ) \
          ** (1.0 / 3.0 )
        l = f * L
        print ( "{:6.2f}".format ( l ), end='' )
    print ();
print ();

print ( '    STANDARD TRUSS SPAN LENGTH IN FEET' )
print ( '   *** TRUSS BRIDGE DESIGNS MUST BE ***' )
print ( '   ****** CHECKED BY AN ENGINEER ******' )
print ( '                    W' )
print ( '   H   |', end='' )
for w in truss_effective_widths:
    print ( "{:6.2f}".format ( w ), end='' )
print ()
print ( '-------+------------------------------' )
for h in truss_heights:
    print ( "{:6.2f} |".format ( h ), end='' )
    for w in truss_effective_widths:
        f =  ( ( w / W ) * ( h / H ) ** 3 ) \
          ** (1.0 / 3.0 )
        l = f * L
        print ( "{:6.2f}".format ( l ), end='' )
    print ();

# Compensation Multipliers

print ( "\f")
print ( "STANDARD MODULUS OF ELASTICITY"
        " SPAN LENGTH MULTIPLIER" )
print ( "       type          E      multiplier" )
for r in reference:
    type = r[0]
    e = r[1]
    m = ( float( e ) / E ) ** ( 1.0 / 3.0 )
    print ( "{0}   {1:7d}     {2:5.2f}"
            .format ( type.rjust(15), e, m ) )

print ()
print ( "STANDARD TREAD LENGTH SPAN LENGTH MULTIPLIER" )
print ( "length   multiplier" )
for length in tread_lengths:
    m = ( LENGTH / length ) ** ( 1.0 / 3.0 )
    print ( " {0:2d}in     {1:5.2f}"
            .format ( length, m ) )

# Alternate Method

print ( "\f" )

alternate_method = """
SPAN LENGTH BY ALTERNATE NDS METHOD
---- ------ -- --------- --- ------

This is the same as the Standard NDS Method, except
that instead of holding the weight per square foot
constant, we hold total weight constant.

This method is NOT valid if the resulting span
length is less that the reference length.  For example,
if the reference section can hold 3 people, this method
calculates the span that can hold 3 people for other
parameters, but if the result is 60% of the reference
length, only 2 people will fit.  So results less than
the reference length are NOT given.

According to the NDS equations for joists, for fixed
total weight:

    deflection/span is directly proportional to:
        the square of the span
    and inversely proportional to:
        the actual width of the stringer
        and
        the cube of the actual height of the stringer
        and
        the number of stringers

The elastic modulus multiplier given below is different
for the alternate method.

For simplicity of output, we set:

H = effective height of stringers
  = actual height of a stringer if NOT truss
  = sum of actual heights of `stringers' if truss

W = sum of actual widths of stringers
    (typically number of stringers times actual
     width of one stringer)
"""
print ( alternate_method )

print ( "\f" )
print ( '  ALTERNATE NON-TRUSS SPAN LENGTH IN FEET' )
print ( '                     H' )
print ( '   W   |', end='' )
for h in stringer_heights:
    print ( "{:6.2f}".format ( h ), end='' )
print ()
print ( '-------+------------------------------' )
for w in effective_widths:
    print ( "{:6.2f} |".format ( w ), end='' )
    for h in stringer_heights:
        f =  ( ( w / W ) * ( h / H ) ** 3 ) \
          ** (1.0 / 2.0 )
        l = f * L
        if l < L:
            print ( ' -----', end='' )
        else:
            print ( "{:6.2f}".format ( l ), end='' )
    print ();
print ();

print ( '    ALTERNATE TRUSS SPAN LENGTH IN FEET' )
print ( '   *** TRUSS BRIDGE DESIGNS MUST BE ***' )
print ( '   ****** CHECKED BY AN ENGINEER ******' )
print ( '                    W' )
print ( '   H   |', end='' )
for w in truss_effective_widths:
    print ( "{:6.2f}".format ( w ), end='' )
print ()
print ( '-------+------------------------------' )
for h in truss_heights:
    print ( "{:6.2f} |".format ( h ), end='' )
    for w in truss_effective_widths:
        f =  ( ( w / W ) * ( h / H ) ** 3 ) \
          ** (1.0 / 2.0 )
        l = f * L
        if l < L:
            print ( ' -----', end='' )
        else:
            print ( "{:6.2f}".format ( l ), end='' )
    print ();

# Compensation Multipliers

print ( "\f" )
print ( "ALTERNATE MODULUS OF ELASTICITY"
        " SPAN LENGTH MULTIPLIER" )
print ( "       type          E      multiplier" )
for r in reference:
    type = r[0]
    e = r[1]
    m = ( float( e ) / E ) ** ( 1.0 / 2.0 )
    print ( "{0}   {1:7d}     {2:5.2f}"
            .format ( type.rjust(15), e, m ) )
