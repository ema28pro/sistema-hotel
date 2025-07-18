from Clases import Huesped, Habitacion, Reserva, SistemaHotel, Comprobante, Factura


def App():
    
    hotel.cargar_huespedes()
    
    while True:
        print("=============== BIENVENIDO AL HOTEL ===============")
        print("1. Iniciar sesión como administrador")
        print("2. Iniciar sesión como huésped")
        print("Enter para salir")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            usuario = input("Usuario: ")
            contrasena = input("Contraseña: ")
            if hotel.autenticar_usuario(usuario, contrasena):
                print("Acceso concedido")
                menu_administracion()
            input("Enter para continuar...")
        elif opcion == "2":
            huesped = hotel.buscar_huesped()
            if huesped:
                menu_huesped(huesped)
            input("Enter para continuar...")
        else:
            salir = input("Está seguro que desea salir? (Enter para confirmar)")
            if salir in ["SI", "Si", "si", "s"]:
                print("Saliendo del sistema...")
                return
            else:
                print("Operacion cancelada.")

def menu_administracion():
    while True:
        print("============ MENU ADMINISTRADOR ============")
        print("1. Registrar huésped")
        print("2. Buscar huesped")
        print("3. Consultar huespedes")
        print("4. Visualizar reservas")
        print("5. Visualizar habitaciones")
        print("6. Consultar disponibilidad")
        print("7. Generar reportes")
        print("8. Generar Graficos")
        print("Enter para salir")
        opcion = input("Seleccione una opción: ")
        if not opcion in ["1", "2", "3", "4", "5", "6", "7", "8", ""]:
            print("Opción no válida. Saliendo del sistema.")
            return
        match opcion:
            case "1":
                huesped = hotel.registrar_huesped()
                if huesped:
                    menu_huesped(huesped)
                input("Enter para continuar...")
            case "2":
                huesped = hotel.buscar_huesped()
                if huesped:
                    menu_huesped(huesped)
                input("Enter para continuar...")
            case "3":
                huesped = hotel.consultar_huespedes()
                if huesped:
                    menu_huesped(huesped)
                input("Enter para continuar...")
            case "4":
                reserva = hotel.visualizar_reservas()
                if reserva:
                    menu_reserva(reserva)
                input("Enter para continuar...")
            case "5":
                hotel.visualizar_habitaciones()
                input("Enter para continuar...")
            case "6":
                print("Consultando disponibilidad...")
                hotel.consultar_disponibilidad()
                input("Enter para continuar...")
            case "7":
                print("Generando reportes...")
                reportes = hotel.generar_reportes()
                print("\nReportes administrativos:")
                for k, v in reportes.items():
                    print(f"{k}: {v}")
                input("Enter para continuar...")
            case "8":
                print("Generando gráficos...")
                hotel.mostrar_graficos()
                input("Enter para continuar...")
            case "":
                salir = input("Está seguro que desea salir? (Enter para confirmar)")
                if salir in ["SI", "Si", "si", "s"]:
                    print("Saliendo del sistema...")
                    return
                else:
                    print("Operacion cancelada.")

def menu_huesped(huesped):
    while True:
        print("\n")
        print("="*30)
        print("========== MENU HUESPED ==========")
        print(f"Bienvenido {huesped.nombre} {huesped.apellido}")
        print("1. Consultar reservas")
        print("2. Realizar reserva")
        print("Enter para Salir")
        opcion = input("Seleccione una opción: ")
        if not opcion in ["1", "2", ""]:
            print("Opción no válida. Saliendo del sistema.")
            return
        
        match opcion:
            case "1":
                reserva = huesped.consultar_reservas()
                if reserva:
                    menu_reserva(reserva)
                else:
                    input("Enter para continuar...")
            case "2":
                reserva = hotel.realizar_reserva(huesped)
                if reserva:
                    menu_reserva(reserva)
                else:
                    input("Enter para continuar...")
            case "":
                print("Saliendo del menu huesped...")
                return

def menu_reserva(reserva):
    while True:
        print("\n")
        print("="*30)
        print("========== MENU RESERVA ==========")
        print(f"Reserva N° {reserva.id} | Habitación: {reserva.habitacion.numero}")
        print(f"Fecha de ingreso: {reserva.fecha_ingreso} | Fecha de salida: {reserva.fecha_salida}")
        print(f"N° Noches: {reserva.num_noches} | Costo total: ${reserva.costo_total}")
        print("1. Generar Comprobante")
        print("2. Registrar Ingreso")
        print("3. Registrar Salida")
        print("Enter para salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            comprobante = hotel.generar_comprobante(reserva)
            print(comprobante.detalles)
            input("Enter para continuar...")
        elif opcion == "2":
            hotel.registrar_entrada(reserva)
        elif opcion == "3":
            factura = hotel.registrar_salida(reserva)
            if factura:
                print(factura.detalles)
                return
            input("Enter para continuar...")
        elif opcion == "":
            print("Saliendo del sistema...")
            return

if __name__ == "__main__":
    hotel = SistemaHotel()
    
    App()
