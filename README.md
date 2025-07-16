<div align="center" class="text-center">
<h1>🏨 Sistema de Gestión Hotelera</h1>

<img alt="last-commit" src="https://img.shields.io/github/last-commit/ema28pro/sistema-hotel?style=flat&amp;logo=git&amp;logoColor=white&amp;color=0080ff" class="inline-block mx-1" style="margin: 0px 2px;">
<img alt="repo-top-language" src="https://img.shields.io/github/languages/top/ema28pro/sistema-hotel?style=flat&amp;color=0080ff" class="inline-block mx-1" style="margin: 0px 2px;">
<img alt="repo-language-count" src="https://img.shields.io/github/languages/count/ema28pro/sistema-hotel?style=flat&amp;color=0080ff" class="inline-block mx-1" style="margin: 0px 2px;">
</div>

###

Un sistema completo de gestión hotelera desarrollado en Python que permite administrar huéspedes, reservas, habitaciones y generar reportes para un hotel.

## 📋 Características

### 🔐 Sistema de Autenticación
- **Administradores**: Acceso completo al sistema con credenciales
- **Huéspedes**: Acceso limitado para consultar y gestionar sus propias reservas

### 👥 Gestión de Huéspedes
- Registro de nuevos huéspedes con validación de datos
- Búsqueda por ID, nombre o documento
- Consulta de lista completa de huéspedes
- Validación de información personal (correo, teléfono, documento)

### 🏠 Gestión de Habitaciones
- **3 tipos de habitaciones disponibles:**
  - Sencilla: $50/noche
  - Doble: $80/noche
  - Suite: $150/noche
- Visualización del estado de ocupación
- 6 habitaciones en total (2 de cada tipo)

### 📅 Sistema de Reservas
- Creación de reservas con fechas y duración
- Validación de disponibilidad de habitaciones
- Cálculo automático de costos
- Gestión del estado de reservas (activa/finalizada)
- Consulta de reservas por huésped

### 📄 Documentación y Facturación
- Generación de comprobantes de reserva
- Emisión de facturas al registrar salida
- Detalles completos de costos y fechas

### 📊 Reportes Administrativos
- Total de huéspedes registrados
- Estado de ocupación de habitaciones
- Reservas activas
- Ingresos totales
- Tiempo promedio de estancia

## 🛠️ Estructura del Proyecto

```
sitema-hotel/
│
├── main.py           # Archivo principal con menús e interfaz
├── Clases.py         # Definición de todas las clases del sistema
├── Utils.py          # Funciones de validación y utilidades
└── README.md         # Documentación del proyecto
```

## 📁 Descripción de Archivos

### `main.py`
- **Función principal**: Maneja la interfaz de usuario y navegación
- **Menús incluidos**:
  - Menú principal (selección administrador/huésped)
  - Menú de administración
  - Menú de huésped
  - Menú de gestión de reservas

### `Clases.py`
- **Huesped**: Gestión de información personal y reservas
- **Habitacion**: Propiedades y estado de habitaciones
- **Reserva**: Lógica de reservas y cálculos
- **Comprobante**: Generación de comprobantes
- **Factura**: Generación de facturas
- **SistemaHotel**: Clase principal que coordina todo el sistema

### `Utils.py`
- Funciones de validación de datos
- Constantes del sistema
- Funciones auxiliares para entrada de datos

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Python 3.8 o superior
- Módulos estándar de Python (datetime)

