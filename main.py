from pymodbus.client.sync import ModbusTcpClient

# Adresse IP et port de l'onduleur (ajuster si nécessaire)
IP_ADDRESS = "172.31.254.74"
PORT = 502

# Connexion au client Modbus
client = ModbusTcpClient(IP_ADDRESS, port=PORT)
client.connect()

# Fonction pour récupérer les registres et les valeurs
def get_register_value(register_address):
    result = client.read_holding_registers(register_address, 1, unit=239)
    if not result.isError():
        return result.registers[0]
    else:
        print(f"Erreur à l'adresse {register_address}")
        return None

# Récupération des valeurs des registres
ac_output_voltage_mv = get_register_value(3101)  # AC Sortie mV
dc_input_voltage_mv = get_register_value(3105)  # DC Entrée mV
current_amperes = get_register_value(3114)  # Ampères

# Calcul de la puissance en watts
# AC Sortie en V = AC Sortie mV / 1000
# Puissance en Watts = Volts * Amperes
if ac_output_voltage_mv and current_amperes:
    ac_voltage = ac_output_voltage_mv / 100  # Conversion mV à V
    watts = ac_voltage * (current_amperes / 100)  # Calcul de la puissance en watts (A -> A*V)
    print(f"Puissance AC : {watts:.2f} W")
else:
    watts = None

# Calcul du pourcentage de la batterie LiFePO4
# Plage de tension typique pour LiFePO4 12V
full_voltage = 12.8  # Pleine charge
empty_voltage = 11  # Batterie déchargée

if dc_input_voltage_mv:
    dc_voltage = dc_input_voltage_mv / 100  # Conversion mV à V
    # Calcul du pourcentage de la batterie
    battery_percentage = ((dc_voltage - empty_voltage) / (full_voltage - empty_voltage)) * 100
    battery_percentage = max(0, min(battery_percentage, 100))  # Limiter entre 0% et 100%
    print(f"Pourcentage de batterie : {battery_percentage:.2f}%")
else:
    battery_percentage = None

# Affichage des résultats
if ac_output_voltage_mv:
    print(f"Tension AC Sortie : {ac_output_voltage_mv / 100:.2f} V")

if dc_input_voltage_mv:
    print(f"Tension DC Entrée : {dc_input_voltage_mv / 100:.2f} V")

if current_amperes:
    print(f"Courant : {current_amperes :.2f} A")

# Fermer la connexion au client Modbus
client.close()
