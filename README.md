<div align="center" class="text-center">
<h1>🏨 Sistema de Gestión Hotelera</h1>

<img alt="last-commit" title="Last Commit" src="https://img.shields.io/github/last-commit/ema28pro/sistema-hotel?style=flat&amp;logo=git&amp;logoColor=white&amp;color=0080ff" class="inline-block mx-1" style="margin: 0px 2px;">
<img alt="repo-top-language" title="Repo Top Lenguage" src="https://img.shields.io/github/languages/top/ema28pro/sistema-hotel?style=flat&amp;color=0080ff" class="inline-block mx-1" style="margin: 0px 2px;">
<img alt="repo-language-count" title="Repo Language Count" src="https://img.shields.io/github/languages/count/ema28pro/sistema-hotel?style=flat&amp;color=0080ff" class="inline-block mx-1" style="margin: 0px 2px;">
<img alt="gitHub-contributors" title="GitHub Contributors" src="https://img.shields.io/github/contributors/ema28pro/sistema-hotel?style=flat&amp;color=0080ff" class="inline-block mx-1" style="margin: 0px 2px;">
<img alt="Matplotlib" title="matplotlib" src="https://img.shields.io/badge/Visualization-Matplotlib-blue" class="inline-block mx-1" style="margin: 0px 2px;">


</div>

<p align="center">Un sistema completo de gestión hotelera desarrollado en Python que permite administrar huéspedes, reservas, habitaciones y generar reportes con visualizaciones gráficas.</p>

## 📋 Características Principales

### 🔐 Sistema de Autenticación
- **Administradores**: Acceso completo al sistema
- **Huéspedes**: Acceso para gestionar sus reservas

### 👥 Gestión de Huéspedes
- Registro con validación de datos
- Búsqueda por ID, nombre o documento
- Importación/exportación desde archivos CSV

### 🏠 Gestión de Habitaciones
- **3 tipos**: Sencilla ($50), Doble ($80), Suite ($150)
- **6 habitaciones totales** (2 de cada tipo)
- Control de disponibilidad por fechas

### 📅 Sistema de Reservas
- Verificación automática de disponibilidad
- Prevención de conflictos de fechas
- Cálculo automático de costos
- Estados: pendiente, activa, finalizada

### 💰 Gestión Financiera
- Seguimiento automático del efectivo total
- Incremento con cada reserva realizada
- Reportes financieros detallados

### 📊 Sistema de Gráficos (8 Visualizaciones)

**Datos en tiempo real:**

   1. **Gráfico de barras** - Habitaciones ocupadas por tipo (sencilla/doble/suite)

   2. **Gráfico circular** - Distribución habitaciones ocupadas vs disponibles


**Análisis de archivos CSV:**

   3. **Gráfico de líneas** - Check-outs por día (archivo: checkouts.csv)

   4. **Barras horizontales** - Top 10 huéspedes por noches reservadas

   5. **Gráfico de dispersión** - Relación noches vs total pagado (archivo: historial_reservas.csv)

   6. **Gráfico circular** - Ingresos por tipo de habitación (archivo: ingresos_caja.csv)

   7. **Histograma** - Distribución de duración de estancias (archivo: historial_reservas.csv)

   8. **Gráfico combinado** - Ingresos diarios (barras) + huéspedes por día (línea) (archivos: ingresos_caja.csv y checkouts.csv)

## 🛠️ Estructura del Proyecto

```
sistema-hotel/
├── main.py                 # Interfaz principal y menús
├── Clases.py              # Clases del sistema (Hotel, Huésped, Reserva, etc.)
├── Utils.py               # Validaciones y utilidades
├── registros/             # Archivos CSV de datos
│   ├── huespedes.csv
│   ├── historial_reservas.csv
│   ├── entrada.csv
│   ├── checkouts.csv
│   └── ingresos_caja.csv
└── README.md
```

## 🚀 Instalación y Ejecución

### Requisitos Previos
- Python 3.8 o superior
- Módulos estándar de Python (datetime)

### Pasos para Ejecutar

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/ema28pro/sistema-hotel
   cd sistema-hotel
   ```

2. **Ejecutar el sistema**:
   ```bash
   python main.py
   ```

## 🔑 Credenciales

### Administradores
- `admin` / `admin123`
- `luna` / `luna123`

## 📱 Guía de Uso

### Para Administradores

1. **Iniciar sesión** con credenciales de administrador
2. **Opciones disponibles**:
   - **Registrar nuevo huésped** (obligatorio antes de que puedan hacer reservas)
   - Buscar huésped existente
   - Consultar lista de huéspedes
   - Visualizar todas las reservas
   - Visualizar estado de habitaciones
   - **Consultar disponibilidad por fechas**
   - Generar reportes del hotel (incluyendo efectivo total)
   - Generar gráficos

### Para Huéspedes

1. **Registro previo**: El huésped debe estar registrado en el sistema (registrado por un administrador)
2. **Buscar su registro** por ID, nombre o documento
3. **Opciones disponibles**:
   - Consultar sus reservas actuales
   - Realizar nueva reserva
   - Generar comprobante de reserva
   - Registrar entrada (check-in)
   - Registrar salida (check-out) y obtener factura

### Proceso de Reserva

1. Seleccionar fechas de ingreso (formato: YYYY-MM-DD)
2. Especificar número de noches
3. **Sistema verifica automáticamente disponibilidad** en las fechas solicitadas
4. **Mostrar habitaciones disponibles** con información detallada
5. Elegir habitación específica de la lista de disponibles
6. **Efectivo del hotel se incrementa automáticamente** con el costo de la reserva
7. Confirmar reserva y generar comprobante
8. **Todos los datos se guardan automáticamente** en los archivos CSV correspondientes

### Gestión de Estancia

1. **Check-in**: Registrar entrada del huésped en su fecha programada
   - Se guarda automáticamente en `entrada.csv`
2. **Durante la estancia**: Consultar detalles de la reserva
3. **Check-out**: Registrar salida para generar factura final
   - Se guarda automáticamente en `checkouts.csv`

## ✅ Validaciones

- **Nombres y apellidos**: Solo letras, mínimo 3 caracteres
- **Documentos**: 3-15 dígitos numéricos
- **Correos**: Formato válido con @ y .com o .co
- **Teléfonos**: 7-15 dígitos numéricos
- **Fechas**: Formato YYYY-MM-DD, no anteriores a hoy
- **Tipos de habitación**: Solo valores permitidos (sencilla, doble, suite)

## 💾 Archivos de Datos

El sistema mantiene **persistencia automática** de todos los datos:

- **huespedes.csv**: Información personal de huéspedes (se actualiza al registrar nuevos huéspedes)
- **historial_reservas.csv**: Historial completo de reservas (se actualiza al crear reservas)
- **entrada.csv**: Registro de check-ins (se actualiza al registrar entradas)
- **checkouts.csv**: Registro de check-outs (se actualiza al registrar salidas)
- **ingresos_caja.csv**: Registro de ingresos por reserva (se actualiza automáticamente con cada reserva)

**Nota importante**: Todos los cambios se guardan automáticamente en tiempo real. No es necesario guardar manualmente.

Todos los archivos usan formato CSV con separador `;` y codificación UTF-8.

<div align="right"><sub >Made with patience and code ☕ — <a href="https://github.com/JessicaDiaz07/Hotel-Redenci-n" >Based on</a>.</sub></div>

**Desarrollado con ❤️ en Python | Sistema de Gestión Hotelera v2.0**