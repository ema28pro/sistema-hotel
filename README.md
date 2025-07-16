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

### 📅 Sistema de Reservas Avanzado
- **Sistema de disponibilidad basado en fechas**: Permite múltiples reservas por habitación en diferentes períodos
- **Detección automática de conflictos**: Previene reservas superpuestas en fechas
- **Consulta de disponibilidad**: Verificación en tiempo real para rangos de fechas específicos
- Creación de reservas con fechas y duración
- Validación de disponibilidad de habitaciones
- Cálculo automático de costos
- Gestión del estado de reservas (activa/finalizada)
- Consulta de reservas por huésped

### 💰 Gestión Financiera
- **Efectivo del hotel**: Seguimiento automático del efectivo total acumulado
- **Incremento automático**: El efectivo aumenta con cada reserva realizada
- **Reportes financieros**: Visualización del efectivo total en reportes administrativos

### 📄 Documentación y Facturación
- Generación de comprobantes de reserva
- Emisión de facturas al registrar salida
- Detalles completos de costos y fechas

### 📊 Reportes Administrativos
- Total de huéspedes registrados
- Estado de ocupación de habitaciones (activas/disponibles)
- Reservas activas en el sistema
- Ingresos totales por reservas activas
- **Efectivo total del hotel**: Suma de todos los pagos recibidos
- Tiempo promedio de estancia
- **Consulta de disponibilidad**: Verificación de habitaciones disponibles por fechas específicas

## 🛠️ Estructura del Proyecto

```
sitema-hotel/
│
├── main.py                    # Archivo principal con menús e interfaz
├── Clases.py                  # Definición de todas las clases del sistema
├── Utils.py                   # Funciones de validación y utilidades
└── README.md                  # Documentación del proyecto
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
- **Habitacion**: Propiedades, estado y gestión de múltiples reservas por fechas
- **Reserva**: Lógica de reservas, cálculos y fechas automáticas
- **Comprobante**: Generación de comprobantes de reserva
- **Factura**: Generación de facturas de salida
- **SistemaHotel**: Clase principal que coordina todo el sistema, incluyendo gestión financiera

### `Utils.py`
- Funciones de validación de datos
- Constantes del sistema (tipos de habitación)
- Funciones auxiliares para entrada de datos (fechas, nombres, documentos, etc.)

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
   - **Consultar disponibilidad por fechas**
   - Generar reportes del hotel (incluyendo efectivo total)

### Para Huéspedes

1. **Buscar su registro** por ID, nombre o documento
2. **Opciones disponibles**:
   - Consultar sus reservas actuales
   - Realizar nueva reserva

### Proceso de Reserva

1. Seleccionar fechas de ingreso (formato: YYYY-MM-DD)
2. Especificar número de noches
3. **Sistema verifica automáticamente disponibilidad** en las fechas solicitadas
4. **Mostrar habitaciones disponibles** con información detallada
5. Elegir habitación específica de la lista de disponibles
6. **Efectivo del hotel se incrementa automáticamente** con el costo de la reserva
7. Confirmar reserva y generar comprobante
8. Al finalizar estancia, registrar salida para generar factura

## ✅ Validaciones Implementadas

- **Nombres y apellidos**: Solo letras, mínimo 3 caracteres
- **Documentos**: 3-15 dígitos numéricos
- **Correos**: Formato válido con @ y .
- **Teléfonos**: 7-15 dígitos numéricos
- **Fechas**: Formato YYYY-MM-DD, no anteriores a hoy
- **Tipos de habitación**: Solo valores permitidos (sencilla, doble, suite)

## 🔧 Funcionalidades Técnicas

### Sistema de Disponibilidad Avanzado
- **Algoritmo de detección de conflictos**: Verifica solapamiento de fechas matemáticamente
- **Múltiples reservas por habitación**: Una habitación puede tener varias reservas en diferentes períodos
- **Consulta en tiempo real**: Verificación instantánea de disponibilidad por rango de fechas
- **Lista de reservas activas**: Cada habitación mantiene su historial de reservas

### Gestión de Estados
- Control automático de disponibilidad de habitaciones por fechas
- Seguimiento de reservas activas/finalizadas con historial completo
- Generación automática de IDs únicos para huéspedes y reservas
- **Gestión financiera**: Tracking automático del efectivo del hotel

### Cálculos Automáticos
- Costo total basado en precio por noche × número de noches
- Fechas de salida calculadas automáticamente usando timedelta
- **Incremento automático del efectivo** con cada reserva
- Reportes financieros en tiempo real con efectivo acumulado

### Persistencia de Datos
- Los datos se mantienen en memoria durante la ejecución
- Sistema diseñado para fácil integración con bases de datos

## 🎯 Casos de Uso

### Caso 1: Registro de Nuevo Huésped
```
Admin → Registrar huésped → Completar datos → Huésped creado → Opción de crear reserva
```

### Caso 2: Reserva de Habitación con Verificación de Disponibilidad
```
Huésped → Realizar reserva → Seleccionar fechas → Sistema verifica disponibilidad → 
Mostrar habitaciones disponibles → Elegir habitación → Efectivo se incrementa → Generar comprobante
```

### Caso 3: Múltiples Reservas en la Misma Habitación
```
Habitación 101 → Reserva del 1-5 de julio → Reserva del 10-15 de julio → 
Ambas coexisten sin conflicto → Diferentes huéspedes, misma habitación
```

### Caso 4: Check-out
```
Reserva activa → Registrar salida → Generar factura → Liberar habitación
```

## 📈 Reportes Disponibles

El sistema genera reportes automáticos que incluyen:
- **total_huespedes**: Número total de huéspedes registrados
- **habitaciones_con_reservas_activas**: Cantidad de habitaciones con reservas activas
- **habitaciones_sin_reservas**: Cantidad de habitaciones completamente libres  
- **reservas_activas**: Número de reservas actualmente activas
- **ingresos**: Total de ingresos por reservas activas
- **efectivo_total**: Total de efectivo acumulado por todas las reservas realizadas
- **tiempo_promedio_estancia**: Promedio de noches por reserva

### 🆕 Funcionalidades de Consulta
- **Consulta de disponibilidad por fechas**: Verificar qué habitaciones están disponibles en un rango específico
- **Información detallada**: Ver todas las reservas activas de una habitación específica
- **Estado en tiempo real**: Visualización actualizada del estado de cada habitación

## 🤝 Contribuciones

Para contribuir al proyecto:

1. Fork el repositorio
2. Crear una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear un Pull Request

## 📝 Notas de Desarrollo

- El sistema está diseñado con programación orientada a objetos
- **Arquitectura modular**: Separación clara de responsabilidades entre clases
- **Sistema de fechas robusto**: Manejo de datetime para reservas y disponibilidad
- **Algoritmos de detección de conflictos**: Matemática para verificar solapamiento de fechas
- Validaciones robustas para todos los inputs de usuario
- Interfaz de consola intuitiva y fácil de navegar
- Código modular y escalable
- **Gestión financiera integrada**: Tracking automático de efectivo

### 🔍 Algoritmo de Disponibilidad

El sistema utiliza un algoritmo matemático para detectar conflictos de fechas:
```python
# Verificar si hay solapamiento entre dos rangos de fechas
if not (fecha_salida_nueva <= reserva_ingreso or fecha_ingreso_nueva >= reserva_salida):
    # Hay conflicto - fechas se solapan
