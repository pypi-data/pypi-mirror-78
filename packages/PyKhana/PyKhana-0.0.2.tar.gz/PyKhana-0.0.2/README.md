It is easy to take the unique factorization property for granted, but with more experience we will
see that this gift is not something which had to happen. Among the similar “integers” that are
dealt with in the advanced topics of number theory there are examples with unique factorization
(for example the Gaussian integers, Z[i]) and conversely there are examples where unique
factorization fails (for example Z[√-5], where the otherwise perfectly well behaved integer 6 has
as prime factorizations both 6 = (2)(3) and a second one 6 = (-1)(1+√-5)(1-√-5)).

The package PyKhana contains a method implemented entirely in Python3.
It can be used to implement Gaussian Integer Numbers.

Gaussian Integer functions.
Functions implemented are:
Arithmetic functions: +,*,//,%,**(exponentiation)
a.gcd(b) - Compute the greatest common divisor of a and b.
a.xgcd(b) - Extended gcd - return gcd(a,b) and x,y such that gcd(a,b)=xa+yb.
n.isprime() - Is n prime (pseudoprime tests)
n.factor() - Return a factor of n.
n.factors() - Return list of the factors of n.
Gaussian Integers can be created by:
n = GaussInt(5,7)  # Create (5 + 7i)
n = GaussInt(13)  # Create (5 + 0i)
z = complex(2,3); n = GaussInt(z) # Round the complex number to integer form