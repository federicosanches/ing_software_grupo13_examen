# ing_software_grupo13_examen
Repositorio para el Examen 1 de Ing. de Software

## Patrón State - Flujo de Pago

Este proyecto implementa el **patrón State** para manejar el flujo de estados de un pago. El patrón permite que un objeto cambie su comportamiento cuando su estado interno cambia, aparentando como si el objeto hubiera cambiado de clase.

### 🎯 Funcionalidades del Sistema

El sistema de pagos maneja tres estados principales:

1. **REGISTRADO**: Estado inicial donde el pago fue registrado pero no procesado
2. **PAGADO**: Estado final exitoso donde el pago fue procesado correctamente  
3. **FALLIDO**: Estado de error donde el pago falló durante el procesamiento

### 🔄 Operaciones Disponibles

#### Registrar
- El usuario registra un pago con `id`, `monto` y `método de pago`
- El pago se crea automáticamente en estado **REGISTRADO**

#### Pagar
- El sistema valida el pago según el método seleccionado
- Si la validación es exitosa → estado **PAGADO**
- Si la validación falla → estado **FALLIDO**

#### Revertir
- Cambia un pago en estado **FALLIDO** a estado **REGISTRADO**
- Permite un nuevo intento de procesamiento
- No funciona en estados **PAGADO** (por seguridad)

#### Actualizar
- Modifica `monto` y/o `método de pago`
- Solo funciona en estado **REGISTRADO**
- No permite modificar pagos procesados o fallidos

### 📁 Estructura del Proyecto

```
├── EstadoPago.py          # Interfaz abstracta para todos los estados
├── EstadoRegistrado.py    # Implementación del estado REGISTRADO
├── EstadoPagado.py        # Implementación del estado PAGADO
├── EstadoFallido.py       # Implementación del estado FALLIDO
├── Pago.py               # Clase contexto que usa el patrón State
├── ejemplo_uso.py        # Ejemplo completo de uso del sistema
└── README.md            # Este archivo
```

### 🏗️ Arquitectura del Patrón State

```
┌─────────────────┐
│     Pago        │  ← Contexto
│  (Contexto)     │
├─────────────────┤
│ - estado        │ ─────┐
│ + pagar()       │      │
│ + revertir()    │      │
│ + actualizar()  │      │
└─────────────────┘      │
                         │
                         ▼
         ┌─────────────────────┐
         │   EstadoPago        │  ← Interfaz State
         │   (Abstract)        │
         ├─────────────────────┤
         │ + pagar()           │
         │ + revertir()        │
         │ + actualizar()      │
         │ + get_nombre_estado()│
         └─────────────────────┘
                    ▲
         ┌──────────┼──────────┐
         │          │          │
┌────────────┐ ┌───────────┐ ┌────────────┐
│EstadoReg.  │ │EstadoPag. │ │EstadoFall. │  ← Estados Concretos
│            │ │           │ │            │
├────────────┤ ├───────────┤ ├────────────┤
│✓ pagar()   │ │✗ pagar()  │ │✗ pagar()   │
│≈ revertir()│ │✗ revertir()│ │✓ revertir()│
│✓ actualizar│ │✗ actualizar│ │✗ actualizar│
└────────────┘ └───────────┘ └────────────┘
```

### 📊 Matriz de Estados y Transiciones

| Estado Actual | Pagar | Revertir | Actualizar |
|---------------|-------|----------|------------|
| **REGISTRADO** | ✅ → PAGADO/FALLIDO | ≈ Sin efecto | ✅ Permitido |
| **PAGADO** | ❌ Ya procesado | ❌ No permitido | ❌ Inmutable |
| **FALLIDO** | ❌ Debe revertirse | ✅ → REGISTRADO | ❌ Debe revertirse |

**Leyenda:**
- ✅ = Operación permitida
- ❌ = Operación no permitida  
- ≈ = Operación sin efecto

### 🚀 Cómo Usar

#### Instalación y Ejecución

```bash
# Clonar el repositorio
git clone <url-del-repositorio>
cd ing_software_grupo13_examen

# Ejecutar el ejemplo completo
python ejemplo_uso.py
```

#### Uso Básico

```python
from Pago import Pago

# 1. Crear un nuevo pago (estado REGISTRADO)
pago = Pago("PAY-001", 150.75, "tarjeta_credito")

# 2. Actualizar si es necesario (solo en REGISTRADO)
pago.actualizar(nuevo_monto=200.00, nuevo_metodo="paypal")

# 3. Procesar el pago
exito = pago.pagar()  # → PAGADO o FALLIDO

# 4. Si falló, revertir y reintentar
if not exito:
    pago.revertir()  # FALLIDO → REGISTRADO
    pago.actualizar(nuevo_metodo="transferencia")
    pago.pagar()

# 5. Verificar estado y información
print(f"Estado actual: {pago.get_estado()}")
pago.mostrar_info()
```

### 🔍 Ejemplos de Flujos

#### Flujo Exitoso
```
REGISTRADO → [pagar()] → PAGADO
```

#### Flujo con Fallo y Recuperación
```
REGISTRADO → [pagar()] → FALLIDO → [revertir()] → REGISTRADO → [pagar()] → PAGADO
```

#### Flujo con Actualización
```
REGISTRADO → [actualizar()] → REGISTRADO → [pagar()] → PAGADO
```

### ⚙️ Configuración de Métodos de Pago

El sistema simula diferentes tasas de éxito según el método de pago:

- **efectivo**: 100% éxito
- **transferencia**: 95% éxito  
- **tarjeta_debito**: 90% éxito
- **tarjeta_credito**: 85% éxito
- **paypal**: 80% éxito
- **otros métodos**: 50% éxito

### 🎯 Ventajas del Patrón State Implementado

1. **Encapsulación**: Cada estado maneja su propia lógica
2. **Extensibilidad**: Fácil agregar nuevos estados
3. **Mantenibilidad**: Cambios en un estado no afectan otros
4. **Claridad**: El código refleja claramente las reglas de negocio
5. **Seguridad**: Previene operaciones inválidas según el estado

### 🧪 Testing

El archivo `ejemplo_uso.py` incluye pruebas comprehensivas que demuestran:

- ✅ Flujos exitosos de pago
- ❌ Manejo de pagos fallidos  
- 🔄 Reversión y reintento de pagos
- 🔧 Validaciones de entrada
- 📊 Todas las transiciones de estado posibles

### 👥 Equipo de Desarrollo

**Grupo 13 - Ingeniería de Software**
- Implementación del patrón State para sistema de pagos
- Examen 1 - Octubre 2025
