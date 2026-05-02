import re
from calcul import *

def variations2deg(a, alpha, beta) :
    steps = []
    steps += [rf"$a={a}"]
    if a > 0 :
        steps += [">0$, on en déduit le tableau de variations suivant : "]
        steps += ["\\begin{center}\\begin{tikzpicture}[yscale=1]\n"]
        steps += ["\\tkzTabInit[lgt=2.4,espcl=4]{$x$ / 1 ,  Variations de $f$/2}"]
        steps += ["{" + f"$-\\infty$, ${alpha}$, $+\\infty$" + "}"]
        steps += ["\\tkzTabVar{+/, -/$" + f"{beta}$ , +/" + "}"]
        steps += ["\\end{tikzpicture}\\end{center}"]
    elif a < 0 :
        steps += ["< 0$, on en déduit le tableau de variations suivant : "]
        steps += ["\\begin{center}\\begin{tikzpicture}[yscale=1]\n"]
        steps += ["\\tkzTabInit[lgt=2.4,espcl=4]{$x$ / 1 ,  Variations de $f$/2}"]
        steps += ["{" + f"$-\\infty$, ${alpha}$, $+\\infty$" + "}"]
        steps += ["\\tkzTabVar{-/, +/$" + f"{beta}$ , -/" + "}"]
        steps += ["\\end{tikzpicture}\\end{center}"]
    return steps

def signeaff(expr, nodef = []) :
    mstr, pstr = clean_coef(expr, ["x"])
    mstr, pstr = clean(mstr), clean(pstr)
    m,p = latex2sympy(mstr), latex2sympy(pstr)
    steps = []
    signes = ","
    if m != 0 :
        steps += [f"\\\\\n $x \\mapsto " + clean(f"{expr}")+ f"$ est une fonction affine de coefficient directeur $m={mstr}"]
        if m > 0 :
            steps += [">0$, on en déduit le tableau  suivant : "]
        else :
            steps += ["<0$, on en déduit le tableau  suivant : "]
        try :
            zeros = [frasimp(-p, m)[-1]]
        except :
            zeros = [qfrac("-" + pstr, mstr)[-1]]
        signes += signe(-m) + ","
        antecedents = {x: "z" for x in zeros if x != ""}
        antecedents.update({n: "d" for n in nodef if n != ""})
        antecedents = sorted( [(x, t) for x, t in antecedents.items()], key=lambda ant: latex2sympy(ant[0]))
        for k in range(len(antecedents)) :
            ant = antecedents[k]
            signes += f"{ant[1]},"
            if ant[0] in zeros and ant[0] in nodef :
                signes += rsignes("-"+ signes[-4])+ ","
            elif ant[1] == "z" :
                signes += rsignes("-"+ signes[-4]) + ","
            elif ant[1] == "d" :
                signes += signes[-4]+ ","
    else :
        # print(p)
        if p < 0 :
            steps += [f"$f(x)={expr}<0$, d'où le tableau suivant : "]
        elif p > 0 :
            steps += [f"$f(x)={expr}>0$, d'où le tableau suivant : "]
        signes += signe(p) + ","
        for _ in nodef :
            signes += "d," + signe(p) + ","
        antecedents = nodef
    steps += ["\\begin{center}\\begin{tikzpicture}[yscale=1]\n"]
    steps += ["\\tkzTabInit[lgt=3,espcl=2.5]{$x$ / 1 ,  Signe de $" + expr + "$/2}"]
    steps += ["{" + f"$-\\infty$," + ",".join([f"${ant[0]}$" for ant in antecedents]) + ", $+\\infty$" + "}"]
    steps += ["\\tkzTabLine{ " + signes + " }"]
    steps += ["\\end{tikzpicture}\\end{center}"]
    return steps

