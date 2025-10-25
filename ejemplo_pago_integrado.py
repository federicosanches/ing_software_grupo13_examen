#!/usr/bin/env python3
"""
Ejemplo de uso de la clase Pago integrada con main.py
Este ejemplo demuestra cómo la clase Pago funciona con el sistema de persistencia JSON.
"""

from Pago import Pago
import json

def ejemplo_pago_integrado():
    """Demuestra el uso de la clase Pago con integración JSON."""
    
    print("=== EJEMPLO: Clase Pago Integrada con main.py ===\n")
    
    # 1. Crear un pago (se guarda automáticamente en JSON)
    print("1. Creando pago con tarjeta de crédito...")
    pago1 = Pago("001", 5000.00, "tarjeta_credito")
    print(f"   Estado: {pago1.get_estado()}")
    print()
    
    # 2. Crear otro pago
    print("2. Creando pago con PayPal...")
    pago2 = Pago("002", 3000.00, "paypal")
    print(f"   Estado: {pago2.get_estado()}")
    print()
    
    # 3. Mostrar contenido del archivo JSON
    print("3. Contenido actual del archivo JSON:")
    data = Pago.load_all_payments()
    print(json.dumps(data, indent=2))
    print()
    
    # 4. Procesar pagos
    print("4. Procesando pagos...")
    print("   Procesando pago 001:")
    resultado1 = pago1.pagar()
    print(f"   Resultado: {'EXITOSO' if resultado1 else 'FALLIDO'}")
    print(f"   Estado final: {pago1.get_estado()}")
    print()
    
    print("   Procesando pago 002:")
    resultado2 = pago2.pagar()
    print(f"   Resultado: {'EXITOSO' if resultado2 else 'FALLIDO'}")
    print(f"   Estado final: {pago2.get_estado()}")
    print()
    
    # 5. Mostrar contenido actualizado del JSON
    print("5. Contenido actualizado del archivo JSON:")
    data = Pago.load_all_payments()
    print(json.dumps(data, indent=2))
    print()
    
    # 6. Cargar pago desde JSON
    print("6. Cargando pago desde JSON...")
    try:
        pago_cargado = Pago.load_from_json("001")
        print(f"   Pago cargado: {pago_cargado}")
        print(f"   Estado del pago cargado: {pago_cargado.get_estado()}")
        pago_cargado.mostrar_info()
    except Exception as e:
        print(f"   Error cargando pago: {e}")
    
    # 7. Obtener todos los pagos desde JSON
    print("7. Obteniendo todos los pagos desde JSON...")
    todos_los_pagos = Pago.get_all_from_json()
    for pago_id, pago in todos_los_pagos.items():
        print(f"   Pago {pago_id}: {pago.get_estado()} - ${pago.monto:.2f}")
    print()
    
    # 8. Actualizar un pago
    print("8. Actualizando pago (si está en estado REGISTRADO)...")
    # Crear un pago que permanezca en REGISTRADO
    pago3 = Pago("003", 1000.00, "paypal")
    print(f"   Pago 003 creado en estado: {pago3.get_estado()}")
    
    resultado_update = pago3.actualizar(nuevo_monto=1500.00, nuevo_metodo="tarjeta_credito")
    print(f"   Actualización: {'EXITOSA' if resultado_update else 'FALLIDA'}")
    print(f"   Nuevo estado: {pago3.get_estado()}")
    print(f"   Nuevo monto: ${pago3.monto:.2f}")
    print(f"   Nuevo método: {pago3.metodo_pago}")
    print()
    
    # 9. Contenido final del JSON
    print("9. Contenido final del archivo JSON:")
    data = Pago.load_all_payments()
    print(json.dumps(data, indent=2))

def ejemplo_validaciones():
    """Demuestra las validaciones específicas implementadas."""
    
    print("\n=== EJEMPLO: Validaciones Específicas ===\n")
    
    # Limpiar datos previos
    with open("data.json", "w") as f:
        f.write("{}")
    
    # Validación 1: Tarjeta de crédito con monto alto (debería fallar)
    print("1. Tarjeta de crédito con monto >= $10,000 (debería fallar):")
    pago_tc_alto = Pago("TC001", 15000.00, "tarjeta_credito")
    resultado = pago_tc_alto.pagar()
    print(f"   Resultado: {'EXITOSO' if resultado else 'FALLIDO'}")
    print(f"   Estado final: {pago_tc_alto.get_estado()}\n")
    
    # Validación 2: Tarjeta de crédito con monto válido (debería pasar)
    print("2. Tarjeta de crédito con monto < $10,000 (debería pasar):")
    pago_tc_valido = Pago("TC002", 5000.00, "tarjeta_credito")
    resultado = pago_tc_valido.pagar()
    print(f"   Resultado: {'EXITOSO' if resultado else 'FALLIDO'}")
    print(f"   Estado final: {pago_tc_valido.get_estado()}\n")
    
    # Validación 3: Segundo pago con tarjeta de crédito (debería fallar por límite)
    print("3. Segundo pago con tarjeta de crédito en REGISTRADO (debería fallar):")
    pago_tc_segundo = Pago("TC003", 3000.00, "tarjeta_credito")
    resultado = pago_tc_segundo.pagar()
    print(f"   Resultado: {'EXITOSO' if resultado else 'FALLIDO'}")
    print(f"   Estado final: {pago_tc_segundo.get_estado()}\n")
    
    # Validación 4: PayPal con monto alto (debería fallar)
    print("4. PayPal con monto >= $5,000 (debería fallar):")
    pago_pp_alto = Pago("PP001", 6000.00, "paypal")
    resultado = pago_pp_alto.pagar()
    print(f"   Resultado: {'EXITOSO' if resultado else 'FALLIDO'}")
    print(f"   Estado final: {pago_pp_alto.get_estado()}\n")
    
    # Validación 5: PayPal con monto válido (debería pasar)
    print("5. PayPal con monto < $5,000 (debería pasar):")
    pago_pp_valido = Pago("PP002", 2500.00, "paypal")
    resultado = pago_pp_valido.pagar()
    print(f"   Resultado: {'EXITOSO' if resultado else 'FALLIDO'}")
    print(f"   Estado final: {pago_pp_valido.get_estado()}\n")

def main():
    """Función principal que ejecuta todos los ejemplos."""
    ejemplo_pago_integrado()
    ejemplo_validaciones()
    
    print("✅ EJEMPLOS COMPLETADOS")
    print("📁 Los datos se guardaron en: data.json")

if __name__ == "__main__":
    main()