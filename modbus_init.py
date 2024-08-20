import serial


def serial_init():
    # Konfiguracja portu szeregowego
    port = '/dev/ttyUSB0'
    baud_rate = 9600
    parity = serial.PARITY_EVEN
    stop_bits = serial.STOPBITS_ONE

    # Inicjalizacja portu szeregowego
    serial_object = serial.Serial(
        port=port,
        baudrate=baud_rate,
        parity=parity,
        stopbits=stop_bits,
        timeout=0.1  # Krótki timeout na oczekiwanie
    )

    # Sprawdzenie, czy port jest otwarty
    if serial_object.is_open:
        print(f"Port {port} otwarty.")
    else:
        print(f"Port {port} nie mógł zostać otwarty.")
        exit()

    return serial_object


def send_message(serial_port, message_bytes):
    """Wysyła wiadomość przez port szeregowy"""
    serial_port.write(message_bytes)
