from random import randint, choice, seed
from format import*

def not0(min, max) :
    x = randint(min, max)
    while x == 0 :
        x = randint(min, max)
    return x

def notall0(min, max, n) :
    L = [randint(min, max) for _ in range(n)]
    while L == [0]*n :
        L = [randint(min, max) for _ in range(n)]
    return L

def nomonom(min, max, n) :
    while True :
        L = [randint(min, max) for _ in range(n)]
        if sum([abs(l) for l in L]) >= 2 :
            return L

def aff(coef_max) :
    coefs = [randint(-coef_max, coef_max) for _ in range(4)]
    a, b, c, d = list(map(str, coefs))
    eq = f" {a}x+{b}= {c}x+{d}"
    eq = clean(eq)
    return eq, coefs

def poly2(coef_max) :
    a = not0(-coef_max, coef_max)
    coefs = [a] + [randint(-coef_max, coef_max) for _ in range(2)]
    a, b, c = list(map(str, coefs))
    eq = f" {a}x^2+{b}x+{c}"
    eq = clean(eq)
    return eq, coefs

def poly3(coef_max) :
    a = 2*not0(-coef_max, coef_max)
    x1, x2, d = randint(-coef_max, coef_max), randint(-coef_max, coef_max), randint(-coef_max, coef_max)
    b, c = -3*a*(x1+x2)//2, 3*a*x1*x2
    if x1 == x2 :
        x2 =""
    coefs = [a, x1, x2]
    x = symbols("x")
    eq = clean(f"{a}x^3+{b}x^2+{c}x+{d}")
    a, b, c, d = list(map(str, [a,b,c,d]))
    return eq, coefs

def rat2(coef_max) :
    a, d = 1, 1
    b , c, e, f = 0,0,0,0
    if randint(0,5) < 3 :
        while a*e - d*b == b*f - c*e or e == f == 0 :
            a = randint(-coef_max//3,coef_max//3)
            d = a
            while d in [-a, a] :
                d = randint(-coef_max//3,coef_max//3)
            k = 2*not0(-coef_max//2,coef_max//2)
            x1, x2 = randint(-coef_max, coef_max),  randint(-coef_max, coef_max)
            while  x1 + x2 == 0 :
                x2 = randint(-coef_max, coef_max)
            if a != 0 :
                seuil = abs(36//a)
            else :
                seuil = 36
            m, M = min((x1*x2+seuil)//(x1+x2),(x1*x2-seuil)//(x1+x2)), max((x1*x2+seuil)//(x1+x2),(x1*x2-seuil)//(x1+x2))
            alpha = randint(m,M)
            c = -x1*x2 + alpha*(x1+x2)
            b = -2*(x1*x2 + c)//(x1 + x2)
            e = k + b
            f = c - k*(x1+x2)//2
            b, c = a*b, a*c
            e, f = d*e, d*f
    else :
        while f == c :
            a = 1
            d = a
            b = 2*randint(-coef_max//2, coef_max//2)
            c, f = [randint(-coef_max, coef_max) for _ in range(2)]
            e = b
    coefs = [a, b, c, d, e , f]
    a, b, c, d, e, f = list(map(str, coefs))
    num , den = clean(f" {a}x^2+{b}x+{c}"), clean(f" {d}x^2+{e}x+{f}")
    # if randint(0,1) == 0 :
    eq = rf"\dfrac{{{num}}}{{{den}}}"
    # else :
    #     eq = rf"\dfrac{{{den}}}{{{num}}}"
    return eq, coefs

def exp2(coef_max) :
    a = not0(-1,1)
    b, m, n = [randint(-coef_max, coef_max) for _ in range(3)]
    a2, a1, a0 = 1//a, - (m+n)//a -2//a**2, m*n//a + (m+n)//a**2 + 2//a**3
    expr = clean(f"({a2}x^2+{a1}x+{a0})e^{{{a}x+{b}}}")
    return expr, [a2, a1, a0, a, b]