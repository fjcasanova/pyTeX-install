import importlib
import sys
import shutil
import subprocess
import os
import re
import platform

def detect_latex_system():
    if shutil.which("mpm"):
        return "miktex"
    elif shutil.which("tlmgr"):
        return "texlive"
    else:
        return None


def enable_miktex_auto_install():
    possible_paths = [r"C:\Program Files\MiKTeX\miktex\bin\x64\initexmf.exe", r"C:\Program Files (x86)\MiKTeX\miktex\bin\initexmf.exe", rf"C:\Users\{os.getenv('USERNAME')}\AppData\Local\Programs\MiKTeX\miktex\bin\x64\initexmf.exe"]
    for path in possible_paths:
        if os.path.exists(path):
            try:
                subprocess.run([path, "--set-config-value=[MPM]AutoInstall=1"], check=True)
                subprocess.run([path, "--set-config-value=[MPM]AutoAdmin=0"], check=True)
                subprocess.run([path, "--update-fndb"], check=True)
                print("MiKTeX configuré : installation automatique activée.")
                return
            except :
                print("Installation automatique des packages impossible (MiKTeX).")

system = platform.system()

if system == "Windows" :
    if shutil.which("pdflatex") is  None :
        choice = input("MiKTeX n'est pas installé. Voulez-vous l'installer ? (oui/non) : ").strip().lower()
        if choice in ["oui", "o", "yes", "y", "Yes", "Oui", "OUI", "YES"]:
            try:
                subprocess.run(["winget", "install", "-e", "--id", "MiKTeX.MiKTeX"], check=True)
                enable_miktex_auto_install()
            except Exception:
                try:
                    subprocess.run(["choco", "install", "miktex", "-y"], check=True)
                    enable_miktex_auto_install()
                except Exception:
                    print("Impossible d’installer automatiquement MiKTeX.")
                    print("Installer manuellement MiKTeX : https://miktex.org/download")
                    enable_miktex_auto_install()
        elif choice in ["non", "n", "no", "Non", "No", "NON", "NO"]:
            print("Impossible d’installer automatiquement MiKTeX.")
            print("Installer manuellement MiKTeX : https://miktex.org/download")
        else:
            print("Réponse invalide. Tapez 'oui' ou 'non'")
elif system == "Linux" :
    if shutil.which("tlmgr") is  None :
        choice = input("Tex Live n'est pas installé. Voulez-vous l'installer ? (oui/non) : ").strip().lower()
        if choice in ["oui", "o", "yes", "y", "Yes", "Oui", "OUI", "YES"]:
            try :
                subprocess.run(["sudo", "apt-get", "update"], check=True)
                subprocess.run(["sudo", "apt-get", "install", "-y", "texlive-full"], check=True)
            except :
                print("Impossible d’installer automatiquement TeX Live.")
                print("Installer manuellement : https://tug.org/texlive/")
        elif choice in ["non", "n", "no", "Non", "No", "NON", "NO"]:
            print("Impossible d’installer automatiquement TeX Live.")
            print("Installer manuellement : https://tug.org/texlive/")
        else:
            print("Réponse invalide. Tapez 'oui' ou 'non'")
elif system == "Darwin":
    if shutil.which("tlmgr") is  None :
        choice = "oui"
        if choice in ["oui", "o", "yes", "y", "Yes", "Oui", "OUI", "YES"]:
            try :
                subprocess.run(["brew", "install", "--cask", "mactex"], check=True)
            except :
                print("Impossible d’installer automatiquement Mac TeX.")
                print("Installer manuellement : https://tug.org/mactex/")
        elif choice in ["non", "n", "no", "Non", "No", "NON", "NO"]:
            print("Impossible d’installer automatiquement Mac TeX.")
            print("Installer manuellement Mac TeX : https://tug.org/mactex/")
        else:
            print("Réponse invalide. Tapez 'oui' ou 'non'")


sys.path.insert(1, './methodes')

for name in ["sympy", "latex2sympy2"] :
    try:
        importlib.import_module(name)
    except ImportError:
        print(f"{name} non trouvé, installation en cours...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", name])
        
def add2path() :
    system = platform.system()
    if system == "Windows":
        possible_paths = [
            r"C:\Program Files\MiKTeX\miktex\bin\x64",
            r"C:\Program Files (x86)\MiKTeX\miktex\bin",
            rf"C:\Users\{os.getenv('USERNAME')}\AppData\Local\Programs\MiKTeX\miktex\bin\x64"]
        for path in possible_paths:
            if os.path.exists(path):
                os.environ["PATH"] += ";" + path
                return True
    elif system == "Darwin":
        path = "/Library/TeX/texbin"
        if os.path.exists(path):
            os.environ["PATH"] += os.pathsep + path
            return True
    elif system in ["Linux"]:
        return True

    return False

def compil(chemin_fichier):
    dossier = os.path.dirname(chemin_fichier)
    nom_fichier = os.path.basename(chemin_fichier)
#    system = platform.system()
#    if shutil.which("latexmk"):
#        cmd = ["latexmk", "-pdf", "-interaction=nonstopmode", nom_fichier]
#    elif system == "Windows" :
#        if shutil.which("pdflatex") is  None :
#            add2path()
#        cmd = ["pdflatex", "-interaction=nonstopmode", nom_fichier]
    subprocess.run(["latexmk", "-pdf", "-interaction=nonstopmode", nom_fichier],
               cwd=dossier,
               stdout=subprocess.DEVNULL,
               stderr=subprocess.DEVNULL,
               check=True)

from resolutions import*
from derivation import*
from calcul import*
from tableaux import*
from courbes import*
from gen_fonctions import*
import glob

def clean_latex_files(directory="."):
    extensions = ["*.aux", "*.log", "*.out", "*.toc", "*.lof", "*.lot"]
    for ext in extensions:
        for file in glob.glob(os.path.join(directory, ext)):
            os.remove(file)
