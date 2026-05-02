'''taper dans la console  les instructions suivantes pour installer les packages'''
# pip install sympy, latex2sympy2
from sympy import *
from latex2sympy2 import latex2sympy
import shutil
import subprocess
import os
import re


def parentheses(expr) :
    expr = expr.replace("**", "^")
    expr = expr.replace("*", "\\times ")
    expr = expr.replace("\\times+", "\\times ")
    expr = re.sub(r'(\\times)\s*-\s*([0-9]*e\^\{[^{}]+\})',r'\1 (-\2)',expr)
    expr = re.sub(r'--([0-9a-zA-Z(][^+\-=]*)',r'-(-\1)', expr)
    expr = re.sub(r'(\\times)\s*-\s*([0-9a-zA-Z(][^+\-]*)', r'\1 (-\2)', expr)
    pattern = r'(\\times)\s*-\s*(\\frac\{[^}]+\}\{[^}]+\}|[^+\-]+)'
    def repl(m):
        return f"{m.group(1)}\\left(-{m.group(2)}\\right)"
    return re.sub(pattern, repl, expr)

def signe(x) :
    if isinstance(x, str) :
        x = latex2sympy(x)
    if x > 0 :
        s = "+"
    elif x < 0 :
        s = "-"
    elif x == 0 :
        s = ""
    return s

def rsignes(expr) :
    return expr.replace("--","+").replace("-+","-").replace("+-", "-").replace("++", "+")

def parenthese(x, var = None) :
    if var == None :
        var = ""
    if x < 0 :
        x = "(" + str(x) + var + ")"
    else:
        x =  str(x)
    return x

def clean(eq, var = "x") :
    eq = eq.replace("−", "-")
    eq = " " + eq
    eq = eq.replace(" 1e^", "e^")
    eq = eq.replace("-1e^", "-e^")
    eq = eq.replace(" 1(", "(")
    eq = eq.replace(" 1\left(", "\left(")
    eq = eq.replace(f" 1{var}", f" {var}")
    eq = eq.replace(f" 1{var}^2", f" {var}^2")
    eq = eq.replace(f"- 0{var}^2", "")
    eq = eq.replace(f"+ 0{var}^2", "")
    eq = eq.replace(f"-0{var}^2", "")
    eq = eq.replace(f"+0{var}^2", "")
    eq = eq.replace(f" 0{var}^2", "")
    eq = eq.replace(f"+ 0{var}", "")
    eq = eq.replace(f"- 0{var}", "")
    eq = eq.replace(f" 0{var}", "")
    eq = eq.replace(" 0 -", "-")
    eq = eq.replace(" ", "")
    eq = parentheses(eq)
    eq = eq.replace("-1(", "-(")
    eq = eq.replace("+1(", "(")
    eq = eq.replace("-()", "")
    eq = eq.replace("+()", "")
    eq = eq.replace("-0)", ")")
    eq = eq.replace("+0)", ")")
    eq = eq.replace("-1\left(", "-\left(")
    eq = eq.replace("+1\left(", "\left(")
    eq = eq.replace("-\left(\right)", "")
    eq = eq.replace(f"\left({var}\right)", f"{var}")
    eq = eq.replace("+\left(\right)", "")
    eq = eq.replace("-0\right)", "\right)")
    eq = eq.replace("+0\right)", "\right)")
    eq = eq.replace("-+", "-")
    eq = eq.replace("+-", "-")
    eq = eq.replace("++", "+")
    eq = eq.replace("--", "+")
    eq = eq.replace("+1x", f"+{var}")
    eq = eq.replace("-1x", f"-{var}")
    eq = eq.replace("+1x^2", f"+{var}^2")
    eq = eq.replace("-1x^2", f"-{var}^2")
    eq = eq.replace("+=", "=")
    eq = eq.replace("-=", "=")
    eq = eq.replace("=+", "=")
    eq = eq.replace("(0x", "(").replace("{0x", "{")
    eq = eq.replace("(1x", "(x").replace("{1x", "{x")
    eq = eq.replace("\left(0x", "\left(")
    eq = eq.replace("\left(1x", "\left(x")
    eq = eq.replace("--(", "-(")
    eq = eq.replace("+\\dfrac{-", "-\\dfrac{")
    eq = eq.replace("\\dfrac{+", "\\dfrac{")
    eq = eq.replace("+}", "}")
    eq = eq.replace("{+", "{")
    eq = eq.replace(f"({var})", f"{var}")
    eq = eq.replace(f"\\left({var}\\right)", f"{var}")
    symboles = ["+", "-"]
    nullify = [sym + f"0{var}" for sym in symboles] + [sym + f"0" for sym in symboles] #+ ["-0",  "+0" ]
    for null in nullify :
        eq = eq.replace(null, " ")
    eq = ((eq+ " ").replace("+0 ", " ").replace("-0 ", " "))[:-1]
    if (" " + eq)[-1] in ["= ", "="] :
        eq += "0"
    if (eq + " ")[0] in ["="] :
        eq = eq.replace("=", "0=", 1)
    if (eq + " ")[0]  == "+" :
        eq = eq.replace("+", "", 1)
    if eq.replace(" ", "") == "" :
        eq = "0"
    # eq = eq.replace('\\times0', "")
    eq = eq.replace('\\timesx', "\\times x")
    return eq

