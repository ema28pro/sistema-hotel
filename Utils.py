import datetime

TIPOS_HABITACION = ["sencilla", "doble", "suite"]

def validar_texto(texto: str, tipo: str = None):
    if tipo:
        advertencia = f"El {tipo} debe ser valido y no debe contener números ni símbolos ni espacios."
    else:
        advertencia = "Debe ser valido y no debe contener números ni símbolos ni espacios."
    
    if texto.isdigit() or not texto.isalpha():
        print(advertencia)
        return False
    else:
        return True

def validar_numero(numero: str, tipo: str = None):
    if tipo:
        advertencia = f"El {tipo} debe ser un número válido, sin espacios."
    else:
        advertencia = "Debe ser un número válido, sin espacios."
    
    if isinstance(numero, int):
        return numero
    elif isinstance(numero, float):
        return int(numero)
    elif numero.isalpha() or not numero.isdigit():
        print(advertencia)
        return False
    else:
        return int(numero)

def validar_nombre_apellido(texto: str):
    # if len(texto) < 3 and  texto.replace(" ","").isdigit() or not texto.replace(" ","").isalpha():
    if len(texto) < 3 or texto.isdigit() or not texto.isalpha():
        print("El Nombre y Apellido deben ser validos y no debe contener números ni símbolos.") # Imprime advertencia
        return False
    else:
        return True

def validar_documento(documento: str):
    if 3 <= len(documento) <= 15 and documento.isdigit():
        return True
    else:
        print("El documento debe tener entre 3 y 15 dígitos y no debe contener letras ni símbolos.")
        return False

def validar_correo(email: str):
    if "@" not in email or ".com" not in email or ".co" not in email or " " in email:
        print("El correo electrónico no debe tener espacios y debe contener '@' y '.'")
        return False
    else:
        return True

def validar_telefono(telefono: str):
    if not telefono.isdigit() or telefono.isalpha():
        print("El teléfono no debe contener letras ni símbolos.")
        return False
    elif 7 <= len(telefono) <= 15:
        return True
    else:
        print("El teléfono debe tener entre 7 y 15 dígitos.")
        return False

def validar_fecha(fecha: str):
    try:
        fecha_dt = datetime.datetime.strptime(fecha, "%Y-%m-%d").date()
        if fecha_dt < datetime.date.today():
            print("La fecha de ingreso no puede ser anterior a la fecha actual.")
            return False
        else:
            return True
    except Exception as e:
        print(f"Formato de fecha inválido. Use YYYY-MM-DD: {str(e)}")
        return False

def pedir_fecha():
    while True:
        fecha = input("Fecha de ingreso (YYYY-MM-DD): ")
        if validar_fecha(fecha):
            return fecha

def pedir_nombre():
    while True:
        nombre = input("Nombre: ")
        if validar_nombre_apellido(nombre):
            return nombre

def pedir_apellido():
    while True:
        apellido = input("Apellido: ")
        if validar_nombre_apellido(apellido):
            return apellido

def pedir_documento():
    while True:
        documento = input("Documento: ")
        if validar_documento(documento):
            return documento

def pedir_correo():
    while True:
        correo = input("Correo electrónico: ")
        if validar_correo(correo):
            return correo

def pedir_telefono():
    while True:
        telefono = input("Teléfono: ")
        if validar_telefono(telefono):
            return telefono

def pedir_tipo_habitacion():
    print("Tipos de habitación disponibles:", ", ".join(TIPOS_HABITACION))
    while True:
        tipo = input("Tipo de habitación: ").lower()
        if validar_texto(tipo, "tipo de habitación"):
            if tipo in TIPOS_HABITACION:
                return tipo
            else:
                print(f"Tipo de habitación inválido. Debe ser uno de ({', '.join(TIPOS_HABITACION)})")

# print(pedir_tipo_habitacion())