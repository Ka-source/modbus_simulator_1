from typing import Optional
import time
import json
from device_handler import random_operation_for_device

import device_handler

class Protocol:
    READ_COIL = "01"
    READ_HOLDING_REGISTER = "03"
    WRITE_SINGLE_COIL = "05"
    WRITE_MULTIPLE_REGISTER = "10"

    @staticmethod
    def calculate_crc(data: bytes) -> Optional[str]:
        """Zwraca obiekt data z odpowiednim kodem bytes w formie HEX (format string)"""
        if type(data) != bytes:
            return None

        crc = 0xFFFF
        for pos in data:
            crc ^= pos
            for _ in range(8):
                if crc & 0x0001:
                    crc >>= 1
                    crc ^= 0xA001
                else:
                    crc >>= 1
        # Format the CRC as a hexadecimal string, swapping the low and high bytes
        crc_low = crc & 0xFF
        crc_high = (crc >> 8) & 0xFF
        return f'{crc_low:02X}{crc_high:02X}'

    @staticmethod
    def add_crc_to_data(provided_data: str) -> str:
        """Przetwarza dane modbusowe dodając na końcu CRC. Zwraca gotowy ciąg do wysłania"""
        data = bytes.fromhex(provided_data)
        return f"{provided_data} {Protocol.calculate_crc(data)}"

    @staticmethod
    def check_crc_for_data(data):
        """Sprawdza czy CRC dla podanych danych jest prawidłowy"""
        data_in_str = str(data)
        main_package = data_in_str[:-4]
        crc_package = data_in_str[-4:]
        if crc_package.lower() == Protocol.calculate_crc(bytes.fromhex(main_package)).lower():
            return True
        else:
            return False


class Data:
    @staticmethod
    def bytes_to_hex(data):
        """Konwertuje bajty na format hex"""
        return ' '.join(f'{byte:02X}' for byte in data)

    @staticmethod
    def hex_to_bytes(hex_string):
        """Konwertuje ciąg heksadecymalny na bajty"""
        return bytes.fromhex(hex_string)

    @staticmethod
    def read_full_message(serial_port):
        """Odczytuje pełne wiadomości z portu szeregowego"""
        buffer = bytearray()
        while True:
            # Odczyt dostępnych danych
            data = serial_port.read(serial_port.in_waiting or 1)
            if data:
                buffer.extend(data)
                # Można dodać dodatkową logikę do rozpoznawania pełnych ramek
                # Przykład: jeśli wiadomość ma określoną długość
                # if len(buffer) >= expected_length:
                #     break
            else:
                if len(buffer) > 0:
                    # Jeśli nic więcej nie przychodzi, ale coś w buforze jest, przerwij
                    break
            time.sleep(0.01)  # Małe opóźnienie

        return buffer


def request_analyze(request_data):
    # print(f"Request: {request_data}")

    modbus_data = request_data.split(" ")

    if len(modbus_data) < 8:
        print("Request rejected")
        return None

    frame_slave_address = modbus_data[0]
    frame_function_code = modbus_data[1]
    frame_first_register = int(modbus_data[2] + modbus_data[3], 10)  # Konwertuj na int
    frame_number_of_registers = int(modbus_data[4] + modbus_data[5], 10)  # Konwertuj na int
    frame_only_data = modbus_data[4:-2]

    print(f"Frame first register: {frame_first_register}")

    # Konwertuj na liczby całkowite
    modbus_data_int = [int(x, 16) for x in modbus_data]

    # Pobierz dane ramki i CRC
    frame_data_bytes = bytes(modbus_data_int[:-2])
    frame_crc = ''.join(f'{x:02X}' for x in modbus_data_int[-2:])

    # Zamień bajty na szesnastkowe ciągi znaków dla druku
    frame_data_str = ' '.join(f'{x:02}' for x in modbus_data_int[6:-2])

    # Wyświetl wyniki
    # print(f"Slave Address: {frame_slave_address}")
    # print(f"Function Code: {frame_function_code}")
    # print(f"First Register: {frame_first_register}")
    # print(f"Number of Registers: {frame_number_of_registers}")
    # print(f"Data: {frame_data_str}")
    # print(f"CRC: {frame_crc}")

    calculated_crc = Protocol.calculate_crc(frame_data_bytes)

    if frame_crc == calculated_crc:
        pass
    else:
        print(f"CRC error. Should be: {calculated_crc}")

    # Analiza ramki
    if frame_function_code == "03":
        response = prepare_response_holding_register(
            slave_address=int(frame_slave_address),
            first_register=frame_first_register,
            number_of_registers=frame_number_of_registers
        )
        if response:
            print(f"Response: {response}")
            return response


def prepare_response_holding_register(slave_address: int, first_register: int, number_of_registers: int) -> Optional[str]:
    device_handler.random_operation_for_device(slave_address)

    # Zamień adres na string, ponieważ klucze w JSON są stringami
    address_str = str(slave_address)
    # print(f"addr: {address_str}")

    # Wczytaj plik JSON
    with open('config/devices.json', 'r') as file:
        devices = json.load(file)
        # print(devices)

    # Sprawdź, czy adres istnieje w danych
    if address_str not in devices:
        print("Device address not found")
        return None

    device_data = devices[address_str]
    print(f"dev: {device_data}")

    # Przygotuj dane odpowiedzi
    response = [slave_address, 0x03,
                number_of_registers * 2]  # Slave address + Function code 0x03 (Read Holding Registers)
    print(f"First register: {first_register}")
    # Dodaj wartości rejestrów
    for register in range(first_register, first_register + number_of_registers):
        print(register)
        register_value = device_data.get(str(register), "0000")
        response.extend([int(register_value[i:i+2], 16) for i in range(0, len(register_value), 2)])

    # Konwertuj listę odpowiedzi na bajty
    response_bytes = bytes(response)

    # Oblicz CRC
    crc = Protocol.calculate_crc(response_bytes)
    if crc is None:
        print("CRC calculation failed")
        return None

    # Dodaj CRC do odpowiedzi
    response_hex = ''.join(f'{byte:02X}' for byte in response_bytes) + crc
    return response_hex

# Przykładowe wywołanie funkcji
# print(prepare_response_holding_register(1, 5, 2))  # Odpowiedź dla rejestrów 5 i 10
