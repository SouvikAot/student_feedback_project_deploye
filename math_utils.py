import math

def factorial(n):
    if n < 1:
        raise ValueError("Factorial not defined for numbers less than 1")
    result = 1
    for i in range(1, n+1):
        result *= i
    return result

def is_prime(n):
    if n < 2:
        raise ValueError("Prime check not valid for numbers less than 2")
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def area_of_circle(r):
    if r <= 0:
        raise ValueError("Radius must be greater than 0")
    return math.pi * r * r