def signe2deg(a, x1, x2, nodef = []) :
    zeros = [x for x in [x1, x2] if x != ""]
    steps = []
    if a > 0 :
        s = "+"
        pos = "> 0"
    elif a < 0 :
        s = "-"
        pos = "< 0"
    antecedents = []
    signes = ","
    if zeros + nodef != [] :
        antecedents = {x: "z" for x in zeros if x != ""}
        antecedents.update({n: "d" for n in nodef if n != ""})
        antecedents = sorted( [(x, t) for x, t in antecedents.items()], key=lambda ant: latex2sympy(ant[0]))
        signes += s + ","
        for k in range(len(antecedents)) :
            ant = antecedents[k]
            signes += f"{ant[1]},"
            if ant[0] in zeros and ant[0] in nodef :
                if x2 == "" :
                    signes += signes[-4] + ","
                else :
                    signes +=  rsignes("-"+ signes[-4]) + ","
            elif ant[1] == "z" and x1 != x2 :
                signes += rsignes("-"+ signes[-4]) + ","
            elif ant[1] == "z" and x1 == x2 :
                signes += signes[-4] + ","
            elif ant[1] == "d" :
                signes +=  signes[-4]+ ","
    if x1 == "" :
        steps += [f"$f$ n'admet pas de racine, donc est du signe de $a={a}{pos}$, d'où le tableau suivant : "]
        # signes = f", ,{s},"
    elif x2 == x1 :
        steps += [f"$a={a}{pos}$, d'où le tableau  suivant : "]
        # signes = f",{s},z,{s},"
        # signes = signes.replace("+,z,-", "+,z,+", 1).replace("-,z,+", "-,z,-", 1)
    else :
        steps += [f"$a={a}{pos}$, on en déduit le tableau suivant : "]
    steps += ["\\begin{center}\\begin{tikzpicture}[yscale=1]\n"]
    steps += ["\\tkzTabInit[lgt=3,espcl=2.5]{$x$ / 1 ,  Signe de $f(x)$/2}"]
    steps += ["{" + f"$-\\infty$," + ",".join([f"${ant[0]}$" for ant in antecedents]) + ", $+\\infty$" + "}"]
    steps += ["\\tkzTabLine{ " + signes + " }"]
    steps += ["\\end{tikzpicture}\\end{center}"]
    return steps

def signe2var(tableau, expr, nodef = []) :
    variations = tableau.copy()
    variations[-4] = variations[-4].replace("f(x)", "f'(x)")
    variations[-4] = variations[-4].replace("}", ", Variations de $f$/3 }")
    ants = variations[-3].replace(" ", "").replace("{$-\infty$,", "").replace(",$+\infty$}", "").replace("$", "")
    ants = ants.split(",")
    ants = {x: "z" for x in ants if x!= ""}
    ants.update({n: "d" for n in nodef if n!= ""} )
    ants = sorted([(x, t) for x, t in ants.items()],key=lambda ant: latex2sympy(ant[0]))
    signes = variations[-2].replace("\\tkzTabLine{", "").replace("}", "")
    signes = signes.split(",")
    signes = "".join(signes).replace(" ", "")
    signes = signes.split("d")
    if ants != [] :
        calc_img = [(x[0],image(expr, latex2sympy(x[0]))) for x in ants if x[1] == "z" ]
        ims =  ["$ " + img[1][-1] + " $" for img in calc_img if img[1] != [""]]
    else :
        calc_img = [""]
        ims = [""]
    vars = ""
    for signe in signes :
        if signe == "" :
            pass
        elif signe[0] == "-" :
            signe = "+" + signe
        elif signe[0] == "+" :
            signe = "-" + signe
        for j in range(len(signe)) :
            s = signe[j]
            if s == "+" : vars += ",+/"
            elif s == "-" : vars += ",-/"
            elif s == "z" : vars += "image"
        vars += "D/"
    vars = vars.replace("+/D/,-/", "+D-/").replace("+/D/,+/", "+D+/").replace("-/D/,-/", "-D-/").replace("-/D/,+/", "-D+/")
    vars = vars.replace("+/image,+/", "R/image,+/").replace("-/image,-/", "R/image,-/")
    vars = vars[1:].split("image")
    add_ims = []
    for j, val in enumerate(ims) :
        v = vars[j]
        if "R/" in v :
            v = v.replace("image", "")
            add_ims.append("\\tkzTabIma" + f"{{{j+1}}}{{{j+3}}}{{{j+2}}}{{{ims[j]}}}")
        else :
            vars[j] += val
    vars = "".join(vars)
    vars = vars.replace("/D/", "/")
    variations.insert(-1, "\\tkzTabVar{" + vars + "}")
    for add_im in add_ims :
        variations.insert(-1, add_im)
    for k in range(len(calc_img)) :
        ant, calc_ant = calc_img[k]
        if ant[0] != "" :
            variations += [rf"$f\left({ant}\right)=" + "=".join(calc_ant) +"$ \\\\\n"]
    return variations