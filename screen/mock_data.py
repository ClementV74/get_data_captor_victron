class MockDataProvider:
    def __init__(self):
        # État initial des casiers (True = disponible, False = occupé)
        self.locker_status = {
            0: True,  # Casier 1 disponible
            1: False  # Casier 2 occupé
        }
        
        # Codes de déverrouillage pour les casiers
        self.locker_codes = {
            0: "1234",
            1: "5678"
        }
    
    def get_locker_status(self, locker_id):
        """
        Récupère l'état d'un casier
        
        Args:
            locker_id: ID du casier
            
        Returns:
            bool: True si disponible, False si occupé/réservé
        """
        return self.locker_status.get(locker_id, False)
    
    def update_locker_status(self, locker_id, status):
        """
        Met à jour l'état d'un casier
        
        Args:
            locker_id: ID du casier
            status: Nouvel état (True = disponible, False = occupé)
        """
        self.locker_status[locker_id] = status
    
    def verify_code(self, locker_id, code):
        """
        Vérifie si le code fourni est valide pour le casier
        
        Args:
            locker_id: ID du casier
            code: Code à vérifier
            
        Returns:
            bool: True si le code est valide, False sinon
        """
        return self.locker_codes.get(locker_id) == code
    
    def get_valid_code(self, locker_id):
        """
        Récupère le code valide pour un casier (pour la démo)
        
        Args:
            locker_id: ID du casier
            
        Returns:
            str: Code valide
        """
        return self.locker_codes.get(locker_id, "")