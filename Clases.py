from datetime import date, timedelta, datetime

import Utils as util
from Utils import TIPOS_HABITACION

class Huesped:
    def __init__(self, id, nombre, apellido, documento, correo, telefono):
        self.id = id
        self.nombre = nombre
        self.apellido = apellido
        self.documento = documento
        self.correo = correo
        self.telefono = telefono
        self.reservas = []
    
    def consultar_reservas(self):
        if not self.reservas:
            print("No tienes reservas registradas.")
            return None
            
        print(f"\n===== RESERVAS DE {self.nombre.upper()} {self.apellido.upper()} =====")
        for reserva in self.reservas:
            estado = "Activa" if reserva.activa else "Finalizada"
            print(f"ID: {reserva.id} - Hab: {reserva.habitacion.numero} - {reserva.fecha_ingreso} al {reserva.fecha_salida} - ${reserva.costo_total} - {estado}")
        
        id_reserva = input("\nSeleccione una reserva por ID o Enter para continuar... ")
        if id_reserva == "":
            print("Saliendo del menú de reservas...")
            return None
        else:
            if util.validar_numero(id_reserva, "ID de reserva"):
                id_reserva = int(id_reserva)
                if id_reserva < 1:
                    print(f"ID de reserva inválido.")
                    return None
            else:
                print("ID de reserva inválido. Debe ser un número.")
                return None
            
            for reserva in self.reservas:
                if reserva.id == id_reserva:
                    print(f"\n===== Reserva Seleccionada =====")
                    print(f"ID Reserva: {reserva.id}")
                    print(f"ID Huésped: {self.id}")
                    print(f"Huésped: {self.nombre} {self.apellido}")
                    print(f"Documento: {self.documento}")
                    print(f"Habitación: {reserva.habitacion.numero} ({reserva.habitacion.tipo})")
                    print(f"Fecha ingreso: {reserva.fecha_ingreso}")
                    print(f"Fecha salida: {reserva.fecha_salida}")
                    print(f"Noches: {reserva.num_noches}")
                    print(f"Costo total: ${reserva.costo_total}")
                    print(f"Estado: {'Activa' if reserva.activa else 'Finalizada'}")
                    return reserva 
            print(f"No se encontró una reserva con ID {id_reserva}.")
            return None

class Habitacion:
    def __init__(self, numero, tipo, precio_noche):
        self.numero = numero
        self.tipo = tipo
        self.precio_noche = precio_noche
        self.disponible = True
    
    def info_habitacion(self):
        return f"Hab. {self.numero} ({self.tipo}) - ${self.precio_noche}/noche - {'Disponible' if self.disponible else 'Ocupada'}"

class Reserva:
    def __init__(self, id_reserva, huesped, habitacion, fecha_ingreso, num_noches, activa=True):
        self.id = id_reserva
        self.huesped = huesped
        self.habitacion = habitacion
        self.fecha_ingreso = fecha_ingreso
        self.num_noches = num_noches
        self.fecha_salida = (datetime.strptime(fecha_ingreso, "%Y-%m-%d").date() + timedelta(days=num_noches)).strftime("%Y-%m-%d")
        self.activa = activa
        self.costo_total = self.calcular_costo()

    def calcular_costo(self):
        return self.habitacion.precio_noche * self.num_noches 
    
class Comprobante:
    def __init__(self, reserva):
        self.reserva = reserva
        self.detalles = self.generar_detalles()
    
    def generar_detalles(self):
        return f"""
        COMPROBANTE DE RESERVA - ID: {self.reserva.id}
        Huésped: {self.reserva.huesped.nombre} {self.reserva.huesped.apellido}
        id: {self.reserva.huesped.id}
        Habitación: {self.reserva.habitacion.numero} ({self.reserva.habitacion.tipo})
        Fecha de ingreso: {self.reserva.fecha_ingreso}
        Noches: {self.reserva.num_noches}
        Costo total: ${self.reserva.costo_total}
        """

class Factura:
    def __init__(self, reserva):
        self.reserva = reserva
        self.detalles = self.generar_detalles()
    
    def generar_detalles(self):
        return f"""
        FACTURA - ID Reserva: {self.reserva.id}
        Huésped: {self.reserva.huesped.nombre} {self.reserva.huesped.apellido}
        id: {self.reserva.huesped.id}
        Habitación: {self.reserva.habitacion.numero}
        Fecha de ingreso: {self.reserva.fecha_ingreso}
        Fecha de salida: {date.today()}
        Noches: {self.reserva.num_noches}
        Total pagado: ${self.reserva.costo_total}
        """

