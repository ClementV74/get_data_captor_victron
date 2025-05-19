from pymodbus.client.sync import ModbusTcpClient
import requests
import datetime

# Adresse IP et port de l'onduleur
IP_ADDRESS = "172.31.254.74"
PORT = 502
UNIT_ID = 239

client = ModbusTcpClient(IP_ADDRESS, port=PORT)
client.connect()

def get_register_value(register_address):
    result = client.read_holding_registers(register_address, 1, unit=UNIT_ID)
    if not result.isError():
        return result.registers[0]
    else:
        print(f"Erreur à l'adresse {register_address}")
        return None

# Lire les registres
ac_output_voltage_mv = get_register_value(3101)
dc_input_voltage_mv = get_register_value(3105)
current_centi_amp = get_register_value(3114)
inverter_mode = get_register_value(3126)

# Préparer les valeurs
ac_voltage = ac_output_voltage_mv / 10 if ac_output_voltage_mv is not None else None
dc_voltage = dc_input_voltage_mv / 100 if dc_input_voltage_mv is not None else None
current_amp = current_centi_amp / 100 if current_centi_amp is not None else None

power_watts = ac_voltage * current_amp if ac_voltage is not None and current_amp is not None else None

battery_percentage = None
if dc_voltage is not None:
    full_voltage = 12.8
    empty_voltage = 11.0
    battery_percentage = ((dc_voltage - empty_voltage) / (full_voltage - empty_voltage)) * 100
    battery_percentage = max(0, min(battery_percentage, 100))

# Si données valides, envoyer vers l'API
if ac_voltage is not None and current_amp is not None and power_watts is not None:
    payload = {
        "borne_id": 1,
        "voltage": round(ac_voltage, 2),
        "current": round(current_amp, 2),
        "power": round(power_watts, 2),
        "battery_level": round(battery_percentage) if battery_percentage is not None else None,
        "total_energy": None,
        "solar_power": None,
        "energy_generated_kwh": None,
        "energy_consumed_kwh": None,
        "measure_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    # Nettoyer les valeurs nulles
    payload = {k: v for k, v in payload.items() if v is not None}

    try:
        response = requests.post("https://solary.vabre.ch/AddMesureEnergie", json=payload)
        print("Réponse API :", response.status_code, response.text)
    except Exception as e:
        print("Erreur d'envoi :", str(e))
else:
    print("Données incomplètes. Rien envoyé.")

client.close()
