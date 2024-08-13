import json
import random


def increase_energy_by_random_value(address, step):
    # Wczytaj plik JSON
    with open('config/devices.json', 'r') as file:
        devices = json.load(file)

    # Zamień adres na string, ponieważ klucze w JSON są stringami
    address_str = str(address)

    # Sprawdź, czy adres istnieje w danych
    if address_str in devices:
        device_data = devices[address_str]

        # Pobierz wartości rejestrów "10" i "11"
        energy_10_hex = device_data.get("10", "0000")
        energy_11_hex = device_data.get("11", "0000")

        # Konwertuj wartości HEX na DEC
        energy_10_dec = int(energy_10_hex, 16)
        energy_11_dec = int(energy_11_hex, 16)

        # Wygeneruj losową wartość do zwiększenia (od 0 do step)
        random_increase = random.randint(0, step)

        # Zwiększ wartości DEC o losową wartość
        new_energy_10_dec = energy_10_dec + random_increase
        new_energy_11_dec = energy_11_dec + random_increase

        # Konwertuj nowe wartości DEC na HEX (upewnij się, że mają 4 cyfry)
        new_energy_10_hex = format(new_energy_10_dec, '04X')
        new_energy_11_hex = format(new_energy_11_dec, '04X')

        # Zaktualizuj wartości w urządzeniu
        device_data["10"] = new_energy_10_hex
        device_data["11"] = new_energy_11_hex

        # Zapisz zmienione dane z powrotem do pliku JSON
        with open('config/devices.json', 'w') as file:
            json.dump(devices, file, indent=4)

        return new_energy_10_hex, new_energy_11_hex
    else:
        return None  # Lub możesz zwrócić domyślną wartość, jeśli adres nie istnieje


def return_energy(address):
    # Wczytaj plik JSON
    with open('config/devices.json', 'r') as file:
        devices = json.load(file)

    # Zamień adres na string, ponieważ klucze w JSON są stringami
    address_str = str(address)

    # Sprawdź, czy adres istnieje w danych
    if address_str in devices:
        device_data = devices[address_str]
        # Pobierz wartości rejestrów "10" i "11"
        energy_10 = device_data.get("10", "0000")
        energy_11 = device_data.get("11", "0000")

        combined_hex = energy_10 + energy_11
        combined_dec = int(combined_hex, 16)

        return combined_dec
    else:
        return None  # Lub możesz zwrócić domyślną wartość, jeśli adres nie istnieje


def set_voltage_to_random_value(address):
    # Wczytaj plik JSON
    with open('config/devices.json', 'r') as file:
        devices = json.load(file)


    # Zamień adres na string, ponieważ klucze w JSON są stringami
    address_str = str(address)

    # Sprawdź, czy adres istnieje w danych
    if address_str in devices:
        device_data = devices[address_str]

        # Generuj losową wartość całkowitą w zakresie 224-238
        random_value = random.randint(224, 238)

        # Konwertuj wartość na HEX i upewnij się, że ma 4 cyfry (wypełniając zerami, jeśli potrzeba)
        voltage_hex = format(random_value, '04X')

        # Ustaw nową wartość w rejestrze "5"
        device_data["5"] = voltage_hex

        # Zapisz zmienione dane z powrotem do pliku JSON
        with open('config/devices.json', 'w') as file:
            json.dump(devices, file, indent=4)

        return voltage_hex
    else:
        return None  # Lub możesz zwrócić domyślną wartość, jeśli adres nie istnieje


def return_voltage(address):
    # Wczytaj plik JSON
    with open('config/devices.json', 'r') as file:
        devices = json.load(file)

    # Zamień adres na string, ponieważ klucze w JSON są stringami
    address_str = str(address)

    # Sprawdź, czy adres istnieje w danych
    if address_str in devices:
        device_data = devices[address_str]
        # Pobierz wartość rejestru "5"
        voltage_hex = device_data.get("5", "0000")

        # Konwertuj wartość HEX na DEC
        voltage_dec = int(voltage_hex, 16)

        return voltage_dec
    else:
        return None  # Lub możesz zwrócić domyślną wartość, jeśli adres nie istnieje


def return_registers(slave_address, registers):
    pass


def random_operation_for_device(address):
    set_voltage_to_random_value(address)
    increase_energy_by_random_value(address, 7)
