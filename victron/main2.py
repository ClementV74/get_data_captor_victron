import datetime
from pymodbus.client.sync import ModbusTcpClient
import requests

IP_ADDRESS = "172.31.254.74"
PORT = 502
UNIT_ID = 239
client = ModbusTcpClient(IP_ADDRESS, port=PORT)
client.connect()

def get_register_value(addr):
    result = client.read_holding_registers(addr, 1, unit=UNIT_ID)
    return result.registers[0] if not result.isError() else None

# Lire les registres
ac_mv = get_register_value(3101)
dc_mv = get_register_value(3105)
centi_amp = get_register_value(3114)
inverter_mode = get_register_value(3126)

ac_v = ac_mv / 10 if ac_mv is not None else None
dc_v = dc_mv / 100 if dc_mv is not None else None
amp = centi_amp / 100 if centi_amp is not None else None
power_w = ac_v * amp if ac_v is not None and amp is not None else None

battery_pct = None
if dc_v is not None:
    battery_pct = ((dc_v - 11.0) / (12.8 - 11.0)) * 100
    battery_pct = max(0, min(battery_pct, 100))

solar_power = dc_v * amp if dc_v is not None and amp is not None else None

# Pas de cumul possible ici, donc estimations sur 1 seconde
delta_t = 1  # secondes
energy_generated_kwh = solar_power * delta_t / 3600 if solar_power is not None else None
energy_consumed_kwh = power_w * delta_t / 3600 if power_w is not None else None
total_energy = energy_consumed_kwh  # approximation sans historique

# Préparer la requête
if ac_v is not None and amp is not None and power_w is not None:
    payload = {
        "borne_id": 1,
        "voltage": round(ac_v, 2),
        "current": round(amp, 2),
        "power": round(power_w, 2),
        "battery_level": round(battery_pct) if battery_pct is not None else None,
        "total_energy": round(total_energy, 4) if total_energy is not None else None,
        "solar_power": round(solar_power, 2) if solar_power is not None else None,
        "energy_generated_kwh": round(energy_generated_kwh, 4) if energy_generated_kwh is not None else None,
        "energy_consumed_kwh": round(energy_consumed_kwh, 4) if energy_consumed_kwh is not None else None,
        "measure_date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    payload = {k: v for k, v in payload.items() if v is not None}

    try:
        res = requests.post("https://solary.vabre.ch/AddMesureEnergie", json=payload)
        print(res.status_code, res.text)
    except Exception as e:
        print("Erreur d'envoi:", e)
else:
    print("Données incomplètes, rien envoyé.")

client.close()
