from calcul import*
from latex2sympy2 import latex2sympy

def droite(expr, xmax, ymax=None):
    mstr, pstr = clean_coef(expr, ["x"])
    mstr, pstr = clean(mstr), clean(pstr)
    m,p = latex2sympy(mstr), latex2sympy(pstr)
    if ymax is None:
        ymax = xmax
    expr = expr.replace(mstr,"("+ str(m) +")*", 1).replace(pstr, str(p))
    steps = "\\definecolor{qqwuqq}{rgb}{0.,0.39215686274509803,0.}"
    steps += "\\begin{center}\\begin{tikzpicture}[line cap=round,line join=round,>=triangle 45, scale = .4]"
    steps += "\\begin{axis}[x=0.75cm,y=0.75cm, axis lines=middle, axis line style={very thick,-{Triangle[length=3mm,width=2mm]}},"
    steps += " ymajorgrids=true, xmajorgrids=true, grid style={thick, black!65},"
    steps += rf" xmin=-{xmax}, xmax={xmax}, ymin=-{ymax}, ymax={ymax},"
    steps += rf" xtick={{{-xmax},{-xmax+1},...,{xmax}}}, ytick={{-{ymax},{-ymax+1},...,{ymax}}},"
    steps += " xlabel = $x$, ylabel = $y$]"

    steps += f"\\addplot[line width=2pt,color=qqwuqq,smooth,samples=200,domain={-xmax}:{xmax}] plot(x,{{{expr}}});"

    if m != 0 :
        if "frac" in mstr :
            num, den = clean_frac(mstr)
            num, den = int(num), int(den)
            steps += f"\\draw[->, color = Blue, ultra thick] (0,{p}) -- ({den},{p});"
            steps += f"\\draw[color=blue] ({.5*den},{p}) node[above]" + f"{{$+{den}$}};\n"
            steps += f"\\draw[->, color = Blue, ultra thick] ({den},{p}) -- ({den},{p+num});"
            steps += f"\\draw[color=blue] ({den},{p+.5*num}) node[above right]" +" {$"
            if m > 0 :
                steps += "+"
            steps += f"{num}" +"$};\n"
        else :
            steps += f"\\draw[->, color = Blue, ultra thick] (0,{p}) -- (1,{p});"
            steps += f"\\draw[color=blue] (.5,{p}) node[above]" +" {$+1$};\n"
            steps += f"\\draw[->, color = Blue, ultra thick] (1,{p}) -- (1,{p+m});"
            steps += f"\\draw[color=blue] (1,{p+.5*m}) node[above right]" +" {$"
            if m > 0 :
                steps += "+"
            steps += f"{mstr}" +"$};\n"
    steps += "\\end{axis}\\end{tikzpicture}\\end{center}"

    return steps

def parabole(a, alpha, beta, x1= "", x2= "") :
    steps = ["\\definecolor{qqwuqq}{rgb}{0.,0.39215686274509803,0.}\\\\\n"]
    steps += ["\\begin{center}\\begin{tikzpicture}[line cap=round,line join=round,>=triangle 45]\\\\\n"]
    steps += ["\\begin{axis}[width=18cm, height=10cm, axis lines=middle, axis line style={very thick,-{Triangle[length=3mm,width=2mm]}},  ymajorgrids=true, xmajorgrids=true, grid style={thick, black!75}, ymajorgrids=true, xmajorgrids=true, xmin=-10.51239188649573, xmax=10.340712397491607, ymin=-20.05774985852008, ymax=20.681701030884228, xtick={-10,-9,...,10}, ytick={-20,-15,...,15}, xlabel = $x$, ylabel = $y$]\\\\\n"]
    steps += ["\clip(-10,-20) rectangle (10,20);"]
    steps += [f"\\addplot[line width=1.pt,color=qqwuqq,smooth,samples=100,domain={alpha-5}:{alpha+5}] "+ f"plot(\\x,{{{a}*((\\x)-{alpha})^2 + {beta}}});\\\\\n"]
    if beta <= 0 and alpha <= 0 :
        bpos = "below right"
        apos = "above left"
    elif beta <= 0 and alpha > 0 :
        bpos = "below left"
        apos = "above right"
    if beta > 0 and alpha <= 0 :
        bpos = "above right"
        apos = "below left"
    if beta > 0 and alpha > 0 :
        bpos = "above left"
        apos = "above right"
    steps += [f"\\draw[dashed, color = red, ultra thick] ({alpha},{beta}) -- (0,{beta});"]
    steps += [f"\\draw[color=red] (0,{beta}) node[" + f"{bpos}]" + " {$\\beta$};\n"]
    steps += [f"\\draw[dashed, color = red, ultra thick] ({alpha},{beta}) -- ({alpha},0);"]
    steps += [f"\\draw[color=red] ({alpha},0) node[" + f"{apos}]" + " {$\\alpha$};\n"]
    if x1 != "":
        X1 = latex2sympy(x1)
        X1 = N(X1)
        steps += [f"\\filldraw[blue] ({X1},0) circle (2.5pt);\n"]
        steps += [f"\\draw[color=blue] ({X1},0) node[above]" +" {$x_1$};\n"]
    if x2 != "":
        X2 = latex2sympy(x2)
        X2 = N(X2)
        steps += [f"\\filldraw[blue] ({X2},0) circle (2.5pt);\n"]
        steps += [f"\\draw[color=blue] ({X2},0) node[above]" +" {$x_2$};\n"]
    steps += ["\\end{axis}\\end{tikzpicture}\\end{center}  \\\\\n"]
    return steps