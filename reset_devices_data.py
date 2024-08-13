import json

import device_handler
from device_handler import set_voltage_to_random_value


def do_reset():
    file_path = 'config/devices.json'

    # Wczytaj dane z pliku JSON
    with open(file_path, 'r') as file:
        devices = json.load(file)

    # Przejdź przez wszystkie urządzenia i zaktualizuj rejestry 10 i 11
    for address, registers in devices.items():
        registers['5'] = device_handler.set_voltage_to_random_value(address)
        registers['10'] = '0000'
        registers['11'] = '0000'

    # Zapisz zaktualizowane dane z powrotem do pliku JSON
    with open(file_path, 'w') as file:
        json.dump(devices, file, indent=4)

    print("Reset completed.")


# Wywołanie funkcji do_reset
do_reset()
