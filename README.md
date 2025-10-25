# Ing. de Software - Examen Grupo 13
Repositorio para el Examen 1 de Ing. de Software

Integrantes:
- Federico Sanches
- Cecilia Podesta

## Patrón State - Flujo de Pago

Este proyecto implementa el **patrón State** para manejar el flujo de estados de un pago. El patrón permite que un objeto cambie su comportamiento cuando su estado interno cambia, aparentando como si el objeto hubiera cambiado de clase.

Los estados son los siguientes:

1. **REGISTRADO**: Estado inicial donde el pago fue registrado pero no procesado
2. **PAGADO**: Estado final exitoso donde el pago fue procesado correctamente  
3. **FALLIDO**: Estado de error donde el pago falló durante el procesamiento


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



## Tests
Para correr los tests por linea de comando:
python -m unittest tests.py


## Deploy
La aplicacion esta deployeada en el servicio de Render en https://ing-software-practica-examen-grupo13.onrender.com/docs