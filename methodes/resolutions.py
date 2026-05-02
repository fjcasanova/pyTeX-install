from simplifications import*
from calcul import *

def sol1(eq, var = "x", details = True, fdet = True) :
    eq = clean(eq).replace(var, "x")
    gauche, droite = eq.split( "=")
    steps, gauche, droite = nofrac(eq)
    a, b = clean_coef(gauche, seps = ["x"])
    c, d = clean_coef(droite, seps = ["x"])
    if a == c == "0" and b != d :
        return   [", cette \\'equation n'admet pas de solution."] , ""
    steps += [clean(parentheses(f"{a}x - {c}x = {d} - {b}" ))]
    a, b, c, d = list(map(sympify, [a, b, c, d]))
    steps += [f" {a - c}x={d - b}"]
    if a - c == 0 :
        return [ " $ \Leftrightarrow" + steps[0] + "$"+ " ~ "] + [ r"~  $ \Leftrightarrow " + clean(steps[k]) + "$ " for k in range(1, len(steps))] +  ["Cette \\'equation n'admet donc pas de solution."] , ""
    elif a - c == -1 :
        steps += [clean(f"-(-x)=-{d - b}")]
        steps += [clean(f"x= {b - d}")]
    elif a - c != 1 :
        Fracs = frasimp(d - b, a - c, details = fdet)
        steps += [f"\\dfrac{{\\Colcancel[red]{{{a - c}}}x}}{{\\Colcancel[red]{{{a - c}}}}}=" + Fracs[0]]
        steps +=  ["x" + "".join([f"={frac}" for frac in Fracs ]).replace("==", "=")]
    steps = [clean(steps[k])  for k in range(len(steps) - 1) if clean(steps[k]).replace(" ", "")  != clean(steps[k+1]).replace(" ", "") ] + [steps[-1]]
    if details == True :
        return  nodouble([ r"  $ \Leftrightarrow " + clean(steps[k]).replace("x", var) + "$ "  for k in range(len(steps))]),  steps[-1].split("=")[-1].replace("$", "").replace("x", var)
    else :
        return  [  r"$ \Leftrightarrow " +clean( steps[-1]).replace("x", var) + "$ " ], steps[-1].split("=")[-1].replace("$", "").replace("x", var)

def prodeq(eq,  details = True) :
    try :
        eq1, eq2 = eq.split(')(')
        eq1 = clean(eq1).replace("(", " ")
        eq2 = clean(eq2).replace(")=0", "")
    except :
        eq1, eq2 = eq.split('(')
        eq1 = clean(eq1).replace("(", " ")
        eq2 = clean(eq2).replace(")=0", "")
    steps = ["$ \\Leftrightarrow " + clean(eq1) + " =0$ ou $" + clean(eq2) +" =0$" + r" \\"]
    steps1, x1 = sol1(eq1+"=0")
    steps2, x2 = sol1(eq2+"=0")
    steps2 = [step.replace("\\Leftrightarrow", "") for step in steps2]
    if x1 != "" :
        rep1 = rf"   ~  $ \Leftrightarrow x = {x1}$"
    else :
        rep1 = "cette \\'equation n'admet pas de solution."
    if x2 != "" :
        rep2 = rf"   ~  $  x = {x2}$"
    else :
        rep2 = "cette \\'equation n'admet pas de solution."
    while len(steps1) < len(steps2) :
        steps1.append(rep1)
    while len(steps1) > len(steps2) :
        steps2.append(rep2)
    for k in range(len(steps2)) :
        if "cette \\'equation n'admet pas de solution." in steps1[k] :
            steps += [ "$ \\Leftrightarrow $ " + steps2[k] +  r" \\"]
        elif "cette \\'equation n'admet pas de solution." in steps2[k] :
            steps += [ steps1[k] +  r" \\"]
        else :
            steps += [steps1[k] + " ~ ou ~ " + steps2[k] + r" \\"]
    return    steps , x1, x2

