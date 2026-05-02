from format import*

def factorisation(n):
    factors = factorint(n)
    prod = []
    for p, exp in factors.items() :
        prod += [f"{p}"]*exp
    return "\\times".join(prod)

def rasimp(n):
    racs = []
    factors = factorint(n)
    racs.append(rf"\sqrt{{{n}}}")
    if n == 1 :
        return racs + ["1"]
    outside = 1
    inside = 1
    for p, exp in factors.items() :
        outside *= p ** (exp // 2)
        inside *= p ** (exp % 2)
    if outside == 1 :
        return racs
    if inside == 1 :
        racs += [f"\sqrt{{{outside}^2}}"]
        racs += [f"{outside}"]
    else:
        racs += [f"\sqrt{{{outside}^2\\times {inside}}}"]
        racs += [rf"{outside}\sqrt{{{inside}}}"]
    return racs

def frasimp(num, den, sep = False, details = True) :
    fracs = []
    if den in [1, "1"] :
        return [f"{num}"]
    if den in [-1, "-1"] :
        return [f"\\dfrac{{{num}}}{{{den}}}", f"{-num}"]
    if num in [0, "0"] :
        return  [f"\\dfrac{{{num}}}{{{den}}}" ,  "0"]
    # if num == den :
    #     fracs += [ f"\\dfrac{{{num}}}{{{den}}}"]
    #     fracs += ["1"]
    #     return fracs
    if isinstance(num, str) :
        num, den = int(sympify(times2prod(num))), int(sympify(times2prod(den)))
    simp = Rational(num, den)
    if sep == True :
        return simp.numerator, simp.denominator
    if simp.denominator in [den, -den] or details == False :
        if simp.denominator == 1 :
            fracs += [f"{simp.numerator}"]
        elif simp.denominator == -1 :
            fracs += [f"-{simp.numerator}"]
        elif simp.numerator < 0 :
            fracs += [ f"-\\dfrac{{{-simp.numerator}}}{{{simp.denominator}}}"]
        else :
            fracs += [ f"\\dfrac{{{simp.numerator}}}{{{simp.denominator}}}"]
    else :
        # fracs += [ f"\\dfrac{{{num}}}{{{den}}}"]
        s = signe(num*den)
        num, den = abs(num), abs(den)
        if "-" in s :
            fracs += [s +f"\\dfrac{{{num}}}{{{den}}}"]
        else :
            s = ""
            fracs += [ f"\\dfrac{{{num}}}{{{den}}}"]
        simp = Rational(num, den)
        d = gcd(num, den)
        p = num/d
        q = den/d
        fracs +=  [s +"\\dfrac{{" + rf"\Colcancel[red]{{{d}}}" + "\\times " + parenthese(p) + "}}{{" + rf"\Colcancel[red]{{{d}}}" + "\\times " + parenthese(q) + "}}"]
        if num in [0, "0"] :
            fracs += ["0"]
        elif simp.denominator == 1 :
            fracs += [s +f"{simp.numerator}"]
        elif simp.denominator == -1 :
            fracs += [s + f"-{simp.numerator}"]
        else :
            fracs += [s + f"\\dfrac{{{simp.numerator}}}{{{simp.denominator}}}"]
    return nodouble(fracs)

def qfrac(num, den) :
    if "frac" in num :
        a, b = clean_frac(num)
    else :
        a, b = num, "1"
    if "frac" in den :
        c, d = clean_frac(den)
    else :
        c, d = den, "1"
    return frasimp(f"{a}\\times{d}",f"{b}\\times{c}")

def simp_simult(L, rev=False):
    n = max(len(f) for f in L)
    out = []
    for f in L:
        f = list(f)
        if rev:
            f = [f[0]] * (n - len(f)) + f
        else:
            f = f + [f[-1]] * (n - len(f))
        out.append(f)
    return out