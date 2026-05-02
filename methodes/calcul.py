from simplifications import*
from sympy.parsing.sympy_parser import (parse_expr, standard_transformations, implicit_multiplication_application)

def splitpoly(poly) :
    poly = poly.replace(" ", "")
    monomes = re.findall(r'[+-]?[^+-]+', poly)
    return monomes

def fonction(expr) :
    x = symbols('x')
    transformations = standard_transformations + (implicit_multiplication_application,)
    expr = re.sub(r"\\dfrac\s*\{([^{}]+)\}\s*\{([^{}]+)\}", r"(\1)/(\2)", expr)
    expr = expr.replace("^", "**")
    expr = expr.replace("{" , "")
    expr = expr.replace("}" , "")
    expr = parse_expr(expr, transformations=transformations)
    f = lambdify(x, expr, "math")
    return f

def splitfracs(exprs) :
    sep = []
    for expr in exprs:
        expr = expr.replace("\\frac", "\\dfrac")
        parts = re.split(r'(\\dfrac\{|}\{|})', expr)
        parts = [p for p in parts if p != ""]
        sep.extend(parts)
    return sep

def image(expr, x, val = False) :
    steps = []
    if "frac" in expr :
        num, den = clean_frac(expr)
        nums, dens = polyimg(num, x), polyimg(den, x)
        nums, dens = simp_simult([nums, dens])
        steps += [f"\dfrac{{{nums[k]}}}{{{dens[k]}}}" for k in range(len(nums))]
        num, den = nums[-1], dens[-1]
        num, den = latex2sympy(num), latex2sympy(den)
        if val == True :
            return eval(num)/eval(den)
        # if "frac" in num :
        #     nums = sfrac(num)
        # if "frac" in dens :
        #     dens = sfrac(den)
        steps += [f"{f}" for f in frasimp(num, den)]
    elif "e^" in expr :
        poly, puiss = expr.split("e^{")
        poly, puiss = nopar(poly), puiss.replace("}", "")
        poly, puiss = polyimg(poly, x), polyimg(puiss, x)
        poly, puiss =  simp_simult([poly, puiss])
        if puiss[-1] == "0" and poly[-1] == "1":
            pass
        elif poly[-1] in ["-1", "1"] :
            poly[-1] = poly[-1].replace("1", "")
        steps += [f"({poly[k]})e^{{{puiss[k]}}}".replace("e^{0}", "\\times 1").replace("e^{1}", "e") for k in range(len(poly)-1)]
        if poly[-1] == "0" :
            steps += [nopar(f"0\\times e^{{{puiss[-1]}}}".replace("e^{0}", "").replace("e^{1}", "e"))]
            steps += ["0"]
        else :
            steps += [nopar(f"({poly[-1]})e^{{{puiss[-1]}}}".replace("e^{0}", "").replace("e^{1}", "e"))]
    else :
        if val == True :
            return eval(polyimg(expr, x)[-1])
        steps +=  polyimg(expr, x)
    return nodouble(steps)

def polyimg(expr, x) :
    img = []
    x = f"{x}"
    expr = re.sub(r'([\d}])x', r'\1\\timesx', expr)
    if latex2sympy(str(x)) < 0 or "frac" in x :
        expr = expr.replace("x^", "\\left(x\\right)^")
        expr = expr.replace("\\timesx", "\\times\\left(x\\right)")
        expr = expr.replace("-x", "-\\left(x\\right)")
    img += [clean(parentheses(expr.replace("x", x)))]
    expr = expr[0] + expr[1:].replace("-", "+-").replace("++", "+")
    termes = simp_simult([pfrac(frac.replace("x", x)) for frac in expr.split("+")])
    for k in range(len(termes[0])) :
        img += [clean("+".join([p[k] for p in termes]))]
    img += sfrac(img[-1].replace("=", ""))
    return nodouble(img)

