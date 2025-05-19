from mock_data import MockDataProvider

class LockerManager:
    def __init__(self):
        self.data_provider = MockDataProvider()
    
    def get_locker_status(self, locker_id):
        """
        Récupère l'état d'un casier
        
        Args:
            locker_id: ID du casier
            
        Returns:
            bool: True si disponible, False si occupé/réservé
        """
        return self.data_provider.get_locker_status(locker_id)
    
    def verify_code(self, locker_id, code):
        """
        Vérifie si le code fourni est valide pour le casier
        
        Args:
            locker_id: ID du casier
            code: Code à vérifier
            
        Returns:
            bool: True si le code est valide, False sinon
        """
        return self.data_provider.verify_code(locker_id, code)
    
    def reserve_locker(self, locker_id):
        """
        Réserve un casier
        
        Args:
            locker_id: ID du casier à réserver
        """
        self.data_provider.update_locker_status(locker_id, False)
    
    def release_locker(self, locker_id):
        """
        Libère un casier
        
        Args:
            locker_id: ID du casier à libérer
        """
        self.data_provider.update_locker_status(locker_id, True)
    
    # Méthodes à implémenter pour l'intégration future avec l'API
    def connect_to_api(self, api_url, api_key):
        """
        Connecte le gestionnaire à l'API
        
        Args:
            api_url: URL de l'API
            api_key: Clé d'API
        """
        pass
    
    # Méthode pour le contrôle futur des relais
    def trigger_relay(self, locker_id):
        """
        Déclenche le relais pour ouvrir un casier
        
        Args:
            locker_id: ID du casier à ouvrir
        """
        # À implémenter avec GPIO ou MQTT
        print(f"Ouverture du casier {locker_id} via relais")