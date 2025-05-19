#!/usr/bin/env python3
import sys
import subprocess
import importlib.util
import os
import platform

def check_python_version():
    """Vérifie que Python 3.x est utilisé"""
    if sys.version_info[0] < 3:
        print("❌ Python 3 est requis. Vous utilisez Python", sys.version.split()[0])
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} détecté")

def check_module(module_name):
    """Vérifie si un module est installé"""
    spec = importlib.util.find_spec(module_name)
    if spec is None:
        return False
    return True

def install_module(module_name):
    """Installe un module avec pip"""
    print(f"📦 Installation de {module_name}...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", module_name])

def check_and_install_dependencies():
    """Vérifie et installe les dépendances nécessaires"""
    # Liste des modules requis
    required_modules = {
        "tkinter": "python3-tk",  # tkinter est spécial, il s'installe différemment
        "datetime": "datetime",
        "time": None,  # Module standard, pas besoin d'installer
        "segno": "segno",  # Pour générer le QR code
        "PIL": "pillow",  # Pour manipuler les images
    }
    
    missing_modules = []
    
    # Vérifier chaque module
    for module, pip_name in required_modules.items():
        if not check_module(module):
            if pip_name:  # Si le module a un nom pip
                missing_modules.append((module, pip_name))
            else:
                print(f"❌ Module standard {module} non disponible. Vérifiez votre installation Python.")
                sys.exit(1)
    
    # Installer les modules manquants
    if missing_modules:
        print("Modules manquants détectés. Installation en cours...")
        
        # Cas spécial pour tkinter sur différents systèmes
        if any(module == "tkinter" for module, _ in missing_modules):
            system = platform.system().lower()
            if system == "linux":
                # Sur Linux, tkinter s'installe via le gestionnaire de paquets
                if os.path.exists("/usr/bin/apt"):
                    print("📦 Installation de tkinter via apt...")
                    subprocess.check_call(["sudo", "apt", "update"])
                    subprocess.check_call(["sudo", "apt", "install", "-y", "python3-tk"])
                elif os.path.exists("/usr/bin/dnf"):
                    print("📦 Installation de tkinter via dnf...")
                    subprocess.check_call(["sudo", "dnf", "install", "-y", "python3-tkinter"])
                else:
                    print("❌ Impossible d'installer tkinter automatiquement. Veuillez l'installer manuellement.")
                    sys.exit(1)
            elif system == "darwin":  # macOS
                print("❌ Sur macOS, tkinter devrait être inclus avec Python. Vérifiez votre installation Python.")
                sys.exit(1)
            elif system == "windows":
                print("❌ Sur Windows, tkinter devrait être inclus avec Python. Vérifiez votre installation Python.")
                sys.exit(1)
        
        # Installer les autres modules via pip
        for module, pip_name in missing_modules:
            if module != "tkinter":  # tkinter est traité séparément
                install_module(pip_name)
    
    print("✅ Toutes les dépendances sont installées")

def generate_qr_code():
    """Génère le QR code pour l'application"""
    print("🔄 Génération du QR code...")
    
    # Créer le dossier assets s'il n'existe pas
    if not os.path.exists("assets"):
        os.makedirs("assets")
    
    # URL du site (demander à l'utilisateur ou utiliser la valeur par défaut)
    default_url = "https://dashboard.vabre.ch/"
    url = input(f"Entrez l'URL pour le QR code (ou appuyez sur Entrée pour utiliser {default_url}): ") or default_url
    
    try:
        import segno
        
        # Générer le QR code
        qr = segno.make_qr(url)
        
        # Sauvegarder le QR code avec une taille adaptée
        qr_path = "assets/qrcode.png"
        qr.save(qr_path, scale=10, border=4)
        
        print(f"✅ QR code généré avec succès: {qr_path}")
        
        # Sauvegarder l'URL dans un fichier de configuration
        with open("assets/qrcode_url.txt", "w") as f:
            f.write(url)
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la génération du QR code: {e}")
        return False

def run_application():
    """Lance l'application principale"""
    print("🚀 Lancement de l'application Solary...")
    
    # Vérifier si main.py existe
    if not os.path.exists("main.py"):
        print("❌ Fichier main.py introuvable. Vérifiez que vous êtes dans le bon répertoire.")
        sys.exit(1)
    
    # Lancer l'application
    subprocess.call([sys.executable, "main.py"])

def main():
    """Fonction principale"""
    print("🔍 Vérification de l'environnement pour Solary...")
    
    # Vérifier la version de Python
    check_python_version()
    
    # Vérifier et installer les dépendances
    check_and_install_dependencies()
    
    # Générer le QR code
    qr_success = generate_qr_code()
    
    if not qr_success:
        print("⚠️ Le QR code n'a pas pu être généré. L'application utilisera un QR code par défaut.")
    
    # Lancer l'application
    run_application()

if __name__ == "__main__":
    main()