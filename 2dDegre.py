from utils import*

os.makedirs("./Exercices", exist_ok=True)
second_membre = True
nom = "2d_degre"
if  second_membre :
    nom += "_2d_membre"

n = 20
path_enonce, path_corr = os.path.join("./Exercices/1ereSpe/", nom + f"_{n}.tex"), os.path.join("./Exercices/1ereSpe/", nom + f"_{n}_correction.tex")
paths = [path_enonce, path_corr]

MASTER_SEED = 20260425
coef_max = 10

enonce = "\\include{../preambule}\n \\begin{document}\n"
enonce += "Résoudre chacune des équations suivantes : \n \\begin{enumerate}\n"
corr = enonce

for i in range(n):
    seed_i = MASTER_SEED + i
    seed(seed_i)
    enonce += f"% SEED {seed_i}\n"
    corr += f"% SEED {seed_i}\n"
    a1 = not0(-coef_max, coef_max)
    coefs1 = [a1] + [randint(-coef_max, coef_max) for _ in range(2)]
    if second_membre :
        a2 = randint(-coef_max, coef_max)
        while a2 == a1 :
            a2 = randint(-coef_max, coef_max)
        coefs2 = [a2] + [randint(-coef_max, coef_max) for _ in range(2)]
    else :
        coefs2 = ["0", "0", "0"]
    a1, b1, c1 = list(map(str, coefs1))
    a2, b2, c2 = list(map(str, coefs2))
    eq = clean(f" {a1}x^2+{b1}x+{c1}") + "=" + clean(f"{a2}x^2+{b2}x+{c2}")
    print(eq)
    enonce += r"\item $"+ eq + "$."
    corr += r"\item $"+ eq + "$."
    corr += "{\\\\\n \\blue "
    etapes, _, _ = sol2(eq)
    corr += " ".join(etapes)
    corr += "}"

enonce += "\\end{enumerate}\n \\end{document}"
corr += "\\end{enumerate}\n \\end{document}"

textes = [enonce, corr]

for k in range(2) :
    path = paths[k]
    texte = textes[k]
    doc_enonce = open(path, "w", encoding="utf-8")
    doc_enonce.write(texte)
    doc_enonce.close()
    compil(path)

clean_latex_files('./Exercices/1ereSpe')