```

Este enfoque permite múltiples reservas en la misma habitación siempre que no se solapen en fechas.

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
- [ ] Sistema de notificaciones automáticas
- [ ] **Gestión de servicios adicionales** (spa, restaurante, etc.)
- [ ] Multi-idioma
- [ ] **Sistema de descuentos y promociones**
- [ ] **Gestión de empleados y turnos**
- [ ] **Integración con calendarios externos**
- [ ] **API REST para integración con otros sistemas**

## 📞 Soporte

Para reportar bugs o solicitar nuevas funcionalidades, por favor crear un issue en el repositorio.

---

## Changelog
- **16/07/2025**: Implementación del sistema de disponibilidad basado en fechas
  - ✅ Sistema de múltiples reservas por habitación
  - ✅ Detección automática de conflictos de fechas
  - ✅ Consulta de disponibilidad por rangos de fechas
  - ✅ Gestión automática del efectivo del hotel
  - ✅ Reportes financieros mejorados
  - ✅ Optimización de la función realizar_reserva
  - ✅ Interfaz de usuario mejorada con información detallada
  - ✅ Archivos de pruebas para validar funcionalidades
  - ✅ Limpieza de código y eliminación de parámetros redundantes

- **Versión inicial**: Funcionalidades básicas
  - Agregar clases y funcionalidades para la gestión de huéspedes, habitaciones y reservas

<div align="right"><sub >Made with patience and code ☕ — <a href="https://github.com/JessicaDiaz07/Hotel-Redenci-n" >Based on</a>.</sub></div>

**Desarrollado con ❤️ en Python | Sistema de Gestión Hotelera v2.0**

---

### 🏆 Características Destacadas de la Versión 2.0

- **🗓️ Sistema de fechas inteligente**: Reservas múltiples sin conflictos
- **💰 Gestión financiera automática**: Tracking de efectivo en tiempo real  
- **🔍 Consultas avanzadas**: Disponibilidad por fechas específicas
- **🛡️ Validaciones robustas**: Sistema a prueba de errores
- **📊 Reportes completos**: Información financiera y operativa detallada

