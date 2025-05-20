# 🔐 Solary - Système de Casiers Connectés 📱


## 🌟 Présentation

Solary est un système innovant de casiers connectés alimentés par énergie solaire ☀️ qui permet aux utilisateurs de recharger leurs appareils électroniques en toute sécurité. Chaque casier est équipé d'une prise électrique interne permettant de charger smartphones, tablettes et autres appareils pendant que l'utilisateur vaque à ses occupations. Ce projet combine une application Tkinter pour l'interface utilisateur des bornes physiques, une application web pour la gestion et la réservation en ligne, et un diagramme UML pour visualiser les cas d'utilisation.


---

## ✨ Fonctionnalités Principales

### 🔑 Gestion des Casiers
- 🟢 Visualisation de l'état des casiers (disponible/occupé)
- 🔒 Réservation de casiers via QR code et application mobile
- 🔓 Déverrouillage des casiers via code OTP
- 📊 Interface utilisateur intuitive et moderne



---

## 🔋 Technologie de Recharge

### ☀️ Alimentation Solaire
- 🌞 Panneaux solaires intégrés pour une énergie propre et renouvelable
- 🔄 Système de stockage d'énergie pour fonctionnement 24/7
- 💡 Consommation énergétique optimisée

### 🔌 Casiers de Recharge
- ⚡ Chaque casier équipé d'une prise électrique standard
- 📱 Compatible avec tous types d'appareils (smartphones, tablettes, ordinateurs portables)
- 🔒 Sécurisation pendant toute la durée de la charge
- 📊 Indicateur de niveau de charge (sur l'application mobile)

---

## 🚀 Installation

### Prérequis
- Python 3.8+
- Tkinter
- Flask (pour l'interface web)
- React (pour le diagramme UML)
- Segno (pour la génération de QR codes)

### 📥 Installation Automatique

\`\`\`bash
# Cloner le dépôt
git clone https://github.com/votre-repo/get_data_captor_victron.git
cd get_data_captor_victron

# Exécuter le script d'installation
python setup.py
\`\`\`

### 🛠️ Installation Manuelle

\`\`\`bash
# Installer les dépendances
pip install -r requirements.txt

# Configurer l'URL du QR code
echo "https://dashboard.vabre.ch/" > assets/qrcode_url.txt

# Générer le QR code
python -c "import segno; segno.make_qr('https://dashboard.vabre.ch/').save('assets/qrcode.png')"
\`\`\`

---

## 🏃‍♂️ Utilisation

### 🖥️ Application Borne (Tkinter)

\`\`\`bash
# Lancer l'application Tkinter
python main.py
\`\`\`



---

## 📂 Structure du Projet

\`\`\`
solary/
├── assets/                # Ressources (images, QR codes)
├── components/            # Composants React pour le diagramme UML
├── locker_manager.py      # Gestion des casiers
├── main.py                # Point d'entrée de l'application Tkinter
├── setup.py               # Script d'installation automatique
├── ui.py                  # Interface utilisateur Tkinter
└── README.md              # Ce fichier
\`\`\`

---

## 🛠️ Technologies Utilisées

- **Interface Borne**: Python, Tkinter, PIL
- **QR Code**: Segno
- **Interface Web**: Flask, Bootstrap
- **Diagramme UML**: React, SVG
- **Styles**: CSS, Tailwind CSS

---

## 📸 Captures d'Écran

### Interface Borne
![Interface Borne](https://placeholder.svg?height=200&width=400&text=Interface+Borne)



---

## 🔄 Flux d'Utilisation

1. 👀 L'utilisateur voit un casier disponible (vert)
2. 🖱️ L'utilisateur clique sur "RÉSERVER"
3. 📱 Le système affiche un QR code
4. 📲 L'utilisateur scanne le QR code avec son téléphone
5. 🌐 L'utilisateur est redirigé vers l'application mobile
6. 🎫 L'utilisateur obtient un code de réservation
7. 🔓 L'utilisateur ouvre le casier et branche son appareil à la prise interne
8. 🔒 L'utilisateur ferme le casier, laissant son appareil charger en sécurité
9. ⏱️ Plus tard, l'utilisateur revient et entre le code pour déverrouiller le casier
10. 🔋 L'utilisateur récupère son appareil rechargé

---



⭐ **N'hésitez pas à donner une étoile à ce projet si vous l'avez trouvé utile!** ⭐
