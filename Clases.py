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
        self.reservas_activas = []  # Lista de reservas activas para verificar disponibilidad por fechas
    
    def esta_disponible_en_fechas(self, fecha_ingreso, fecha_salida):
        """
        Verifica si la habitación está disponible en el rango de fechas especificado
        """
        fecha_ingreso_dt = datetime.strptime(fecha_ingreso, "%Y-%m-%d").date()
        fecha_salida_dt = datetime.strptime(fecha_salida, "%Y-%m-%d").date()
        
        for reserva in self.reservas_activas:
            if not reserva.activa:
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
        # Obtener reservas activas
        reservas_activas = [r for r in self.reservas_activas if r.activa]
        
        if reservas_activas:
            info = f"Hab. {self.numero} ({self.tipo}) - ${self.precio_noche}/noche - {len(reservas_activas)} reserva(s):"
            for i, reserva in enumerate(reservas_activas, 1):
                info += f"\n    {i}. {reserva.fecha_ingreso} al {reserva.fecha_salida} ({reserva.huesped.nombre} {reserva.huesped.apellido})"
            return info
        else:
            return f"Hab. {self.numero} ({self.tipo}) - ${self.precio_noche}/noche - Disponible"

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
        self.efectivo = 0.0
    
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
        
        print(f"🎉 Reserva realizada exitosamente!")
        print(f"ID de reserva: {nueva_reserva.id}")
        print(f"Habitación: {habitacion_reservada.numero}")
        print(f"Fechas: {nueva_reserva.fecha_ingreso} al {nueva_reserva.fecha_salida}")
        print(f"Costo total: ${nueva_reserva.costo_total}")
        print(f"💰 Efectivo del hotel: ${self.efectivo}")
        
        return nueva_reserva
    
    def generar_comprobante(self, reserva):
        return Comprobante(reserva)
    
    def registrar_salida(self, reserva):
        reserva.activa = False
        reserva.habitacion.liberar_reserva(reserva)
        return Factura(reserva)
    
    def autenticar_usuario(self, usuario, contrasena):
        return self.usuarios_admin.get(usuario) == contrasena
    
    def generar_reportes(self):
        reportes = {}
        reportes["total_huespedes"] = len(self.huespedes)
        
        # Contar habitaciones con reservas activas
        habitaciones_con_reservas_activas = 0
        for habitacion in self.habitaciones:
            if any(reserva.activa for reserva in habitacion.reservas_activas):
                habitaciones_con_reservas_activas += 1
        
        reportes["habitaciones_con_reservas_activas"] = habitaciones_con_reservas_activas
        reportes["habitaciones_sin_reservas"] = len(self.habitaciones) - habitaciones_con_reservas_activas
        
        reservas_activas = [r for r in self.reservas if r.activa]
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
                        if reserva.activa:
                            res_ingreso = datetime.strptime(reserva.fecha_ingreso, "%Y-%m-%d").date()
                            res_salida = datetime.strptime(reserva.fecha_salida, "%Y-%m-%d").date()
                            consulta_ingreso = datetime.strptime(fecha_ingreso, "%Y-%m-%d").date()
                            consulta_salida = datetime.strptime(fecha_salida, "%Y-%m-%d").date()
                            
                            if not (consulta_salida <= res_ingreso or consulta_ingreso >= res_salida):
                                print(f"    Reservada por: {reserva.huesped.nombre} {reserva.huesped.apellido}")
                                print(f"    Del {reserva.fecha_ingreso} al {reserva.fecha_salida}")
            
            print(f"\nResumen: {len(habitaciones_disponibles)} disponibles, {len(habitaciones_ocupadas)} ocupadas")
        
        return habitaciones_disponibles
