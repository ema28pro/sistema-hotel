# 🏨 Sistema de Gestión Hotelera

Un sistema completo de gestión hotelera desarrollado en Python que permite administrar huéspedes, reservas, habitaciones y generar reportes con visualizaciones gráficas.

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
sitema-hotel/
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

### Requisitos
- Python 3.8+
- matplotlib (para gráficos): `pip install matplotlib`

### Ejecutar
```bash
python main.py
```

## 🔑 Credenciales

### Administradores
- `admin` / `admin123`
- `luna` / `luna123`

### Huéspedes de Prueba
- Juan Pérez (Doc: 12345678)
- María García (Doc: 87654321)
- Carlos Martínez (Doc: 11223344)
- Y más... (ver huespedes.csv)

## 📱 Guía Rápida

### Administradores
1. Iniciar sesión
2. Registrar/buscar huéspedes
3. Visualizar reservas y habitaciones
4. Generar reportes y gráficos

### Huéspedes
1. Buscar por documento/nombre
2. Consultar reservas existentes
3. Realizar nuevas reservas

### Proceso de Reserva
1. Seleccionar fechas (YYYY-MM-DD)
2. Especificar noches
3. Sistema verifica disponibilidad
4. Elegir habitación disponible
5. Confirmar y generar comprobante

## 💾 Archivos de Datos
- **huespedes.csv**: Información personal de huéspedes
- **historial_reservas.csv**: Historial completo de reservas
- **entrada.csv**: Registro de check-ins
- **checkouts.csv**: Registro de check-outs
- **ingresos_caja.csv**: Registro de ingresos por reserva

Todos los archivos usan formato CSV con separador `;` y codificación UTF-8.