def sol2(eq) :
    eq = clean(eq)
    steps = [ ]
    seps = ["x^2", "x"]
    gauche, droite = eq.split("=")
    gcoefs = clean_coef(gauche)
    dcoefs = clean_coef(droite)
    if dcoefs != ["0", "0", "0"] :
        a1, b1, c1 = gcoefs
        a2, b2, c2 = dcoefs
        a1, b1, c1  = list(map(int, gcoefs))
        a2, b2, c2  = list(map(int, dcoefs))
        steps += [" $\\Leftrightarrow " + clean(f" {a1}x^2 + {b1}x + {c1}-{a2}x^2-{b2}x-{c2}=0$" )]
        a, b, c = a1 - a2, b1 - b2, c1 - c2
        steps += [" $\\Leftrightarrow " + parentheses(clean(f" {a}x^2+{b}x+{c}=0$ "))]
    else :
        a, b, c = gcoefs
        a, b, c = list(map(int, gcoefs))
    pgcd = gcd(gcd(a,b),c)
    if pgcd != 1 :
        a, b, c = a//pgcd, b//pgcd, c//pgcd
        steps += [f"$\\Leftrightarrow {pgcd}\\times ("+ parentheses(clean(f" {a}x^2+{b}x+{c}=0")) + ") \\Leftrightarrow "+ parentheses(clean(f" {a}x^2+{b}x+{c}=0$"))]
    ant = [-2,-1,1,2]
    ims = [a*k**2 + b*k + c for k in ant]
    if b == 0 :
        if c == 0 :
            steps += [" $\\Leftrightarrow x^2 = 0 \\Leftrightarrow x= 0$ "]
            return steps , "0", ""
        sols, _ =  sol1(f" {a}x+{c}=0", var = "x^2")
        steps += sols
        if -c/a < 0 :
            steps += ["$< 0$ { donc cette \\'equation n'admet pas de solution. }"]
            return steps, "", ""
        else :
            steps +=  [ " \\\\\n $\\Leftrightarrow x "]
            steprac = ""
            if sympify(rf"{-c}/{a}").is_integer :
                Racs = rasimp(sympify(rf"{-c}/{a}"))
                for rac in Racs :
                    steprac += "=" + rac
                x1 =  Racs[-1]
            else :
                num, den = frasimp(-c, a, sep = True)
                x1 = latex(Rational(num, den)).replace("frac", "dfrac")
                x1 = rf"\sqrt{{{x1}}}"
                steps += ["=" + x1 ]
                nRacs = rasimp(num)
                dRacs = rasimp(den)
                while len(nRacs) < len(dRacs) :
                    nRacs.append(nRacs[-1])
                while len(nRacs) > len(dRacs) :
                    dRacs.append(dRacs[-1])
                if len(dRacs) < 2 :
                    pass
                else :
                    for k in range(len(dRacs)) :
                        nr = nRacs[k]
                        dr = dRacs[k]
                        steprac +=  "=" + rf"\dfrac{{{nr}}}{{{dr}}}"
                    x1 = rf"\dfrac{{{nr}}}{{{dr}}}"
            x2 = "-" + x1
            steps += [steprac + "$ ou  $x= " + x2 + "$"]
            x1, x2 = x2, x1
    elif c == 0 :
        steps += [rf" $ \Leftrightarrow x(" + clean(rf"{a}x+{b}") +r")=0$ \\"]
        sols, x1, x2 =  prodeq(f" x({a}x+{b})=0")
        steps += sols
    elif 0 in ims :
        x1 = [ant[k] for k in range(len(ims)) if ims[k] == 0 ][0]
        steps += [f"\\\\\n $x_1={x1}$ est une racine \\'evidente de $" + clean(f"{a}x^2+{b}x+{c}") + "$, de plus : \\\\\n"]
        x2 = [clean(f"$x_1x_2={x1}x_2") + "=\\dfrac{c}{a}"] + ["=" + "=".join(frasimp(c,a)) + "\Leftrightarrow x_2 "]
        Fracs = frasimp(c, a*x1)
        if x1 == 1 :
            steps += x2 + ["=" + Fracs[-1]  + "$ \\\\\n"]
        else :
            steps += x2 + ["=" + "=".join(Fracs)  + "$ \\\\\n"]
        x1, x2 = rf"{x1}", Fracs[-1]
        if a < 0 :
            x1, x2 = x2, x1
    else :
        D = int(b**2 - 4*a*c)
        racine_D = sqrt(D)
        pa, pb, pc = (parenthese(k) for k in [a,b,c])
        steps += ["\\\\\n On reconna\\^it une \\'equation du second degr\\'e de discriminant : \\\\\n"]
        steps += [f"$\\Delta = b^2-4ac="]
        steps +=  [pb + "^2-4\\times " +  pa + "\\times "  + pc + f"= {latex(D)}"]
        if D < 0:
            steps += ["< 0$, il n'y a donc pas de racine dans $\\mathbb{R}$."]
            x1, x2 = "", ""
        elif D > 0:
            steps += ["> 0$, il y a donc deux racines distinctes :\\\\\n"]
            steps += [f"$x_1=\\dfrac{{-b-\\sqrt{{\\Delta}}}}{{2a}}"]
            steps += [f"=\\dfrac{{-{pb}-\\sqrt{{{D}}}}}{{2\\times {pa}}}"]
            calculs, x1, x2 = calcul_racines(a, b, D)
            steps += calculs
        else :
            steps += [r" $, il y a donc une  racine double : \\"]
            x0 = rf"$x_0 = \dfrac{{-b}}{{2a}}"
            Fracs = frasimp(-b, 2*a)
            for f in Fracs :
                x0 += rf"={f}"
            x0 += "$"
            steps += [x0]
            x1, x2 = rf"{f}", rf"{f}"
    steps = [steps[k] for k in range(len(steps) - 1) if clean(steps[k]).replace(" ", "")  != clean(steps[k+1]).replace(" ", "") ] + [steps[-1]]
    return nodouble(steps) + [" \n"], x1, x2