### Pasos para Ejecutar

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/ema28pro/sitema-hotel
   cd sitema-hotel
   ```

2. **Ejecutar el sistema**:
   ```bash
   python main.py
   ```

## 🔑 Credenciales por Defecto

### Administradores
- **Usuario**: `admin` | **Contraseña**: `admin123`
- **Usuario**: `luna` | **Contraseña**: `luna123`

### Huéspedes de Prueba
El sistema incluye datos de prueba con varios huéspedes pre-registrados:
- Juan Pérez (Doc: 12345678)
- María García (Doc: 87654321)
- Carlos Martínez (Doc: 11223344)
- Ana López (Doc: 44332211)
- Luis Rodríguez (Doc: 99887766)
- Carmen Fernández (Doc: 55667788)
- Miguel Torres (Doc: 22334455)
- Lucas Felipo (Doc: 22334455)
- Miguel Simon (Doc: 33445566)

## 📱 Guía de Uso

### Para Administradores

1. **Iniciar sesión** con credenciales de administrador
2. **Opciones disponibles**:
   - Registrar nuevo huésped
   - Buscar huésped existente
   - Consultar lista de huéspedes
   - Visualizar todas las reservas
   - Visualizar estado de habitaciones
   - Generar reportes del hotel

### Para Huéspedes

1. **Buscar su registro** por ID, nombre o documento
2. **Opciones disponibles**:
   - Consultar sus reservas actuales
   - Realizar nueva reserva

### Proceso de Reserva

1. Seleccionar fechas de ingreso (formato: YYYY-MM-DD)
2. Especificar número de noches
3. Elegir tipo de habitación disponible
4. Confirmar reserva y generar comprobante
5. Al finalizar estancia, registrar salida para generar factura

## ✅ Validaciones Implementadas

- **Nombres y apellidos**: Solo letras, mínimo 3 caracteres
- **Documentos**: 3-15 dígitos numéricos
- **Correos**: Formato válido con @ y .
- **Teléfonos**: 7-15 dígitos numéricos
- **Fechas**: Formato YYYY-MM-DD, no anteriores a hoy
- **Tipos de habitación**: Solo valores permitidos (sencilla, doble, suite)

## 🔧 Funcionalidades Técnicas

### Gestión de Estados
- Control automático de disponibilidad de habitaciones
- Seguimiento de reservas activas/finalizadas
- Generación automática de IDs únicos

### Cálculos Automáticos
- Costo total basado en precio por noche × número de noches
- Fechas de salida calculadas automáticamente
- Reportes financieros en tiempo real

### Persistencia de Datos
- Los datos se mantienen en memoria durante la ejecución
- Sistema diseñado para fácil integración con bases de datos

## 🎯 Casos de Uso

### Caso 1: Registro de Nuevo Huésped
```
Admin → Registrar huésped → Completar datos → Huésped creado → Opción de crear reserva
```

### Caso 2: Reserva de Habitación
```
Huésped → Realizar reserva → Seleccionar fechas → Elegir habitación → Generar comprobante
```

### Caso 3: Check-out
```
Reserva activa → Registrar salida → Generar factura → Liberar habitación
```

## 📈 Reportes Disponibles

El sistema genera reportes automáticos que incluyen:
- **total_huespedes**: Número total de huéspedes registrados
- **habitaciones_ocupadas**: Cantidad de habitaciones ocupadas
- **habitaciones_disponibles**: Cantidad de habitaciones libres
- **reservas_activas**: Número de reservas actualmente activas
- **ingresos**: Total de ingresos por reservas activas
- **tiempo_promedio_estancia**: Promedio de noches por reserva

## 🤝 Contribuciones

Para contribuir al proyecto:

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## 📝 Notas de Desarrollo

- El sistema está diseñado con programación orientada a objetos
- Separación clara de responsabilidades entre clases
- Validaciones robustas para todos los inputs de usuario
- Interfaz de consola intuitiva y fácil de navegar
- Código modular y escalable

## 🐛 Problemas Conocidos

- Los datos no persisten entre ejecuciones (se reinician al cerrar)
- Interface limitada a consola de texto
- Sin conexión a base de datos externa

## 🔮 Mejoras Futuras

- [ ] Integración con base de datos (SQLite/PostgreSQL)
- [ ] Interface gráfica (Tkinter/PyQt)
- [ ] Sistema de reservas online
- [ ] Integración con servicios de pago
- [ ] Exportación de reportes (PDF/Excel)
- [ ] Sistema de notificaciones
- [ ] Gestión de servicios adicionales
- [ ] Multi-idioma

## 📞 Soporte

Para reportar bugs o solicitar nuevas funcionalidades, por favor crear un issue en el repositorio.

## Changelog
- 16/07/2025: Last Seen Time
    Agregar clases y funcionalidades para la gestión de huéspedes, habitaciones y reservas
---

**Desarrollado con ❤️ en Python**

<sub align="right">Made with patience and code ☕ — <a href="https://github.com/JessicaDiaz07/Hotel-Redenci-n" >Based on</a>.</sub>