class SistemaHotel:
    def __init__(self):
        self.huespedes = []
        self.next_huesped_id = 1
        self.habitaciones = [
            Habitacion(101, "sencilla", 50),
            Habitacion(102, "sencilla", 50),
            Habitacion(201, "doble", 80),
            Habitacion(202, "doble", 80),
            Habitacion(301, "suite", 150),
            Habitacion(302, "suite", 150)
        ]
        self.reservas = []
        self.next_reserva_id = 1
        self.usuarios_admin = {"admin": "admin123","luna": "luna123"}
        self.tipos_habitacion = TIPOS_HABITACION
    
    def consultar_huespedes(self):
        if not self.huespedes:
            print("No hay huéspedes registrados.")
            return None
        
        print("\n===== LISTA DE HUÉSPEDES =====")
        for huesped in self.huespedes:
            num_reservas_activas = len([r for r in huesped.reservas if r.activa])
            print(f"ID: {huesped.id} - {huesped.nombre} {huesped.apellido} - Doc: {huesped.documento} - Email: {huesped.correo} - Reservas activas: {num_reservas_activas}")
        
        id_huesped = input("\nSeleccione un huésped por ID o Enter para continuar... ")
        if id_huesped == "":
            print("Saliendo del menú de huéspedes...")
            return None
        else:
            if util.validar_numero(id_huesped, "ID de huésped"):
                id_huesped = int(id_huesped)
                if id_huesped < 1:
                    print(f"ID de huésped inválido.")
                    return None
            else:
                print("ID de huésped inválido. Debe ser un número.")
                return None
            
            for huesped in self.huespedes:
                if huesped.id == id_huesped:
                    print(f"\n===== Huésped Seleccionado =====")
                    print(f"ID: {huesped.id}")
                    print(f"Nombre: {huesped.nombre} {huesped.apellido}")
                    print(f"Documento: {huesped.documento}")
                    print(f"Email: {huesped.correo}")
                    print(f"Teléfono: {huesped.telefono}")
                    print(f"Total de reservas: {len(huesped.reservas)}")
                    print(f"Reservas activas: {len([r for r in huesped.reservas if r.activa])}")
                    return huesped
            
            print(f"No se encontró un huésped con ID {id_huesped}.")
            return None
    
    # Funciones principales
    def registrar_huesped(self, nombre=None, apellido=None, documento=None, correo=None, telefono=None):
        
        if not (nombre and apellido and documento and correo and telefono):
            
            nombre = util.pedir_nombre()
            apellido = util.pedir_apellido()
            documento = util.pedir_documento()
            correo = util.pedir_correo()
            telefono = util.pedir_telefono()
            
        else:
            if (not util.validar_nombre_apellido(nombre) or 
                not util.validar_nombre_apellido(apellido) or
                not util.validar_documento(documento) or
                not util.validar_correo(correo) or
                not util.validar_telefono(telefono)):
                return False
        
        id = self.next_huesped_id
        self.next_huesped_id += 1
        
        for huesped in self.huespedes:
            if huesped.documento == documento:
                print("Ya existe un huésped con ese documento.")
                return False
        
        nuevo_huesped = Huesped(id, nombre.lower(), apellido, documento, correo, telefono)
        self.huespedes.append(nuevo_huesped)
        print(f"Huésped registrado exitosamente: {nuevo_huesped.nombre} {nuevo_huesped.apellido} (ID: {nuevo_huesped.id})")
        return nuevo_huesped
    
    def realizar_reserva(self, huesped, tipo_habitacion=None, fecha_ingreso=None, num_noches=None):
        if not huesped:
            print("Debe ingresar un huésped válido.")
            return False
        
        if not (tipo_habitacion and fecha_ingreso and num_noches):
            fecha_ingreso = util.pedir_fecha()
            while True:
                input_noches = input("Número de noches: ")
                if util.validar_numero(input_noches, "Número de noches"):
                    num_noches = int(input_noches)
                    if num_noches > 0:
                        break
        else:
            num_noches = int(num_noches)
            if not util.validar_fecha(fecha_ingreso) or not util.validar_numero(num_noches, "Número de noches") or not num_noches > 0:
                return False

        # Mostrar habitaciones disponibles
        habitaciones_disponibles = {}
        for habitacion in self.habitaciones:
            if habitacion.disponible:
                print(habitacion.info_habitacion())
                habitaciones_disponibles[habitacion.numero] = habitacion
        
        if habitaciones_disponibles:
            numeros_disponibles = list(habitaciones_disponibles.keys())
            print(f"Habitaciones disponibles: {numeros_disponibles}")
            while True:
                numero_habitacion = input("Ingrese el número de habitación: ")
                numero_habitacion = util.validar_numero(numero_habitacion, "Número de habitación")
                if numero_habitacion:
                    if numero_habitacion in habitaciones_disponibles:
                        habitacion_reservada = habitaciones_disponibles[numero_habitacion]
                        break
                    else:
                        print(f"Número de habitación inválido. Debe ser uno de {numeros_disponibles}")
        else:
            print("No hay habitaciones disponibles")
            return False
        
        # Crear reserva
        nueva_reserva = Reserva(
            self.next_reserva_id,
            huesped,
            habitacion_reservada,  # Corregido el nombre de la variable
            fecha_ingreso,
            num_noches
        )
        huesped.reservas.append(nueva_reserva)  # Agregar reserva al huésped
        habitacion_reservada.disponible = False
        self.reservas.append(nueva_reserva)
        self.next_reserva_id += 1
        return nueva_reserva
    
    def generar_comprobante(self, reserva):
        return Comprobante(reserva)
    
    def registrar_salida(self, reserva):
        reserva.activa = False
        reserva.habitacion.disponible = True
        return Factura(reserva)
    
    def autenticar_usuario(self, usuario, contrasena):
        return self.usuarios_admin.get(usuario) == contrasena
    
    def generar_reportes(self):
        reportes = {}
        reportes["total_huespedes"] = len(self.huespedes)
        
        habitaciones_ocupadas = sum(1 for h in self.habitaciones if not h.disponible)
        reportes["habitaciones_ocupadas"] = habitaciones_ocupadas
        reportes["habitaciones_disponibles"] = len(self.habitaciones) - habitaciones_ocupadas
        
        reservas_activas = [r for r in self.reservas if r.activa]
        reportes["reservas_activas"] = len(reservas_activas)
        
        ingresos = sum(r.costo_total for r in reservas_activas)
        reportes["ingresos"] = ingresos
        
        noches = sum(r.num_noches for r in reservas_activas)
        reportes["tiempo_promedio_estancia"] = noches / len(reservas_activas) if reservas_activas else 0
        
        return reportes
    
    def buscar_huesped(self):
        # Búsqueda por ID, Nombre o Documento
        # Menú de Búsqueda
        print("\n======= Buscar huésped =======")
        print(30*"=")
        print("Seleccione el tipo de búsqueda:")
        print("1. Buscar por ID")
        print("2. Buscar por Nombre")  # Listar si hay más de 1 huésped con el mismo nombre
        print("3. Buscar por Documento")
        print("Enter para salir")
        opcion_busqueda = input("Seleccione una opción: ")
        print(30*"=")
        
        if opcion_busqueda not in ["1", "2", "3", ""]:  # Si ingresa una opción fuera de rango termina la ejecución
            print("Opción inválida. Saliendo del menú de búsqueda...")
            return None
        
        huesped_encontrado = None  # Variable para almacenar el huésped encontrado o None si no se encuentra
        
        # Switch case para manejar las opciones de búsqueda
        match opcion_busqueda:
            case "1":
                # Búsqueda por ID
                while True:  # Ciclo para el correcto ingreso del ID
                    id = input("Ingrese el ID del huésped: ")
                    id  = util.validar_numero(id, "ID")
                    if id:  # Si el ID es válido
                        break  # Salir del ciclo si el ID es válido
                for huesped in self.huespedes:  # Recorrer el array de huéspeds
                    if huesped.id == id:  # Buscar coincidencia
                        huesped_encontrado = huesped  # Guardar el huésped encontrado
                        # Imprimir los detalles del huésped encontrado
                        print(f"Huésped encontrado: ID: {huesped.id}, Nombre: {huesped.nombre}, Documento: {huesped.documento}")
                if not huesped_encontrado:  # Si no se encontró el huésped, informar al usuario
                    print(f"No se encontró un huésped con ID {id}.")
                    return None
            
            case "2":
                # Búsqueda por Nombre
                while True:
                    nombre = input("Ingrese el nombre del huésped: ")
                    if util.validar_nombre_apellido(nombre):
                        break
                
                huespedes_con_nombre = []  # Lista para almacenar todos los huéspedes con ese nombre
                
                for huesped in self.huespedes:
                    if huesped.nombre.lower() == nombre.lower():
                        huespedes_con_nombre.append(huesped)
                
                if not huespedes_con_nombre:
                    print(f"No se encontró ningún huésped con nombre {nombre}.")
                    return None
                elif len(huespedes_con_nombre) == 1:
                    # Si solo hay uno, lo devuelve directamente
                    huesped_encontrado = huespedes_con_nombre[0]
                    print(f"Huésped encontrado: ID: {huesped_encontrado.id}, Nombre: {huesped_encontrado.nombre}, Documento: {huesped_encontrado.documento}")
                else:
                    # Si hay varios, muestra la lista para seleccionar
                    print(f"\nSe encontraron {len(huespedes_con_nombre)} huéspedes con el nombre {nombre}:")
                    print(30*"-")
                    for i, huesped in enumerate(huespedes_con_nombre, 1):
                        print(f"{i}. ID: {huesped.id}, Documento: {huesped.documento}")
                    print(30*"-")
                    
                    # Pedir selección del huésped específico
                    while True:
                        seleccion = input("Seleccione el número del huésped que desea (o Enter para cancelar): ")
                        if seleccion == "":
                            print("Búsqueda cancelada.")
                            return None
                        if seleccion.isdigit() and 1 <= int(seleccion) <= len(huespedes_con_nombre):
                            huesped_encontrado = huespedes_con_nombre[int(seleccion)-1]
                            print(f"\nHuésped seleccionado: ID: {huesped_encontrado.id}, Nombre: {huesped_encontrado.nombre}, Documento: {huesped_encontrado.documento}")
                            break
                        else:
                            print("Opción inválida. Intente nuevamente.")
            
            case "3":
                # Búsqueda por Documento
                while True:
                    documento = input("Ingrese el documento del huésped: ")
                    if util.validar_documento(documento):
                        break
                    if huesped.documento == documento:
                        huesped_encontrado = huesped
                        print(f"Huésped encontrado: ID: {huesped.id}, Nombre: {huesped.nombre}, Documento: {huesped.documento}")
                        print(f"Huésped encontrado: ID: {huesped.id}, Nombre: {huesped.nombre}, Documento: {huesped.documento}")
                if not huesped_encontrado:
                    print(f"No se encontró un huésped con documento {documento}.")
                    return None
            
            case "":
                print("Saliendo del menú de búsqueda...")
                return None
        
        return huesped_encontrado  # Objeto huésped encontrado
        
    def visualizar_reservas(self):
        if not self.reservas:
            print("No hay reservas registradas.")
            return None
        
        print("\n===== TODAS LAS RESERVAS =====")
        for reserva in self.reservas:
            estado = "Activa" if reserva.activa else "Finalizada"
            print(f"ID: {reserva.id} - Huésped: {reserva.huesped.nombre} {reserva.huesped.apellido} - Hab: {reserva.habitacion.numero} - {reserva.fecha_ingreso} al {reserva.fecha_salida} - ${reserva.costo_total} - {estado}")
        
        id_reserva = input("\nSeleccione una reserva por ID o Enter para continuar... ")
        if id_reserva == "":
            print("Saliendo del menú de reservas...")
            return None
        else:
            if util.validar_numero(id_reserva, "ID de reserva"):
                id_reserva = int(id_reserva)
                if id_reserva < 1:
                    print(f"ID de reserva inválido.")
                    return None
            else:
                print("ID de reserva inválido. Debe ser un número.")
                return None
            
            for reserva in self.reservas:
                if reserva.id == id_reserva:
                    print(f"\n===== Reserva Seleccionada =====")
                    print(f"ID: {reserva.id}")
                    print(f"Huésped: {reserva.huesped.nombre} {reserva.huesped.apellido} (ID: {reserva.huesped.id})")
                    print(f"Documento: {reserva.huesped.documento}")
                    print(f"Email: {reserva.huesped.correo}")
                    print(f"Habitación: {reserva.habitacion.numero} ({reserva.habitacion.tipo})")
                    print(f"Precio por noche: ${reserva.habitacion.precio_noche}")
                    print(f"Fecha ingreso: {reserva.fecha_ingreso}")
                    print(f"Fecha salida: {reserva.fecha_salida}")
                    print(f"Noches: {reserva.num_noches}")
                    print(f"Costo total: ${reserva.costo_total}")
                    print(f"Estado: {'Activa' if reserva.activa else 'Finalizada'}")
                    return reserva
            
            print(f"No se encontró una reserva con ID {id_reserva}.")
            return None
        
    def visualizar_habitaciones(self):
        if not self.habitaciones:
            print("No hay habitaciones registradas.")
            return None
        
        print("\n===== LISTA DE HABITACIONES =====")
        for habitacion in self.habitaciones:
            print(habitacion.info_habitacion())
        
        numero_habitacion = input("\nSeleccione una habitación por número o Enter para continuar... ")
        if numero_habitacion == "":
            return
        else:
            numero_habitacion = util.validar_numero(numero_habitacion, "Número de habitación")
            if numero_habitacion:
                for habitacion in self.habitaciones:
                    if habitacion.numero == numero_habitacion:
                        print(f"\n===== Habitación Seleccionada =====")
                        print(f"Número: {habitacion.numero}")
                        print(f"Tipo: {habitacion.tipo}")
                        print(f"Precio por noche: ${habitacion.precio_noche}")
                        print(f"Estado: {'Disponible' if habitacion.disponible else 'Ocupada'}")
                        return habitacion
