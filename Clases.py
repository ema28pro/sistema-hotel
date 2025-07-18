from datetime import date, timedelta, datetime
import csv
import Utils as util
from Utils import TIPOS_HABITACION
import matplotlib.pyplot as plt

REGISTRO_ENTRADAS = "registros/entradas.csv"
REGISTRO_CHECKOUTS = "registros/checkouts.csv"
REGISTRO_INGRESOS_CAJA = "registros/ingresos_caja.csv"
REGISTRO_HISTORIAL_RESERVAS = "registros/historial_reservas.csv"
REGISTRO_HUESPEDES = "registros/huespedes.csv"

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
            if reserva.activa is None:
                estado = "Finalizada"
            elif reserva.activa is True:
                estado = "Activa"
            else:  # reserva.activa is False
                estado = "Pendiente de entrada"
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
                    if reserva.activa is None:
                        estado = "Finalizada"
                    elif reserva.activa is True:
                        estado = "Activa"
                    else:  # reserva.activa is False
                        estado = "Pendiente de entrada"
                    print(f"Estado: {estado}")
                    return reserva 
            print(f"No se encontró una reserva con ID {id_reserva}.")
            return None

class Habitacion:
    def __init__(self, numero, tipo, precio_noche):
        self.numero = numero
        self.tipo = tipo
        self.precio_noche = precio_noche
        self.reservas_activas = []  # Lista de reservas activas para verificar disponibilidad por fechas
    
    def esta_disponible_en_fechas(self, fecha_ingreso, fecha_salida):
        """
        Verifica si la habitación está disponible en el rango de fechas especificado
        """
        fecha_ingreso_dt = datetime.strptime(fecha_ingreso, "%Y-%m-%d").date()
        fecha_salida_dt = datetime.strptime(fecha_salida, "%Y-%m-%d").date()
        
        for reserva in self.reservas_activas:
            if reserva.activa is None:  # Saltar reservas finalizadas (cliente registró salida)
                continue
                
            reserva_ingreso = datetime.strptime(reserva.fecha_ingreso, "%Y-%m-%d").date()
            reserva_salida = datetime.strptime(reserva.fecha_salida, "%Y-%m-%d").date()
            
            # Verificar si hay solapamiento de fechas
            if not (fecha_salida_dt <= reserva_ingreso or fecha_ingreso_dt >= reserva_salida):
                return False
        
        return True
    
    def agregar_reserva(self, reserva):
        """Agrega una reserva a la lista de reservas activas de la habitación"""
        self.reservas_activas.append(reserva)
    
    def liberar_reserva(self, reserva):
        """Marca una reserva como inactiva (no la elimina para mantener historial)"""
        if reserva in self.reservas_activas:
            reserva.activa = False
    
    def info_habitacion(self):
        # Obtener reservas activas (incluyendo pendientes de entrada pero excluyendo finalizadas)
        reservas_activas = [r for r in self.reservas_activas if r.activa is not None]
        
        if reservas_activas:
            info = f"Hab. {self.numero} ({self.tipo}) - ${self.precio_noche}/noche - {len(reservas_activas)} reserva(s):"
            for i, reserva in enumerate(reservas_activas, 1):
                estado = "Activa" if reserva.activa else "Pendiente de entrada"
                info += f"\n    {i}. {reserva.fecha_ingreso} al {reserva.fecha_salida} ({reserva.huesped.nombre} {reserva.huesped.apellido}) - {estado}"
            return info
        else:
            return f"Hab. {self.numero} ({self.tipo}) - ${self.precio_noche}/noche - Disponible"

