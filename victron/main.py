from pymodbus.client.sync import ModbusTcpClient

# Adresse IP et port de l'onduleur
IP_ADDRESS = "172.31.254.74"
PORT = 502
UNIT_ID = 239  # Identifiant de l'unité Modbus

# Connexion au client Modbus
client = ModbusTcpClient(IP_ADDRESS, port=PORT)
client.connect()

# Fonction pour récupérer la valeur d'un registre
def get_register_value(register_address):
    result = client.read_holding_registers(register_address, 1, unit=UNIT_ID)
    if not result.isError():
        return result.registers[0]
    else:
        print(f"Erreur à l'adresse {register_address}")
        return None

# Lecture des registres
ac_output_voltage_mv = get_register_value(3101)  # Tension AC sortie 
dc_input_voltage_mv = get_register_value(3105)   # Tension DC entrée 
current_centi_amp = get_register_value(3114)     # Courant en centi-ampères
inverter_mode = get_register_value(3126)         # Mode de fonctionnement de l'onduleur

# Traitement des données
if ac_output_voltage_mv is not None:
    ac_voltage = ac_output_voltage_mv / 10  # divise par 10
    print(f"Tension AC Sortie : {ac_voltage:.2f} V")
else:
    ac_voltage = None

if dc_input_voltage_mv is not None:
    dc_voltage = dc_input_voltage_mv / 100  # Conversion en volts
    print(f"Tension DC Entrée : {dc_voltage:.2f} V")
else:
    dc_voltage = None

if current_centi_amp is not None:
    current_amp = current_centi_amp / 100  # Conversion en ampères
    print(f"Courant : {current_amp:.2f} A")
else:
    current_amp = None

# Calcul de la puissance en watts
if ac_voltage is not None and current_amp is not None:
    power_watts = ac_voltage * current_amp
    print(f"Puissance AC : {power_watts:.2f} W")

# Estimation du pourcentage de batterie pour une batterie LiFePO4 12V
if dc_voltage is not None:
    full_voltage = 12.8  # Tension à pleine charge
    empty_voltage = 11.0  # Tension à vide
    battery_percentage = ((dc_voltage - empty_voltage) / (full_voltage - empty_voltage)) * 100
    battery_percentage = max(0, min(battery_percentage, 100))  # Limiter entre 0% et 100%
    print(f"Pourcentage de batterie : {battery_percentage:.2f}%")

# Interprétation du mode de fonctionnement de l'onduleur (registre 3126)
if inverter_mode is not None:
    inverter_modes = {
        1: "Mode veille (recherche de charge)",
        2: "Mode normal (onduleur opérationnel)",
        3: "Mode bypass",
        4: "Mode charge",
        5: "Mode éco",
        9: "Mode inversion (onduleur actif)"
    }
    mode_description = inverter_modes.get(inverter_mode, f"Code inconnu ({inverter_mode})")
    print(f"État de fonctionnement de l'onduleur : {mode_description}")

# Fermeture de la connexion Modbus
client.close()