def sfrac(fracsum) :
    somme = [fracsum]
    fracsum = fracsum.replace("-", "+-").replace("++", "+")
    if fracsum[0] == "+" :
        fracsum = fracsum[1:]
    fraclist = fracsum.split("+")
    if len(fraclist) < 2 :
        return somme
    fraclist = [frac2sympy(frac) for frac in fraclist]
    numlist = []
    denlist = []
    for frac in fraclist :
        num, den = frac
        numlist.append(num)
        denlist.append(den)
    if all(den == 1 for den in denlist) :
        fracsum = fracsum.replace("\\times", "*")
        return somme + [str(eval(fracsum))]
    ppcm = denlist[0]
    for m in denlist[1:] :
        ppcm = ilcm(m,ppcm)
    multlist = [ppcm/den for den in denlist]
    valnum = ""
    valden = ppcm
    s = ""
    for k in range(len(fraclist)) :
        num = numlist[k]
        den = denlist[k]
        mult = multlist[k]
        valnum += f"{num*mult}+"
        if mult != 1 :
            num = f" {num}\\times {mult}"
            den = f" {den}\\times {mult}"
        s += rf"\dfrac{{{num}}}{{{den}}} +"
        s = clean(s).replace("1\\times", "")
    valnum = clean(valnum[:-1])
    somme += [s[:-1]]
    somme += [rf"\dfrac{{{valnum}}}{{{valden}}}"]
    valnum = eval(valnum)
    somme += frasimp(valnum, valden)
    return somme

def pfrac(fracprod) :
    fraclist = fracprod.split("\\times")
    fraclist = [frac2sympy(frac) for frac in fraclist]
    nums = []
    dens = []
    for frac in fraclist:
        n, d = frac
        if n == 0 :
            return [fracprod, "0"]
        if n != 1 :
            nums.append(f"{n}")
        if d != 1 :
            dens.append(f"{d}")
    num, den = "\\times ".join(nums), "\\times ".join(dens)
    num, den = num.replace(r"-\\times ", "-"), den.replace(r"-\times ", "-")
    num, den = parentheses(num), parentheses(den)
    if num.replace(" ", "") == "" :
        num = "1"
    if den.replace(" ", "") == "" :
        num = num.replace("\\times", "*")
        return [fracprod,  str(eval(rf"{num}"))]
    fracs = frasimp(num, den)
    if len(fracs) > 1 :
        prod = [fracprod] + frasimp(num, den)[1:]
    else :
        prod = [fracprod] + frasimp(num, den)
    # num, den = eval(num.replace("\\times", "*")), eval(den.replace("\\times", "*"))
    # prod += rf"=\dfrac{{{num}}}{{{den}}}"
    return nodouble(prod)

def nofrac(eq, vars= ["x", ""]):
    steps = []
    gauche, droite = eq.split("=")
    deg = len(vars)
    G, D = get_fcoefs(gauche, deg), get_fcoefs(droite, deg)
    sympcoef = [latex2sympy(coef) for coef in G + D]
    if any(denom(coef) != 1 for coef in sympcoef):
        ppcm = 1
        factors = []
        for coef in sympcoef:
            if ilcm(ppcm, int(denom(coef)))//ppcm != 1 :
                factors.append(f"{ilcm(ppcm, int(denom(coef)))//ppcm}")
            ppcm = ilcm(ppcm, int(denom(coef)))
        ppcm_prod = "\\times".join(factors)
        gauche = f"{ppcm_prod}\\times\\left({gauche}\\right)" if all(c != "0" for c in G) else f"{ppcm_prod}\\times {gauche}"
        droite = f"{ppcm_prod}\\times\\left({droite}\\right)" if all(c != "0" for c in D) else f"{ppcm_prod}\\times {droite}"
        steps += [clean(gauche) + "=" + clean(droite)]
        gauche = distrib(f"{ppcm_prod}", gauche.replace(f"{ppcm_prod}\\times\\left(", "").replace("\\right)", "").replace(f"{ppcm_prod}\\times " , ""))
        droite =  distrib(f"{ppcm_prod}", droite.replace(f"{ppcm_prod}\\times\\left(", "").replace("\\right)", "").replace(f"{ppcm_prod}\\times " , ""))
        # steps += [gauche + "=" + droite]
        G, D = get_fcoefs(gauche, deg), get_fcoefs(droite, deg)
        for membre in [G, D] :
            for k in range(len(membre)) :
                terme = membre[k]
                if "frac" in terme :
                    ng, dg, _ = terme.split("}")
                    deng = dg.replace("{", "")
                    pgcd = gcd(sympify("*".join(ng.split("\\times")[:-1])), int(deng))
                    fact = (([""] + ng.split("\\times"))[:-1])[1:]
                    fact1 = "\\times".join(fact)
                    fact = int(sympify("*".join(fact)))//pgcd
                    if fact != 1 :
                        ng = ng.replace(f"{fact1}", f"{pgcd}\\times{fact}").replace("\\times\\times", "\\times")
                    else :
                        ng = ng.replace(f"{fact1}", f"{pgcd}").replace("\\times\\times", "\\times")
                    if deng in ng :
                        ng, dg = ng.replace(f"{deng}", rf"\Colcancel[red]{{{deng}}}", 1), dg.replace(f"{deng}", rf"\Colcancel[red]{{{deng}}}", 1)
                    else :
                        if int(deng)//pgcd != 1 :
                            dg = dg.replace(f"{deng}", f"{pgcd}\\times {int(deng)//pgcd}")
                        ng, dg = ng.replace(f"{pgcd}", rf"\Colcancel[red]{{{pgcd}}}", 1), dg.replace(f"{pgcd}", rf"\Colcancel[red]{{{pgcd}}}", 1)
                    membre[k] = "}".join([ng, dg, _])
                elif terme != "0" :
                    prod = terme.split("\\times")
                    # prod.remove("")
                    fact = int(sympify("*".join(prod) if prod else "1"))
                    # print(prod, fact)
                    membre[k]  = terme.replace(f"{terme}", f"{fact}").replace("\\times\\times", "\\times")
        gauche, droite = polynome(G), polynome(D)
        steps += [clean(gauche) + "=" + clean(droite)]
        G, D = get_fcoefs(remove_cancel(gauche), deg), get_fcoefs(remove_cancel(droite), deg)
        for membre in [G, D] :
            for k in range(len(membre)) :
                coef = membre[k]
                n, den = frac2sympy(pfrac(coef + " ")[-1])
                membre[k] = ([""] + frasimp(n, den))[-1]
        gauche, droite = polynome(G), polynome(D)
        steps += [clean(gauche) + "=" + clean(droite)]
    return steps, gauche, droite

