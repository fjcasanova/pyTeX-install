from format import *
from calcul import*
from resolutions import*

def derivee(expr) :
    if "dfrac" in expr :
        return ratder(expr)
    else :
        return dpoly

def dpoly(poly):
    poly = poly.replace(" ", "")
    monomes = re.findall(r'[+-]?[^+-]+', poly)
    der = []
    for mon in monomes:
        if "x" not in mon:
            der.append("0")
        elif "x^" in mon:
            coef, puissance = mon.split("x^")
            if coef == "" or coef == "+":
                coef = 1
            elif coef == "-":
                coef = -1
            else:
                coef = int(nopar(coef))
            if "{" in puissance :
                puissance = puissance.replace("{", "")
                puissance = puissance.replace("}", "")
            puissance = int(puissance)
            coef = coef * puissance
            puissance = puissance - 1
            if puissance == 1:
                der.append(f"{coef}x")
            elif puissance == 0:
                der.append(f"{coef}")
            else:
                der.append(f"{coef}x^{puissance}")
        else:
            coef = mon.replace("x", "")
            if coef in ["", "+"]:
                coef = 1
            elif coef == "-":
                coef = -1
            else:
                coef = int(nopar(coef))
            der.append(str(coef))
    return clean("+".join(der))


def ratder(f) :
    u, v = clean_frac(f)
    if "x" in u :
        df = [rf" $f=\dfrac{{u}}{{v}}$ avec $u(x)={u}$ et $v(x)={v}$. \\ "]
    else :
        df = [rf" $f=k\times \dfrac{1}{{v}}$ avec $k={u}$ constant et $v(x)={v}$. \\ "]
    Df = r"\R"
    if "x^2" in v :
        sols, x1, x2 = sol2(f"{v}=0")
        df += [rf"De plus : $v(x)=0\Leftrightarrow {v}=0$ "] + [step.replace("\\\\n", "") for step in sols]
        if x1 == "" or x2 == "" or x1 == x2 :
            r = x1 + x2
            r = r.replace(f"{x1}{x2}", f"{x1}")
        else :
            r = f"{x1};{x2}"
    else :
        sols, r = sol1(f"{v}=0", fdet = False)
        df += ["De plus : $v(x)=0\Leftrightarrow {v}=0$"] + [step.replace("\\\\n", "") for step in sols]
    if r.replace(" ",  "") != "" :
        r = r.replace("\\dfrac", "\\frac")
        Df = r"\R\setminus\left\{" rf"{r}"+ r"\right\}"
    df += [rf"\\ Par conséquent $f$ est définie sur ${Df}$. \\ "]
    if "x" in u :
        du, dv = dpoly(u), dpoly(v)
        df += ["Or, $u$ et $v$ sont dérivable sur $\\R$ avec : "]
        df += [rf"$u'(x)={du}$ et $v'(x)={dv}$.  " ]
        df += [rf"\\  Ainsi $f$ est définie et dérivable sur ${Df}$, et pour tout $x$ dans cet ensemble : \\ "]
        u, v = clean( rf"({u})"), clean( rf"({v})")
        du, dv = clean( rf"({du})"), clean( rf"({dv})")
        df += [r"$f'(x)=\left(\dfrac{u}{v}\right)'(x)=\left(\dfrac{u'v-uv'}{v^2}\right)(x)$ \\"]
        num = clean(rf"{du}\times {v} - {u}\times {dv}")
        df += [  rf"$f'(x)=\dfrac{{{num}}}{{{v}^2}}$ \\"]
        num = latex(polyprod(du, v)) + "- (" + latex(polyprod(u, dv)) + ")"
        df += [  rf"$f'(x)=\dfrac{{{num}}}{{{v}^2}}"]
        num = polyprod(du, v) - polyprod(u, dv)
        num = orderpoly(num).replace("\\times", "")
        df += [  rf"=\dfrac{{{num}}}{{{v}^2}}"]
        a,b,c = clean_coef(num)
        if "0" not in [a,b,c] and "x^2" in num:
            a,b,c = int(a), int(b), int(c)
            pgcd = gcd(gcd(a, b), c)
            if pgcd not in [0,1] :
                a,b,c = a//pgcd, b//pgcd, c//pgcd
                num = clean(f"{a}x^2+{b}x+{c}")
                num = f"{pgcd}({num})"
                df += [  rf"$ \\ $f'(x)"]
                df += [  rf"=\dfrac{{{num}}}{{{v}^2}}"]
    else :
        dv = dpoly(v)
        df += [rf"Or, $v$ est dérivable sur $\R$ avec :   $v'(x)={dv}$.  " ]
        df += [rf"\\  Ainsi $f$ est définie et dérivable sur ${Df}$, et pour tout $x$ de ${Df}$ : \\ "]
        v = clean( rf"({v})")
        dv = clean( rf"({dv})")
        df += [r"$f'(x)=\left(k\times \dfrac{1}{v}\right)'(x)=k\times \left(\dfrac{-v'}{v^2}\right)(x)$ \\"]
        num = clean(rf"-{dv}")
        df += [  rf"$f'(x)={u}\times \dfrac{{{num}}}{{{v}^2}} "]
        num = polyprod(u, "-" + dv)
        num = orderpoly(num).replace("\\times", "")
        df += [  rf"$ \\ $f'(x)"]
        df += [  rf"=\dfrac{{{num}}}{{{v}^2}}"]
    df += [" $ "]
    return df, Df

def dexp(f) :
    df = []
    u,v = f.split("e^{")
    u, v = nopar(u), v[:-1]
    du, dv = clean(dpoly(u)), clean(dpoly(v))
    a, b = clean_coef(v, seps = ["x"])
    df += [f"$f=u\\times v$ avec $u={u}$ et $v=e^{{ax+b}}$ où $a={a}$ et $b={clean(b)}$\\"]
    df += ["Or, $u$ et $v$ sont dérivable sur $\\R$ avec : "]
    df += [f"$u'(x)={du}$ et $v'(x)={a}\\times e^{{{a}x+{b}}}=" +clean(f"{dv}e^{{{v}}}") + "$.  " ]
    df += [rf"\\  Ainsi $f$ est définie et dérivable sur $\R$, et pour tout réel $x$ : \\ "]
    df += [rf"$f'(x)=\left(uv\right)'(x)=\left(u'v+uv'\right)(x)=" + clean(f"({du})e^{{{v}}}+({u})\\times {dv}e^{{{v}}}").replace("\\timese", "\\times e") + r"$ \\"]
    df += [rf"$f'(x)=({du}+" + latex(polyprod(u, dv)) + f")e^{{{v}}}="]
    df += ["(" + latex(polyprod(du, "1") + polyprod(u, dv))  + rf")e^{{{v}}}"]
    df += [r"$ \\"]
    return df, "\\R"
