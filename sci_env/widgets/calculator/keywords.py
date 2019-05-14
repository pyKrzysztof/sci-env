import math

# functions too hard for me to implement at this point.
log10 = math.log10
log2 = math.log2
sin = math.sin
cos = math.cos
tan = math.tan

# constants
pi = math.pi
e = math.e

# factorial function:
def factorial(n):
    if n <= 1:
    	return n
    previous = 0
    current = 1
    for _ in range(n - 1):
    	previous, current = current, current + previous
    return current

# root function:
def root(x, degree=2):
    return x**(1/degree)

# to radians:
def rad(deg):
    return deg*pi/180

# to degrees:
def deg(rad):
    return rad*180/pi