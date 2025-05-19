import tkinter as tk
import time
from datetime import datetime
import os
from tkinter import PhotoImage
from locker_manager import LockerManager

class SolaryApp(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.locker_manager = LockerManager()
        
        # Palette de couleurs moderne
        self.bg_color = "#f8f9fa"
        self.primary_color = "#6c5ce7"  # Violet/bleu
        self.secondary_color = "#a29bfe"  # Violet clair
        self.accent_color = "#00cec9"  # Turquoise
        self.text_color = "#2d3436"  # Presque noir
        self.available_color = "#00b894"  # Vert
        self.occupied_color = "#e17055"  # Rouge-orange
        self.button_hover = "#5f50e1"  # Violet plus foncé
        self.error_color = "#d63031"  # Rouge pour les erreurs
        self.success_color = "#00b894"  # Vert pour les succès
        
        # État de l'interface
        self.current_view = "main"  # main, code_entry, notification, qr_code
        self.active_locker = None
        self.notification_text = ""
        self.notification_type = "info"
        
        # Charger l'URL du QR code
        self.qr_code_url = self.load_qr_code_url()
        
        self.configure(bg=self.bg_color)
        self.create_widgets()
        self.update_clock()
        
    def load_qr_code_url(self):
        """Charge l'URL du QR code depuis le fichier de configuration"""
        try:
            if os.path.exists("assets/qrcode_url.txt"):
                with open("assets/qrcode_url.txt", "r") as f:
                    return f.read().strip()
        except Exception:
            pass
        
        # URL par défaut si le fichier n'existe pas
        return "https://dashboard.vabre.ch/"
        
    def create_widgets(self):
        # En-tête avec dégradé
        header_frame = tk.Frame(self, bg=self.primary_color, height=100)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Logo et titre
        logo_frame = tk.Frame(header_frame, bg=self.primary_color)
        logo_frame.pack(pady=15)
        
        # Création d'un logo simple
        logo_canvas = tk.Canvas(logo_frame, width=50, height=50, bg=self.primary_color, highlightthickness=0)
        logo_canvas.create_oval(5, 5, 45, 45, fill=self.accent_color, outline="")
        logo_canvas.create_oval(15, 15, 35, 35, fill=self.primary_color, outline="")
        logo_canvas.pack(side=tk.LEFT, padx=(0, 10))
        
        header_label = tk.Label(
            logo_frame, 
            text="SOLARY", 
            font=("Helvetica", 28, "bold"), 
            fg="white", 
            bg=self.primary_color
        )
        header_label.pack(side=tk.LEFT)
        
        # Sous-titre
        subtitle = tk.Label(
            header_frame, 
            text="Casiers Connectés", 
            font=("Helvetica", 12), 
            fg="white", 
            bg=self.primary_color
        )
        subtitle.pack(pady=(0, 10))
        
        # Conteneur principal
        self.main_container = tk.Frame(self, bg=self.bg_color)
        self.main_container.pack(fill=tk.BOTH, expand=True, padx=30, pady=20)
        
        # Créer les différentes vues
        self.create_main_view()
        self.create_code_entry_view()
        self.create_notification_view()
        self.create_qr_code_view()
        
        # Afficher la vue principale par défaut
        self.show_view("main")
        
        # Pied de page avec dégradé
        footer_frame = tk.Frame(self, bg=self.primary_color, height=60)
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        footer_label = tk.Label(
            footer_frame, 
            text="© 2025 Solary - Tous droits réservés", 
            font=("Helvetica", 10), 
            fg="white", 
            bg=self.primary_color
        )
        footer_label.pack(pady=20)
    
    def create_main_view(self):
        """Crée la vue principale avec les casiers"""
        self.main_view = tk.Frame(self.main_container, bg=self.bg_color)
        
        # Horloge et date
        self.clock_frame = tk.Frame(self.main_view, bg=self.bg_color)
        self.clock_frame.pack(fill=tk.X, pady=(0, 20))
        
        self.time_label = tk.Label(
            self.clock_frame, 
            font=("Helvetica", 14), 
            bg=self.bg_color, 
            fg=self.text_color
        )
        self.time_label.pack(side=tk.RIGHT)
        
        # Titre des casiers avec style
        title_frame = tk.Frame(self.main_view, bg=self.bg_color)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            title_frame, 
            text="Vos casiers disponibles", 
            font=("Helvetica", 22, "bold"), 
            bg=self.bg_color, 
            fg=self.primary_color
        )
        title_label.pack(side=tk.LEFT)
        
        # Ligne de séparation décorative
        separator = tk.Canvas(self.main_view, height=3, bg=self.bg_color, highlightthickness=0)
        separator.pack(fill=tk.X, pady=(0, 30))
        separator.create_line(0, 1, 800, 1, fill=self.secondary_color)
        
        # Conteneur pour les casiers
        lockers_frame = tk.Frame(self.main_view, bg=self.bg_color)
        lockers_frame.pack(fill=tk.BOTH, expand=True)
        
        # Création des casiers
        self.locker_frames = []
        self.locker_status_labels = []
        self.locker_buttons = []
        
        for i in range(2):
            # Frame pour chaque casier avec effet d'ombre
            locker_frame = tk.Frame(
                lockers_frame, 
                bg="white", 
                bd=0, 
                highlightthickness=1,
                highlightbackground="#e0e0e0",
                padx=25, 
                pady=25
            )
            locker_frame.grid(row=0, column=i, padx=20, pady=20, sticky="nsew")
            self.locker_frames.append(locker_frame)
            
            # Titre du casier
            locker_title = tk.Label(
                locker_frame, 
                text=f"Casier {i+1}", 
                font=("Helvetica", 18, "bold"), 
                bg="white",
                fg=self.primary_color
            )
            locker_title.pack(pady=(0, 15))
            
            # Indicateur d'état (cercle coloré)
            status_frame = tk.Frame(locker_frame, bg="white", height=100)
            status_frame.pack(fill=tk.X, pady=15)
            
            # Initialisation avec l'état actuel
            locker_status = self.locker_manager.get_locker_status(i)
            color = self.available_color if locker_status else self.occupied_color
            
            # Cercle plus grand et plus beau
            status_indicator = tk.Canvas(
                status_frame, 
                width=100, 
                height=100, 
                bg="white", 
                highlightthickness=0
            )
            status_indicator.pack(pady=10)
            
            # Cercle extérieur (effet de lueur)
            status_indicator.create_oval(5, 5, 95, 95, fill="#f5f5f5", outline="")
            # Cercle principal
            status_indicator.create_oval(10, 10, 90, 90, fill=color, outline="")
            # Reflet (effet 3D)
            status_indicator.create_oval(25, 25, 55, 55, fill="#ffffff", outline="", width=0)
            
            self.locker_status_labels.append(status_indicator)
            
            # Texte d'état avec style
            status_text = tk.Label(
                locker_frame, 
                text="DISPONIBLE" if locker_status else "OCCUPÉ", 
                font=("Helvetica", 16, "bold"), 
                bg="white",
                fg=self.available_color if locker_status else self.occupied_color
            )
            status_text.pack(pady=(0, 15))
            
            # Description
            description = tk.Label(
                locker_frame,
                text="Prêt à être utilisé" if locker_status else "Actuellement en utilisation",
                font=("Helvetica", 12),
                bg="white",
                fg=self.text_color
            )
            description.pack(pady=(0, 20))
            
            # Bouton d'action avec style
            action_button = tk.Button(
                locker_frame, 
                text="RÉSERVER" if locker_status else "DÉVERROUILLER", 
                font=("Helvetica", 14, "bold"), 
                bg=self.primary_color, 
                fg="white",
                activebackground=self.button_hover,
                activeforeground="white",
                bd=0,
                padx=30, 
                pady=12,
                cursor="hand2",
                command=lambda idx=i: self.handle_locker_action(idx)
            )
            action_button.pack(pady=10)
            self.locker_buttons.append(action_button)
        
        # Configuration du grid pour qu'il soit responsive
        lockers_frame.grid_columnconfigure(0, weight=1)
        lockers_frame.grid_columnconfigure(1, weight=1)
    
    def create_code_entry_view(self):
        """Crée la vue de saisie de code"""
        self.code_entry_view = tk.Frame(self.main_container, bg=self.bg_color)
        
        # Conteneur central
        center_frame = tk.Frame(self.code_entry_view, bg="white", padx=40, pady=40)
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Titre
        title_label = tk.Label(
            center_frame,
            text="Entrez votre code de déverrouillage",
            font=("Helvetica", 20, "bold"),
            bg="white",
            fg=self.primary_color
        )
        title_label.pack(pady=(0, 30))
        
        # Sous-titre avec numéro de casier
        self.code_subtitle = tk.Label(
            center_frame,
            text="Casier X",
            font=("Helvetica", 16),
            bg="white",
            fg=self.text_color
        )
        self.code_subtitle.pack(pady=(0, 30))
        
        # Champ de saisie
        self.code_entry = tk.Entry(
            center_frame,
            font=("Helvetica", 24),
            width=10,
            justify='center',
            bd=2,
            relief=tk.SOLID
        )
        self.code_entry.pack(pady=20)
        
        # Message d'erreur (initialement caché)
        self.code_error = tk.Label(
            center_frame,
            text="Code incorrect. Veuillez réessayer.",
            font=("Helvetica", 12),
            bg="white",
            fg=self.error_color
        )
        self.code_error.pack(pady=(0, 20))
        self.code_error.pack_forget()  # Caché par défaut
        
        # Boutons
        button_frame = tk.Frame(center_frame, bg="white")
        button_frame.pack(pady=20)
        
        tk.Button(
            button_frame,
            text="Annuler",
            font=("Helvetica", 14),
            bg="#dfe6e9",
            fg="#2d3436",
            bd=0,
            padx=30,
            pady=10,
            command=lambda: self.show_view("main")
        ).pack(side=tk.LEFT, padx=20)
        
        tk.Button(
            button_frame,
            text="Valider",
            font=("Helvetica", 14, "bold"),
            bg=self.primary_color,
            fg="white",
            bd=0,
            padx=30,
            pady=10,
            command=self.validate_code
        ).pack(side=tk.LEFT, padx=20)
    
    def create_notification_view(self):
        """Crée la vue de notification"""
        self.notification_view = tk.Frame(self.main_container, bg=self.bg_color)
        
        # Conteneur central
        center_frame = tk.Frame(self.notification_view, bg="white", padx=40, pady=40)
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Icône de notification
        self.notification_icon = tk.Canvas(
            center_frame, 
            width=100, 
            height=100, 
            bg="white", 
            highlightthickness=0
        )
        self.notification_icon.pack(pady=20)
        
        # Texte de notification
        self.notification_label = tk.Label(
            center_frame,
            text="",
            font=("Helvetica", 18, "bold"),
            bg="white",
            fg=self.text_color,
            wraplength=400,
            justify=tk.CENTER
        )
        self.notification_label.pack(pady=30)
        
        # Bouton de retour
        tk.Button(
            center_frame,
            text="Retour",
            font=("Helvetica", 14, "bold"),
            bg=self.primary_color,
            fg="white",
            bd=0,
            padx=30,
            pady=10,
            command=lambda: self.show_view("main")
        ).pack(pady=20)
    
    def create_qr_code_view(self):
        """Crée la vue avec le QR code pour l'application mobile"""
        self.qr_code_view = tk.Frame(self.main_container, bg=self.bg_color)
        
        # Conteneur central
        center_frame = tk.Frame(self.qr_code_view, bg="white", padx=40, pady=40)
        center_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
        # Titre
        title_label = tk.Label(
            center_frame,
            text="Réservation via l'application mobile",
            font=("Helvetica", 20, "bold"),
            bg="white",
            fg=self.primary_color
        )
        title_label.pack(pady=(0, 20))
        
        # Message explicatif
        message = tk.Label(
            center_frame,
            text="Merci de passer par l'application mobile pour la réservation de casiers.",
            font=("Helvetica", 14),
            bg="white",
            fg=self.text_color,
            wraplength=400,
            justify=tk.CENTER
        )
        message.pack(pady=(0, 20))
        
        # QR Code
        qr_frame = tk.Frame(center_frame, bg="white")
        qr_frame.pack(pady=20)
        
        # Conteneur pour le QR code
        self.qr_container = tk.Frame(qr_frame, bg="white")
        self.qr_container.pack()
        
        # Charger le QR code s'il existe
        self.qr_image = None
        self.qr_label = None
        self.load_qr_code()
        
        # URL sous le QR code
        url_label = tk.Label(
            center_frame,
            text=self.qr_code_url,
            font=("Helvetica", 12),
            bg="white",
            fg=self.primary_color
        )
        url_label.pack(pady=(10, 30))
        
        # Bouton de retour
        tk.Button(
            center_frame,
            text="Retour",
            font=("Helvetica", 14, "bold"),
            bg=self.primary_color,
            fg="white",
            bd=0,
            padx=30,
            pady=10,
            command=lambda: self.show_view("main")
        ).pack(pady=10)
    
    def load_qr_code(self):
        """Charge le QR code depuis le fichier"""
        qr_path = "assets/qrcode.png"
        
        if os.path.exists(qr_path):
            try:
                # Supprimer l'ancien label s'il existe
                if self.qr_label:
                    self.qr_label.destroy()
                
                # Charger l'image
                self.qr_image = PhotoImage(file=qr_path)
                
                # Créer un nouveau label avec l'image
                self.qr_label = tk.Label(
                    self.qr_container,
                    image=self.qr_image,
                    bg="white"
                )
                self.qr_label.pack()
            except Exception as e:
                print(f"Erreur lors du chargement du QR code: {e}")
                self.create_fallback_qr_code()
        else:
            self.create_fallback_qr_code()
    
    def create_fallback_qr_code(self):
        """Crée un QR code de secours si l'image n'est pas disponible"""
        # Supprimer l'ancien label s'il existe
        if self.qr_label:
            self.qr_label.destroy()
        
        # Créer un canvas pour dessiner un QR code simplifié
        qr_canvas = tk.Canvas(
            self.qr_container,
            width=200,
            height=200,
            bg="white",
            highlightthickness=1,
            highlightbackground="#e0e0e0"
        )
        qr_canvas.pack()
        
        # Dessiner un QR code simplifié
        # Cadre
        qr_canvas.create_rectangle(10, 10, 190, 190, fill="white", outline="black", width=2)
        
        # Coins caractéristiques d'un QR code
        # Coin supérieur gauche
        qr_canvas.create_rectangle(20, 20, 60, 60, fill="black", outline="")
        qr_canvas.create_rectangle(30, 30, 50, 50, fill="white", outline="")
        qr_canvas.create_rectangle(35, 35, 45, 45, fill="black", outline="")
        
        # Coin supérieur droit
        qr_canvas.create_rectangle(140, 20, 180, 60, fill="black", outline="")
        qr_canvas.create_rectangle(150, 30, 170, 50, fill="white", outline="")
        qr_canvas.create_rectangle(155, 35, 165, 45, fill="black", outline="")
        
        # Coin inférieur gauche
        qr_canvas.create_rectangle(20, 140, 60, 180, fill="black", outline="")
        qr_canvas.create_rectangle(30, 150, 50, 170, fill="white", outline="")
        qr_canvas.create_rectangle(35, 155, 45, 165, fill="black", outline="")
        
        # Dessiner quelques carrés aléatoires pour simuler le contenu du QR code
        for i in range(20):
            x = 70 + (i % 5) * 10
            y = 70 + (i // 5) * 10
            if (i + i//5) % 3 != 0:  # Motif aléatoire
                qr_canvas.create_rectangle(x, y, x+8, y+8, fill="black", outline="")
        
        # Ajouter un logo Solary au centre
        qr_canvas.create_oval(85, 85, 115, 115, fill=self.primary_color, outline="")
        qr_canvas.create_oval(95, 95, 105, 105, fill="white", outline="")
        
        # Stocker le canvas comme label de secours
        self.qr_label = qr_canvas
    
    def show_view(self, view_name):
        """Affiche la vue spécifiée et cache les autres"""
        self.current_view = view_name
        
        # Cacher toutes les vues
        for view in [self.main_view, self.code_entry_view, self.notification_view, self.qr_code_view]:
            view.pack_forget()
        
        # Afficher la vue demandée
        if view_name == "main":
            self.main_view.pack(fill=tk.BOTH, expand=True)
            self.update_locker_displays()  # Mettre à jour l'affichage des casiers
        elif view_name == "code_entry":
            self.code_entry_view.pack(fill=tk.BOTH, expand=True)
            self.code_entry.delete(0, tk.END)  # Effacer le champ
            self.code_error.pack_forget()  # Cacher le message d'erreur
            self.code_entry.focus_set()  # Mettre le focus sur le champ
        elif view_name == "notification":
            self.notification_view.pack(fill=tk.BOTH, expand=True)
            self.update_notification()
        elif view_name == "qr_code":
            self.qr_code_view.pack(fill=tk.BOTH, expand=True)
    
    def update_clock(self):
        """Met à jour l'horloge avec la date et l'heure actuelles"""
        now = datetime.now()
        date_str = now.strftime("%d %B %Y")
        time_str = now.strftime("%H:%M:%S")
        self.time_label.config(text=f"{date_str} | {time_str}")
        self.after(1000, self.update_clock)  # Mise à jour toutes les secondes
    
    def handle_locker_action(self, locker_id):
        """Gère l'action sur un casier (réservation ou déverrouillage)"""
        locker_status = self.locker_manager.get_locker_status(locker_id)
        self.active_locker = locker_id
        
        if locker_status:  # Casier disponible
            # Afficher la vue QR code pour la réservation via l'app mobile
            self.show_view("qr_code")
        else:  # Casier occupé
            # Afficher la vue de saisie de code
            self.code_subtitle.config(text=f"Casier {locker_id + 1}")
            self.show_view("code_entry")
    
    def validate_code(self):
        """Valide le code entré pour déverrouiller un casier"""
        code = self.code_entry.get()
        
        if self.locker_manager.verify_code(self.active_locker, code):
            # Code correct
            self.notification_text = "Code correct! Votre casier est en cours d'ouverture."
            self.notification_type = "success"
            
            # Libérer le casier
            self.locker_manager.release_locker(self.active_locker)
            self.show_view("notification")
        else:
            # Code incorrect
            self.code_error.pack(pady=(0, 20))
            self.code_entry.delete(0, tk.END)
            self.code_entry.focus_set()
    
    def update_notification(self):
        """Met à jour l'affichage de la notification"""
        # Effacer l'icône
        self.notification_icon.delete("all")
        
        # Dessiner l'icône selon le type
        if self.notification_type == "success":
            # Cercle vert avec coche
            self.notification_icon.create_oval(10, 10, 90, 90, fill=self.success_color, outline="")
            self.notification_icon.create_line(30, 50, 45, 65, fill="white", width=5)
            self.notification_icon.create_line(45, 65, 70, 35, fill="white", width=5)
            self.notification_label.config(fg=self.success_color)
        elif self.notification_type == "error":
            # Cercle rouge avec croix
            self.notification_icon.create_oval(10, 10, 90, 90, fill=self.error_color, outline="")
            self.notification_icon.create_line(30, 30, 70, 70, fill="white", width=5)
            self.notification_icon.create_line(30, 70, 70, 30, fill="white", width=5)
            self.notification_label.config(fg=self.error_color)
        else:  # info
            # Cercle bleu avec i
            self.notification_icon.create_oval(10, 10, 90, 90, fill=self.primary_color, outline="")
            self.notification_icon.create_text(50, 50, text="i", fill="white", font=("Helvetica", 40, "bold"))
            self.notification_label.config(fg=self.primary_color)
        
        # Mettre à jour le texte
        self.notification_label.config(text=self.notification_text)
    
    def update_locker_displays(self):
        """Met à jour l'affichage de tous les casiers"""
        for locker_id in range(2):
            self.update_locker_display(locker_id)
    
    def update_locker_display(self, locker_id):
        """Met à jour l'affichage d'un casier spécifique"""
        locker_status = self.locker_manager.get_locker_status(locker_id)
        color = self.available_color if locker_status else self.occupied_color
        
        # Mettre à jour l'indicateur d'état
        canvas = self.locker_status_labels[locker_id]
        canvas.delete("all")
        canvas.create_oval(5, 5, 95, 95, fill="#f5f5f5", outline="")
        canvas.create_oval(10, 10, 90, 90, fill=color, outline="")
        canvas.create_oval(25, 25, 55, 55, fill="#ffffff", outline="", width=0)
        
        # Mettre à jour le texte d'état
        parent = canvas.master.master
        for widget in parent.winfo_children():
            if isinstance(widget, tk.Label) and (widget.cget("text") == "DISPONIBLE" or widget.cget("text") == "OCCUPÉ"):
                widget.config(
                    text="DISPONIBLE" if locker_status else "OCCUPÉ",
                    fg=self.available_color if locker_status else self.occupied_color
                )
            elif isinstance(widget, tk.Label) and (widget.cget("text") == "Prêt à être utilisé" or widget.cget("text") == "Actuellement en utilisation"):
                widget.config(
                    text="Prêt à être utilisé" if locker_status else "Actuellement en utilisation"
                )
        
        # Mettre à jour le bouton
        self.locker_buttons[locker_id].config(
            text="RÉSERVER" if locker_status else "DÉVERROUILLER"
        )