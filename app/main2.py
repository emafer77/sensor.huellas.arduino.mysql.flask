# archivo: arduino_communication.py
import serial
import time

def enviar_a_arduino(comando, id_usuario):
    
    
    # Configura la conexión serial (ajusta 'COM8' al puerto correcto)
    arduino = serial.Serial('COM8', 9600, timeout=1)
    time.sleep(2)  # Da tiempo a Arduino para iniciar la conexión
    try:
        # Enviar datos a Arduino
        arduino.write(f"{comando},{id_usuario}\n".encode())

        # Leer la respuesta de Arduino
        while True:
            data = arduino.readline().decode().strip()
            if data:
                print("Recibido de Arduino:", data)
                # Verificar si se debe salir del bucle
                
                if "¡Almacenado!" in data:
                    return True
                elif "Las huellas dactilares no coinciden" in data:
                    return False
              
                elif "No se encontró el sensor de huellas dactilares :(" in data:
                    return False
                elif "Error de comunicación" in data:
                    return False
            if ("¡Almacenado!" in data or 
                    "Las huellas dactilares no coinciden" in data or
                    "No se encontró el sensor de huellas dactilares :(" in data or
                    "Error de comunicación"in data):
                    break
            

            time.sleep(0.1)  # Espera un poco antes de leer otra vez
    finally:
        # Cierra la conexión cuando termines
        arduino.close()

def enviar_a_abrir_arduino(comando):
    # Configura la conexión serial (ajusta 'COM8' al puerto correcto)
    arduino = serial.Serial('COM8', 9600, timeout=1)
    time.sleep(2)  # Da tiempo a Arduino para iniciar la conexión

    try:
        # Enviar datos a Arduino
        arduino.write(f"{comando}\n".encode())

        # Leer la respuesta de Arduino
        while True:
            data = arduino.readline().decode().strip()
            if data:
                print("Recibido de Arduino:", data)
                if "ID encontrado #" in data:
                    # Extraer el ID del mensaje
                    id_found = int(data.split("#")[1].strip())
                    return id_found
                if ("No se encontró el sensor de huellas dactilares :(" in data):
                    break

            time.sleep(0.1)  # Espera un poco antes de leer otra vez
    finally:
        # Cierra la conexión cuando termines
        arduino.close()
   
# Ejemplo de uso (opcional, para probar la función individualmente)
# enviar_a_arduino(1, 123)


