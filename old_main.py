import serial
import time

# Konfiguracja portu szeregowego
port = 'COM4'
baud_rate = 9600
parity = serial.PARITY_EVEN
stop_bits = serial.STOPBITS_ONE

# Inicjalizacja portu szeregowego
ser = serial.Serial(
    port=port,
    baudrate=baud_rate,
    parity=parity,
    stopbits=stop_bits,
    timeout=0.1  # Krótki timeout na oczekiwanie
)

# Sprawdzenie, czy port jest otwarty
if ser.is_open:
    print(f"Port {port} otwarty.")
else:
    print(f"Port {port} nie mógł zostać otwarty.")
    exit()


def bytes_to_hex(data):
    """Konwertuje bajty na format hex"""
    return ' '.join(f'{byte:02X}' for byte in data)


def hex_to_bytes(hex_string):
    """Konwertuje ciąg heksadecymalny na bajty"""
    return bytes.fromhex(hex_string)


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


def send_message(serial_port, message_bytes):
    """Wysyła wiadomość przez port szeregowy"""
    serial_port.write(message_bytes)

try:
    while True:
        send_message(ser, hex_to_bytes("02 04 00 01 00 01 60 39"))  # READ SENSOR
        # send_message(ser, hex_to_bytes("01 03 01 00 00 02 C5 F7"))  # READ METER
        # send_message(ser, hex_to_bytes("01 06 01 01 00 02 58 37")) # WRITE
        message = read_full_message(ser)
        if message:
            hex_message = bytes_to_hex(message)
            print("Odebrano (Hex):", hex_message)
            time.sleep(2)
            if hex_message == "01 03 10 00 00 01 80 CA":
                # Ramka do wysłania
                response_hex = "01 03 02 00 09 78 42"
                response_bytes = hex_to_bytes(response_hex)
                send_message(ser, response_bytes)
                print("Wysłano (Hex):", bytes_to_hex(response_bytes))
except KeyboardInterrupt:
    print("Przerwano przez użytkownika.")
finally:
    ser.close()
    print("Port szeregowy zamknięty.")
