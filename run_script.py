import modbus_init
import modbus_reader
from modbus_reader import Data
from modbus_init import serial_init, send_message


# Definicja pierwszej funkcji asynchronicznej, która działa cyklicznie
def modbus_handler():
    serial_object = modbus_init.serial_init()
    while True:
        print("Init modbus_handler()")
        message = Data.read_full_message(serial_object)
        hex_message = message.hex(sep=" ")
        if message:
            print(f"Request: {hex_message}")
            response = modbus_reader.request_analyze(hex_message)
            response_bytes = bytes.fromhex(response)
            print(f"Response: {response}")
            modbus_init.send_message(serial_port=serial_object,
                                     message_bytes=response_bytes)


if __name__ == "__main__":
    modbus_handler()