def clean_coef(eq, seps = ["x^2", "x"]) :
    if "x^{" in eq :
        seps = [sep.replace("x^", "x^{") + "}" if sep != "x" else sep for sep in seps ]
    coefs = []
    for sep in seps :
        if len(eq.split(sep, 1)) > 1 :
            coef , eq = eq.split(sep, 1)
        else :
            coef = "0"
            eq = eq.split(sep, 1)[0]
        if coef.replace(" ", "") in ["", "+"] and sep != "=" :
            coef = "1"
        elif coef.replace(" ", "") in ["", "+"] :
            coef = "0"
        elif coef.replace(" ", "") == "-" :
            coef = "-1"
        coef = coef.replace("+", "")  + " "
        if "\\times" in coef and "times-" in coef[-7:] :
            coef = coef.replace("times-", "times-1")
        elif "\\times" in coef and "times " in coef[-7:] :
            coef = coef.replace("times ", "times 1")
        coefs += [coef]
    if eq.replace(" ", "") != "" :
        coefs += [eq]
    else :
        coefs += ["0"]
    coefs = [coef.replace("\\right)", "").replace("\\left(", "").replace("(", "").replace(")", "").replace(" ", "") for coef in coefs]
    return coefs

def clean_frac(a, times = True) :
    a = a.replace("}\\right)", "")
    if "frac" in a :
        num, den = a.split("}{")
        num = num.replace("\\dfrac", "")
        num = num.replace("\dfrac", "")
        num, den = num.replace("}", ""), den.replace("}", "")
        num, den = num.replace("{", ""), den.replace("{", "")
        num, den = parentheses(num), parentheses(den)
        if times == True :
            num, den = num.replace("\times", "*"), den.replace("\times", "*")
        if "\left(" in a :
            num = num.replace("\\left(", "(") +")"
            den = den.replace("\\right)", "")
        if "})^2" in den[-2:] :
            num += "^2"
        elif "})^3" in den[-2:] :
            num += "^3"
    else :
        num = a
        den = "1"
    return num, den

def frac2sympy(frac) :
    num, den = clean_frac(frac)
    match = re.search(r"\^(\d+)", den)
    if match:
        puissance = match.group(1)
        num += "^" + puissance
    num = sympify(num.replace("\\times", "\times").replace("\times", "*").replace("\\left(", "(").replace("\\right)", ")"))
    if "frac" in frac :
        num, den = sympify(num), sympify(den.replace("\\left(", "(").replace("\\right)", ")"))
    else :
        den = 1
    return num, den

def nodouble(steps):
    return [steps[k] for k in range(len(steps) - 1) if clean(steps[k]).replace(" ", "")  != clean(steps[k+1]).replace(" ", "") ] + [steps[-1]]


def get_coefs(poly, n = None):
    poly = poly.replace(" ", "")
    monomes = re.findall(r'[+-]?[^+-]+', poly)
    coefs = []
    for mon in monomes:
        if "x^" in mon:
            coef, deg = mon.split("x^")
            deg = int(deg.replace("{","").replace("}",""))
        elif "x" in mon:
            coef = mon.replace("x", "")
            deg = 1
        else:
            coef = mon
            deg = 0
        if coef in ["", "+"]:
            coef = "1"
        elif coef == "-":
            coef = "-1"
        coefs.append(coef)
    if n != None :
        coefs = ["0"]*(n - len(coefs)) + coefs
    return coefs

def get_fcoefs(poly, degmax = None):
    poly = poly.replace(" ", "")
    parts = re.split(r'x(?:\^\{?\d+\}?)?', poly)
    if degmax == None :
        degmax = len(parts)
    while len(parts) < degmax:
            parts = ["0"] + parts
    coefs = []
    for k in range( len(parts)):
        part = parts[k]
        if k == len(parts) - 1 and part == "" :
            coefs.append("0")
        elif part in ["", "+"]:
            coefs.append( "1")
        elif part == "-":
            coefs.append( "-1")
        else:
            coefs.append(clean(part))
    return coefs

def polynome(coefs) :
    coefs = [clean(coef) for coef in coefs]
    n = len(coefs)
    poly = ""
    for k in range(n):
        p = n - 1 - k
        coef = coefs[k]
        poly += f"+{coef}x^{{{p}}}"
    return clean(poly.replace("x^{1}", "x").replace("x^{0}", "")).replace("times-", "times-1")

def deg(poly):
    if "x^" in poly:
        puissances = re.findall(r'x\^\{?(\d+)\}?', poly)
        return max([int(p) for p in puissances])
    elif "x" in poly:
        return 1
    else:
        return 0

def timespace(expr) :
    return expr.replace("\\times", "\\times  ")

def times2prod(expr) :
    expr = expr.replace("\\times", "\times").replace("\times", "*")
    return sympify(expr)

def nopar(expr) :
    return expr.replace("\\left(", "").replace("\\right)", "").replace("(", "").replace(")", "")

def remove_cancel(expr):
    return re.sub(r'\\Colcancel\[.*?\]\{(.*?)\}', r'\1', expr)