def polyprod(P, Q = "1", var = "x") :
    P = P.replace("\\times", "*")
    Q = Q.replace("\\times", "*")
    nomult = r'(-?\d+)(x)'
    while re.search(nomult, P):
        P = re.sub(nomult, lambda m: m.group(1) + "*" + m.group(2) , P)
    while re.search(nomult, Q):
        Q = re.sub(nomult, lambda m: m.group(1) + "*" + m.group(2) , Q)
    x = symbols(var)
    P = sympify(P)
    Q = sympify(Q)
    return expand(P*Q)

def orderpoly(P, x = symbols("x")) :
    orderP = []
    for p, c in Poly(P, x).terms() :
        orderP += [str(c*x**p[0])]
    return clean("+".join(orderP))

def distrib(k, P):
    coefs_P = get_coefs(P)
    new_coefs = []
    for p in coefs_P:
        if p == "0":
            new_coefs.append("0")
        elif p in ["1", "+1"]:
            new_coefs.append(f"{k}")
        elif p == "-1":
            new_coefs.append(f"-{k}")
        else:
            new_coefs.append(f"{k}\\times {p}")
    return polynome(new_coefs)

def canonique(P) :
    a, b, c = clean_coef(P, seps = ["x^2", "x"])
    a, b, c = list(map(int, [a, b, c]))
    if b == 0 :
        return [f"$f(x)$ est déjà sous forme canonique avec $\\alpha=0$ et $\\beta={c}$."], "0", f"{c}"
    pa, pb, pc = (parenthese(k) for k in [a,b,c])
    steps = [r"$\alpha = -\dfrac{b}{2a} " + rf"= -\dfrac{{{pb}}}{{2\times {pa}}}"]
    Fracs = frasimp(-b, 2*a)
    if len(Fracs) > 2 :
        Fracs = Fracs[len(Fracs)-2:]
    for frac in Fracs :
        steps += ["=" + frac]
    alpha = steps[-1].replace("=", "")
    if Rational(-b, 2*a) < 0 :
        beta = rf"{a}\times \left({alpha}\right)^2 +    {b}\times \left({alpha}\right) + {c} "
    elif "frac" in steps[-1] :
        beta = rf"{a}\times \left({alpha}\right)^2 +    {b}\times {alpha} + {c} "
    else :
        beta = rf"{a}\times {alpha}^2 +    {b}\times {alpha} + {c} "
    steps += [ r"$ \\"]
    steps += [rf"$\beta = f(\alpha)=f\left({alpha}\right)=" + clean(beta) + r"$ \\"]
    alpha_s = sympify(f"-Rational(-{b},2*{a})")
    # steps += [ clean(rf"$\beta =" + latex(a*Rational(-b,2*a)**2) + "+" +latex(b*Rational(-b,2*a))+f" +{c}").replace("\frac", "\dfrac") +"$ "]
    if not alpha_s.is_integer :
        steps += [r"\\ $\beta="]
        steps += [ "=".join(polyimg(P, alpha)[2:]) + r"$ \\"]
    beta = expand(a*Rational(-b,2*a)**2 + b*Rational(-b,2*a) + c)
    beta = latex(beta).replace("frac", "dfrac")
    # steps += [rf"= {beta}$ \\"]
    steps = [steps[k] for k in range(len(steps) - 1) if clean(steps[k]).replace(" ", "")  != clean(steps[k+1]).replace(" ", "") ] + [steps[-1]]
    steps += [rf"Par conséquent, la forme canonique recherchée est : $f(x)=a(x-\alpha)^2+\beta =" +clean(rf"{a}\left(") + latex(sympify(f"x -Rational(-{b},2*{a})")).replace("frac", "dfrac") + clean(rf"\right)^2+{beta}$.")]
    # steps += image(P, alpha)
    return nodouble(steps), alpha, beta

