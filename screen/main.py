import tkinter as tk
from ui import SolaryApp

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Solary")
    
    # Configuration plein écran pour tablette Raspberry Pi
    root.attributes('-fullscreen', True)
    
    # Échappement avec la touche Escape (pour le développement)
    root.bind('<Escape>', lambda e: root.destroy())
    
    app = SolaryApp(root)
    app.pack(fill=tk.BOTH, expand=True)
    
    root.mainloop()