class Reserva:
    def __init__(self, id_reserva, huesped, habitacion, fecha_ingreso, num_noches, activa=False):
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
        self.efectivo = 0.0
    
    def consultar_huespedes(self):
        if not self.huespedes:
            print("No hay huéspedes registrados.")
            return None
        
        print("\n===== LISTA DE HUÉSPEDES =====")
        for huesped in self.huespedes:
            num_reservas_activas = len([r for r in huesped.reservas if r.activa is True])
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
                    print(f"Reservas activas: {len([r for r in huesped.reservas if r.activa is True])}")
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
    
    def realizar_reserva(self, huesped, fecha_ingreso=None, num_noches=None, numero_habitacion=None):
        if not huesped:
            print("Debe ingresar un huésped válido.")
            return False
        
        # Si no se proporcionan todos los parámetros, pedirlos al usuario
        if fecha_ingreso is None or num_noches is None:
            fecha_ingreso = util.pedir_fecha()
            while True:
                input_noches = input("Número de noches: ")
                if util.validar_numero(input_noches, "Número de noches"):
                    num_noches = int(input_noches)
                    if num_noches > 0:
                        break
        else:
            # Validar parámetros proporcionados
            if not util.validar_fecha(fecha_ingreso):
                print("Fecha de ingreso inválida.")
                return False
            
            if not isinstance(num_noches, int):
                num_noches = util.validar_numero(str(num_noches), "Número de noches")
                if not num_noches:
                    return False
            
            if num_noches <= 0:
                print("El número de noches debe ser mayor a 0.")
                return False

        # Consultar disponibilidad usando la función existente (modo silencioso)
        habitaciones_disponibles = self.consultar_disponibilidad(fecha_ingreso, num_noches, mostrar_info=False)
        
        # Si no hay habitaciones disponibles, finalizar
        if not habitaciones_disponibles:
            print("❌ No se puede realizar la reserva. No hay habitaciones disponibles.")
            print(f"   Para las fechas del {fecha_ingreso} (por {num_noches} noches)")
            return False
        
        # Si se especifica un número de habitación, validar que esté en la lista de disponibles
        if numero_habitacion is not None:
            habitacion_reservada = None
            for habitacion in habitaciones_disponibles:
                if habitacion.numero == numero_habitacion:
                    habitacion_reservada = habitacion
                    break
            
            if not habitacion_reservada:
                print(f"❌ La habitación {numero_habitacion} no está disponible para las fechas solicitadas.")
                return False
            
            print(f"✅ Habitación {numero_habitacion} confirmada para la reserva.")
        else:
            # Si no se especifica habitación, mostrar opciones y pedir selección
            print(f"\n📋 Habitaciones disponibles:")
            for habitacion in habitaciones_disponibles:
                print(f"   - {habitacion.info_habitacion()}")
            
            numeros_disponibles = [h.numero for h in habitaciones_disponibles]
            print(f"\nNúmeros de habitaciones disponibles: {numeros_disponibles}")
            
            # Pedir selección de habitación
            while True:
                numero_habitacion_input = input("Ingrese el número de habitación: ")
                numero_habitacion_input = util.validar_numero(numero_habitacion_input, "Número de habitación")
                if numero_habitacion_input:
                    if numero_habitacion_input in numeros_disponibles:
                        for habitacion in habitaciones_disponibles:
                            if habitacion.numero == numero_habitacion_input:
                                habitacion_reservada = habitacion
                                break
                        break
                    else:
                        print(f"Número de habitación inválido. Debe ser uno de {numeros_disponibles}")
        
        # Crear reserva
        nueva_reserva = Reserva(
            self.next_reserva_id,
            huesped,
            habitacion_reservada,
            fecha_ingreso,
            num_noches
        )
        
        # Agregar reserva al huésped y a la habitación
        huesped.reservas.append(nueva_reserva)
        habitacion_reservada.agregar_reserva(nueva_reserva)
        self.reservas.append(nueva_reserva)
        self.next_reserva_id += 1
        
        # Agregar el costo de la reserva al efectivo del hotel
        self.efectivo += nueva_reserva.costo_total
        
        self.historial_reserva(nueva_reserva)
        self.registro_ingreso_caja(nueva_reserva)
        
        print(f"🎉 Reserva realizada exitosamente!")
        print(f"ID de reserva: {nueva_reserva.id}")
        print(f"Habitación: {habitacion_reservada.numero}")
        print(f"Fechas: {nueva_reserva.fecha_ingreso} al {nueva_reserva.fecha_salida}")
        print(f"Costo total: ${nueva_reserva.costo_total}")
        print(f"💰 Efectivo del hotel: ${self.efectivo}")
        
        return nueva_reserva
    
    def generar_comprobante(self, reserva):
        return Comprobante(reserva)
    
    def registrar_entrada(self, reserva):
        if reserva.activa is None:
            print("❌ La reserva ya ah sido finalizada.")
            return
        elif reserva.activa:
            print("❌ Ya se ha registrado la entrada para esta reserva.")
            return
        else:
            reserva.activa = True
            self.registro_entrada(reserva)
            print(f"✅ Reserva {reserva.id} registrada como activa.")
    
    def registrar_salida(self, reserva):
        reserva.activa = None
        self.registro_chekout(reserva)
        reserva.habitacion.liberar_reserva(reserva)
        return Factura(reserva)
    
    def autenticar_usuario(self, usuario, contrasena):
        return self.usuarios_admin.get(usuario) == contrasena
    
    def generar_reportes(self):
        reportes = {}
        reportes["total_huespedes"] = len(self.huespedes)
        
        # Contar habitaciones con reservas activas (incluyendo pendientes de entrada)
        habitaciones_con_reservas_activas = 0
        for habitacion in self.habitaciones:
            if any(reserva.activa is not None for reserva in habitacion.reservas_activas):
                habitaciones_con_reservas_activas += 1
        
        reportes["habitaciones_con_reservas_activas"] = habitaciones_con_reservas_activas
        reportes["habitaciones_sin_reservas"] = len(self.habitaciones) - habitaciones_con_reservas_activas
        
        # Solo contar reservas realmente activas (True) para ingresos y estadísticas
        reservas_activas = [r for r in self.reservas if r.activa is True]
        reportes["reservas_activas"] = len(reservas_activas)
        
        ingresos = sum(r.costo_total for r in reservas_activas)
        reportes["ingresos"] = ingresos
        
        # Agregar efectivo total del hotel
        reportes["efectivo_total"] = self.efectivo
        
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
                    print(f"Estado: {'None' if reserva.activa is None else 'Activa' if reserva.activa else 'Inactiva'}")
                    return reserva
            
            print(f"No se encontró una reserva con ID {id_reserva}.")
            return None
        
    def visualizar_habitaciones(self, retornar_listas=False):
        if not self.habitaciones:
            print("No hay habitaciones registradas.")
            return None if not retornar_listas else ([], [])
        
        if retornar_listas:
            # Retornar listas de habitaciones disponibles y ocupadas
            habitaciones_disponibles = []
            habitaciones_ocupadas = []
            
            for habitacion in self.habitaciones:
                # Una habitación está ocupada si tiene reservas activas (activa=True)
                tiene_reservas_activas = any(r.activa is True for r in habitacion.reservas_activas)
                if tiene_reservas_activas:
                    habitaciones_ocupadas.append(habitacion)
                else:
                    habitaciones_disponibles.append(habitacion)
                    
            return habitaciones_disponibles, habitaciones_ocupadas
        else:
            print("\n===== LISTA DE HABITACIONES =====")
            for habitacion in self.habitaciones:
                print(habitacion.info_habitacion())
        

    
    def consultar_disponibilidad(self, fecha_ingreso=None, num_noches=None, mostrar_info=True):
        """
        Consulta la disponibilidad de habitaciones para un rango de fechas específico
        
        Args:
            fecha_ingreso: Fecha de ingreso en formato YYYY-MM-DD
            num_noches: Número de noches
            mostrar_info: Si True, muestra información detallada. Si False, solo retorna la lista
            
        Returns:
            Lista de habitaciones disponibles
        """
        if not fecha_ingreso:
            fecha_ingreso = util.pedir_fecha()
        
        if not num_noches:
            while True:
                input_noches = input("Número de noches: ")
                if util.validar_numero(input_noches, "Número de noches"):
                    num_noches = int(input_noches)
                    if num_noches > 0:
                        break
        
        fecha_salida = (datetime.strptime(fecha_ingreso, "%Y-%m-%d").date() + timedelta(days=num_noches)).strftime("%Y-%m-%d")
        
        # Separar habitaciones disponibles y ocupadas
        habitaciones_disponibles = []
        habitaciones_ocupadas = []
        
        for habitacion in self.habitaciones:
            if habitacion.esta_disponible_en_fechas(fecha_ingreso, fecha_salida):
                habitaciones_disponibles.append(habitacion)
            else:
                habitaciones_ocupadas.append(habitacion)
        
        # Solo mostrar información si mostrar_info es True
        if mostrar_info:
            print(f"\n===== DISPONIBILIDAD DEL {fecha_ingreso} AL {fecha_salida} =====")
            
            if habitaciones_disponibles:
                print("\n🟢 HABITACIONES DISPONIBLES:")
                for habitacion in habitaciones_disponibles:
                    print(f"  - {habitacion.info_habitacion()}")
            
            if habitaciones_ocupadas:
                print("\n🔴 HABITACIONES OCUPADAS:")
                for habitacion in habitaciones_ocupadas:
                    print(f"  - Hab. {habitacion.numero} ({habitacion.tipo}) - ${habitacion.precio_noche}/noche")
                    # Mostrar las reservas que causan el conflicto
                    for reserva in habitacion.reservas_activas:
                        if reserva.activa is not None:  # Solo reservas confirmadas (True) o pendientes de entrada (False)
                            res_ingreso = datetime.strptime(reserva.fecha_ingreso, "%Y-%m-%d").date()
                            res_salida = datetime.strptime(reserva.fecha_salida, "%Y-%m-%d").date()
                            consulta_ingreso = datetime.strptime(fecha_ingreso, "%Y-%m-%d").date()
                            consulta_salida = datetime.strptime(fecha_salida, "%Y-%m-%d").date()
                            
                            if not (consulta_salida <= res_ingreso or consulta_ingreso >= res_salida):
                                estado_reserva = "Activa" if reserva.activa else "Pendiente de entrada"
                                print(f"    Reservada por: {reserva.huesped.nombre} {reserva.huesped.apellido} ({estado_reserva})")
                                print(f"    Del {reserva.fecha_ingreso} al {reserva.fecha_salida}")
            
            print(f"\nResumen: {len(habitaciones_disponibles)} disponibles, {len(habitaciones_ocupadas)} ocupadas")
        
        return habitaciones_disponibles
    
    def cargar_huespedes(self):
        """
        Carga los huéspedes desde el archivo CSV
        Formato esperado: nombre;apellido;documento;correo;telefono
        """
        try:
            with open(REGISTRO_HUESPEDES, "r", encoding='utf-8') as file:
                reader = csv.reader(file, delimiter=';')
                huespedes_cargados = 0
                
                for row in reader:
                    if len(row) >= 5:  # Verificar que la fila tenga todos los campos
                        nombre, apellido, documento, correo, telefono = row[:5]
                        
                        # Verificar si el huésped ya existe (por documento)
                        huesped_existe = any(h.documento == documento for h in self.huespedes)
                        
                        if not huesped_existe:
                            # Crear nuevo huésped
                            nuevo_huesped = Huesped(
                                self.next_huesped_id,
                                nombre.strip(),
                                apellido.strip(),
                                documento.strip(),
                                correo.strip(),
                                telefono.strip()
                            )
                            self.huespedes.append(nuevo_huesped)
                            self.next_huesped_id += 1
                            huespedes_cargados += 1
                        else:
                            print(f"⚠️ Huésped con documento {documento} ya existe, omitiendo...")
                
                print(f"✅ Se cargaron {huespedes_cargados} huéspedes desde el archivo CSV")
                print(f"📊 Total de huéspedes en el sistema: {len(self.huespedes)}")
                
        except FileNotFoundError:
            print(f"❌ No se encontró el archivo {REGISTRO_HUESPEDES}")
        except Exception as e:
            print(f"❌ Error al cargar huéspedes: {str(e)}")
    
    def exportar_huespedes(self):
        """
        Exporta todos los huéspedes a un archivo CSV
        Formato: nombre;apellido;documento;correo;telefono
        """
        if not self.huespedes:
            print("❌ No hay huéspedes para exportar")
            return False
        
        try:
            nombre_archivo = f"registros/huespedes_exportados_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
            with open(nombre_archivo, "w", newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter=';')
                
                # Escribir encabezados (opcional)
                # writer.writerow(['Nombre', 'Apellido', 'Documento', 'Correo', 'Telefono'])
                
                # Escribir datos de huéspedes
                for huesped in self.huespedes:
                    writer.writerow([
                        huesped.nombre,
                        huesped.apellido,
                        huesped.documento,
                        huesped.correo,
                        huesped.telefono
                    ])
            
            print(f"✅ Huéspedes exportados exitosamente a: {nombre_archivo}")
            print(f"📊 Total de huéspedes exportados: {len(self.huespedes)}")
            return True
            
        except Exception as e:
            print(f"❌ Error al exportar huéspedes: {str(e)}")
            return False

    def historial_reserva(self, reserva):
        #Fecha_ingresos;Fecha_finalizacion;Tipo_habitacion;Numero_noches;Monto_total;Documento;Huesped;
        
        fecha_ingreso = reserva.fecha_ingreso
        fecha_finalizacion = reserva.fecha_salida
        tipo_habitacion = reserva.habitacion.tipo
        numero_noches = reserva.num_noches
        monto_total = reserva.costo_total
        documento_huesped = reserva.huesped.documento
        nombre_huesped = reserva.huesped.nombre
        
        # Guardar el registro en el archivo usando CSV writer
        with open(REGISTRO_HISTORIAL_RESERVAS, "a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([fecha_ingreso, fecha_finalizacion, tipo_habitacion, numero_noches, monto_total, documento_huesped, nombre_huesped])
    
    def registro_entrada(self, reserva):
        #Fecha;Hora;Documento;Huesped;
        
        fecha = datetime.now().strftime('%Y-%m-%d') # Genera el objeto fecha y hora actual y lo convierte a fecha string
        hora = datetime.now().strftime('%H:%M:%S') # Genera el objeto fecha y hora actual y lo convierte a hora string
        documento_huesped = reserva.huesped.documento
        nombre_huesped = reserva.huesped.nombre
        
        # Guardar el registro en el archivo usando CSV writer
        with open(REGISTRO_ENTRADAS, "a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([fecha, hora, documento_huesped, nombre_huesped])
        
        print(f"{fecha} : ✓ Entrada registrada para {nombre_huesped} a las {hora}")
    
    def registro_chekout(self, reserva):
        #Fecha;Hora;Docuemento;Huesped;
        
        fecha = datetime.now().strftime('%Y-%m-%d') # Genera el objeto fecha y hora actual y lo convierte a fecha string
        hora = datetime.now().strftime('%H:%M:%S') # Genera el objeto fecha y hora actual y lo convierte a hora string
        documento_huesped = reserva.huesped.documento
        nombre_huesped = reserva.huesped.nombre
        
        # Guardar el registro en el archivo usando CSV writer
        with open(REGISTRO_CHECKOUTS, "a", newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow([fecha, hora, documento_huesped, nombre_huesped])
        
        print(f"{fecha} : ✓ Checkout registrado para {nombre_huesped} a las {hora}")

    def registro_ingreso_caja(self, reserva):
        #Fecha;Hora;Tipo;Noches;Efectivo;Documento;Nombre     
        
        fecha = datetime.now().strftime('%Y-%m-%d')
        hora = datetime.now().strftime('%H:%M:%S')
        tipo_habitacion = reserva.habitacion.tipo
        noches = reserva.num_noches
        efectivo = reserva.costo_total
        
        documento_huesped = reserva.huesped.documento
        nombre_huesped = reserva.huesped.nombre
        
        # Guardar el registro en el archivo usando CSV writer
        with open(REGISTRO_INGRESOS_CAJA, "a", newline='', encoding='utf-8') as caja_file:
            writer = csv.writer(caja_file, delimiter=';')
            writer.writerow([fecha, hora, tipo_habitacion, noches, f"{float(efectivo):,}", documento_huesped, nombre_huesped])
    
    def mostrar_graficos(self):
        print("📊 Generando gráficos...")
        
        # Agregar algunos datos de prueba si no existen reservas
        if not self.reservas:
            print("No hay datos suficientes para generar gráficos.")
            return

        # 1. Gráfico de barras - Comparación entre tipos de habitaciones ocupadas
        # Crear diccionario dinámico basado en tipos_habitacion del hotel
        habitaciones_ocupadas_por_tipo = {}
        
        # Inicializar el diccionario con los tipos disponibles
        for tipo in self.tipos_habitacion:
            habitaciones_ocupadas_por_tipo[tipo] = 0
        
        # Contar habitaciones ocupadas por tipo
        for habitacion in self.habitaciones:
            tiene_reservas_activas = any(r.activa is True for r in habitacion.reservas_activas)
            if tiene_reservas_activas:
                tipo_habitacion = habitacion.tipo.lower()
                if tipo_habitacion in habitaciones_ocupadas_por_tipo:
                    habitaciones_ocupadas_por_tipo[tipo_habitacion] += 1
        
        # Crear gráfico de barras
        tipos = list(habitaciones_ocupadas_por_tipo.keys())
        cantidades = list(habitaciones_ocupadas_por_tipo.values())
        colores = ["blue", "green", "purple"][:len(tipos)]  # Asignar colores dinámicamente
        
        plt.figure(figsize=(10, 5))
        plt.bar(tipos, cantidades, color=colores)
        plt.title("Habitaciones ocupadas por tipo")
        plt.xlabel("Tipo de habitación")
        plt.ylabel("Cantidad ocupadas")
        plt.show()

        # 2. Pie chart ocupadas vs disponibles
        habitaciones_disponibles, habitaciones_ocupadas = self.visualizar_habitaciones(retornar_listas=True)
        total_ocupadas = len(habitaciones_ocupadas)
        total_disponibles = len(habitaciones_disponibles)
        
        if total_ocupadas + total_disponibles > 0:
            plt.pie([total_ocupadas, total_disponibles], labels=["Ocupadas", "Disponibles"], autopct="%1.1f%%", colors=["red", "green"])
            plt.title("Distribución de habitaciones")
            plt.show()

        # 3. Línea: check-out por día (desde archivo de registro)
        try:
            with open(REGISTRO_CHECKOUTS, "r") as file:
                lineas = file.readlines()
            
            if lineas:
                fechas_checkout = []
                for linea in lineas:
                    if linea.strip():
                        parts = linea.strip().split(";")
                        if len(parts) >= 1:
                            fecha_str = parts[0]
                            try:
                                fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                                fechas_checkout.append(fecha)
                            except ValueError:
                                continue
                
                if fechas_checkout:
                    fechas_unicas = sorted(set(fechas_checkout))
                    conteo = [fechas_checkout.count(f) for f in fechas_unicas]
                    plt.plot(fechas_unicas, conteo, marker='o')
                    plt.title("Check-Outs por día")
                    plt.xlabel("Fecha")
                    plt.ylabel("Cantidad")
                    plt.xticks(rotation=45)
                    plt.tight_layout()
                    plt.show()
        except FileNotFoundError:
            print("Archivo de checkouts no encontrado.")
        except Exception as e:
            print(f"Error: {str(e)}")

        # 4. Barras horizontales: noches por huésped (Top 10)
        noches_huesped = []
        for reserva in self.reservas:
            nombre_completo = f"{reserva.huesped.nombre} {reserva.huesped.apellido}"
            noches_huesped.append((nombre_completo, reserva.num_noches))
        
        # Ordenar por noches descendente y tomar top 10
        noches_huesped_sorted = sorted(noches_huesped, key=lambda x: x[1], reverse=True)[:10]
        
        if noches_huesped_sorted:
            nombres = [x[0] for x in noches_huesped_sorted]
            noches = [x[1] for x in noches_huesped_sorted]
            plt.barh(nombres, noches, color="orange")
            plt.title("Top 10 huéspedes por noches")
            plt.xlabel("Noches")
            plt.gca().invert_yaxis()
            plt.tight_layout()
            plt.show()
        
        # 5. Gráfica de dispersión: noches vs valor pagado (desde historial de reservas)
        try:
            with open(REGISTRO_HISTORIAL_RESERVAS, "r") as file:
                lineas = file.readlines()
            
            if lineas:
                noches_list = []
                pagos_list = []
                
                for linea in lineas:
                    if linea.strip():
                        parts = linea.strip().split(";")
                        if len(parts) >= 5:
                            try:
                                noches = int(parts[3])  # Numero_noches
                                pago = float(parts[4])  # Monto_total
                                noches_list.append(noches)
                                pagos_list.append(pago)
                            except ValueError:
                                continue
                
                if noches_list and pagos_list:
                    plt.figure(figsize=(10, 6))
                    plt.scatter(noches_list, pagos_list, alpha=0.6, color='blue')
                    plt.title("Relación noches vs total pagado")
                    plt.xlabel("Noches")
                    plt.ylabel("Valor pagado ($)")
                    plt.grid(True, alpha=0.3)
                    plt.show()
        except FileNotFoundError:
            print("Archivo de historial de reservas no encontrado.")
        except Exception as e:
            print(f"Error: {str(e)}")

        # 6. Pie chart: ingresos por tipo de habitación (desde ingresos_caja.csv)
        try:
            with open(REGISTRO_INGRESOS_CAJA, "r") as file:
                lineas = file.readlines()
            
            if lineas:
                # Crear diccionario dinámico basado en tipos_habitacion
                ingresos_por_tipo = {}
                for tipo in self.tipos_habitacion:
                    ingresos_por_tipo[tipo] = 0
                
                for linea in lineas:
                    if linea.strip():
                        parts = linea.strip().split(";")
                        if len(parts) >= 5:
                            try:
                                tipo_habitacion = parts[2].lower()  # Tipo
                                efectivo_str = parts[4].replace(',', '')  # Efectivo
                                efectivo = float(efectivo_str)
                                
                                if tipo_habitacion in ingresos_por_tipo:
                                    ingresos_por_tipo[tipo_habitacion] += efectivo
                            except ValueError:
                                continue
                
                # Filtrar tipos con ingresos > 0
                tipos_con_ingresos = {k: v for k, v in ingresos_por_tipo.items() if v > 0}
                
                if tipos_con_ingresos:
                    tipos = list(tipos_con_ingresos.keys())
                    valores = list(tipos_con_ingresos.values())
                    colores = ["lightblue", "lightcoral", "lightgreen"][:len(tipos)]
                    
                    plt.figure(figsize=(8, 8))
                    plt.pie(valores, labels=tipos, autopct="%1.1f%%", colors=colores)
                    plt.title("Ingresos por tipo de habitación")
                    plt.show()
        except FileNotFoundError:
            print("Archivo de ingresos de caja no encontrado.")
        except Exception as e:
            print(f"Error: {str(e)}")

        # 7. Histograma: duración de estancias (desde historial de reservas)
        try:
            with open(REGISTRO_HISTORIAL_RESERVAS, "r") as file:
                lineas = file.readlines()
            
            if lineas:
                noches_list = []
                
                for linea in lineas:
                    if linea.strip():
                        parts = linea.strip().split(";")
                        if len(parts) >= 4:
                            try:
                                noches = int(parts[3])  # Numero_noches
                                noches_list.append(noches)
                            except ValueError:
                                continue
                
                if noches_list:
                    plt.figure(figsize=(10, 6))
                    max_noches = max(noches_list)
                    bins = range(1, max_noches + 2)
                    plt.hist(noches_list, bins=bins, edgecolor="black", alpha=0.7, color='skyblue')
                    plt.title("Distribución de duración de estancias")
                    plt.xlabel("Noches")
                    plt.ylabel("Cantidad de huéspedes")
                    plt.grid(True, alpha=0.3)
                    plt.show()
        except FileNotFoundError:
            print("Archivo de historial de reservas no encontrado.")
        except Exception as e:
            print(f"Error: {str(e)}")

        # 8. Gráfica combinada: ingresos diarios (barras) + huéspedes por día (línea)
        try:
            # Leer ingresos diarios desde ingresos_caja.csv
            ingresos_por_dia = {}
            with open(REGISTRO_INGRESOS_CAJA, "r") as file:
                lineas = file.readlines()
                
                for linea in lineas:
                    if linea.strip():
                        parts = linea.strip().split(";")
                        if len(parts) >= 5:
                            try:
                                fecha_str = parts[0]
                                fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                                efectivo_str = parts[4].replace(',', '')
                                efectivo = float(efectivo_str)
                                
                                if fecha in ingresos_por_dia:
                                    ingresos_por_dia[fecha] += efectivo
                                else:
                                    ingresos_por_dia[fecha] = efectivo
                            except Exception as e:
                                print(f"Error: {str(e)}")
                                continue
            
            # Leer checkouts diarios
            checkouts_por_dia = {}
            with open(REGISTRO_CHECKOUTS, "r") as file:
                lineas = file.readlines()
                
                for linea in lineas:
                    if linea.strip():
                        parts = linea.strip().split(";")
                        if len(parts) >= 1:
                            try:
                                fecha_str = parts[0]
                                fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
                                
                                if fecha in checkouts_por_dia:
                                    checkouts_por_dia[fecha] += 1
                                else:
                                    checkouts_por_dia[fecha] = 1
                            except Exception as e:
                                print(f"Error: {str(e)}")
                                continue
            
            # Combinar fechas y crear gráfico
            todas_fechas = sorted(set(list(ingresos_por_dia.keys()) + list(checkouts_por_dia.keys())))
            
            if todas_fechas:
                ingresos = [ingresos_por_dia.get(fecha, 0) for fecha in todas_fechas]
                huespedes = [checkouts_por_dia.get(fecha, 0) for fecha in todas_fechas]
                
                fig, ax1 = plt.subplots(figsize=(12, 6))
                
                # Gráfico de barras para ingresos
                ax1.bar(todas_fechas, ingresos, color="lightblue", alpha=0.7, label="Ingresos ($)")
                ax1.set_xlabel("Fecha")
                ax1.set_ylabel("Ingresos ($)", color="blue")
                ax1.tick_params(axis='y', labelcolor="blue")
                
                # Segundo eje Y para huéspedes
                ax2 = ax1.twinx()
                ax2.plot(todas_fechas, huespedes, color="red", marker="o", linewidth=2, label="Huéspedes")
                ax2.set_ylabel("Cantidad de huéspedes", color="red")
                ax2.tick_params(axis='y', labelcolor="red")
                
                plt.title("Ingresos diarios vs Cantidad de huéspedes")
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
                
        except FileNotFoundError:
            print("Archivos de registro no encontrados para gráfico combinado.")
        except Exception as e:
            print(f"Error: {str(e)}")