def calcul_racines(a,b, D) :
    steps = []
    Racs = rasimp(D)
    den = 2 * int(a)
    steps += [f"=\\dfrac{{{-b}-{rac}}}{{{den}}}" for rac in Racs[1:]]
    num1, num2 = f"{-b}", f"{Racs[-1]}"
    num = f"{num1}-{num2}"
    steps += [f"=\\dfrac{{{num}}}{{{den}}}"]
    if "sqrt" not in num :
        Fracs = frasimp(eval(f"{-b}-{Racs[-1]}"), den)
        steps += nodouble([f"={frac}" for frac in Fracs])
        x1 = Fracs[-1]
        num = f"{num1}+{num2}"
        Fracs = frasimp(eval(f"{-b}+{Racs[-1]}"), den)
        steps += ["$ \\\\\n Et  $x_2" + f"=\\dfrac{{{num}}}{{{den}}}=" + "=".join(Fracs)  + "$"]
        x2 = Fracs[-1]
    else :
        k, rac = num2.split("\\sqrt")
        rac = "\\sqrt" + rac
        if k == "" :
            k = 1
        frac1, frac2 = simp_simult([frasimp(eval(num1), den), frasimp(abs(eval(f"{k}")), abs(den))], rev = True)
        simplifications = []
        for j in range(len(frac1)) :
            if j == 2 :
                simplifications += [" $ \\\\\n $x_1 "]
            n1, d1 = clean_frac(frac1[j], times =False)
            n2, d2 = clean_frac(frac2[j], times = False)
            n2 = f" {n2}{rac}".replace("\\times 1\\sqrt", "\\times\\sqrt").replace("-1\\sqrt", "-\\sqrt").replace(" 1\\sqrt", "\\sqrt")
            n1, n2 = clean(n1), clean(n2)
            if clean_frac(frac1[-1])[1] == clean_frac(frac2[-1])[1] :
                num = rsignes(rf"{n1}\pm{n2}")
                if d1 != "1" :
                    simplifications += [r"=\dfrac{" + num + "}{" + f"{d1}" + "}"]
                else :
                    simplifications += [r"=" + rf"{num}"]
            else :
                f2 = rf"\pm\dfrac{{{n2}}}{{{d2}}}"
                if not (d1 == "1" or d2 == "1"):
                    simplifications += [rf"=\dfrac{{{n1}}}{{{d1}}}" + f2]
                elif d1 == "1" :
                    simplifications += [rf"={{{n1}}}" + f2]
                else :
                    simplifications += [rf"=\dfrac{{{n1}}}{{{d1}}}\pm{n2}"]
        x1 = simplifications[-1].replace("=","")
        s = signe(a)
        x1, x2 = rsignes(x1.replace(r"\pm", rsignes(f"-{s}"))), rsignes(x1.replace(r"\pm", f"{s}"))
        steps += [rsignes(simp.replace(r"\pm", rsignes(f"-{s}"))) for simp in simplifications]
        steps += [f" $ et  $x_2={x2}$ "]
    return nodouble(steps), x1, x2