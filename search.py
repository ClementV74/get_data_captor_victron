from pymodbus.client.sync import ModbusTcpClient

# Adresse IP du Raspberry Pi ou de l'onduleur
ip_address = "172.31.254.74"
unit_id = 239

# Créer un client Modbus
client = ModbusTcpClient(ip_address, timeout=5)
client.connect()

# Plage de registres à tester
start_address = 3100
end_address = 3128

# Tester chaque registre dans la plage spécifiée
for address in range(start_address, end_address + 1):
    try:
        # Lecture du registre
        response = client.read_holding_registers(address, 1, unit=unit_id)
        
        # Si une réponse est reçue, on traite
        if response.isError():
            print(f"Erreur à l’adresse {address} : {response}")
        else:
            value = response.registers[0]
            print(f"Registre {address} : {value}")
    except Exception as e:
        print(f"Erreur à l’adresse {address} : {e}")

# Déconnexion du client Modbus
client.close()
