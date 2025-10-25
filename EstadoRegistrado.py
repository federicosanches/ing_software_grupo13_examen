from EstadoPago import EstadoPago
from typing import TYPE_CHECKING
import random

if TYPE_CHECKING:
    from Pago import Pago


class EstadoRegistrado(EstadoPago):
    """
    Estado REGISTRADO - El pago fue registrado pero aún no procesado.
    Permite: pagar, revertir (sin efecto), actualizar
    """
    
    def pagar(self, pago: 'Pago') -> bool:
        """
        Procesa el pago y cambia al estado PAGADO o FALLIDO según la validación.
        """
        print(f"Procesando pago {pago.id} con método {pago.metodo_pago}...")
        
        # Simulamos la validación del método de pago
        es_valido = self._validar_pago(pago.metodo_pago, pago.monto)
        
        if es_valido:
            print(f"✓ Pago {pago.id} procesado exitosamente")
            from EstadoPagado import EstadoPagado
            pago._cambiar_estado(EstadoPagado())
            return True
        else:
            print(f"✗ Error al procesar el pago {pago.id}")
            from EstadoFallido import EstadoFallido
            pago._cambiar_estado(EstadoFallido())
            return False
    
    def revertir(self, pago: 'Pago') -> bool:
        """
        En estado REGISTRADO, revertir no tiene efecto (ya está en el estado inicial).
        """
        print(f"ℹ El pago {pago.id} ya se encuentra en estado REGISTRADO")
        return True
    
    def actualizar(self, pago: 'Pago', nuevo_monto: float = None, nuevo_metodo: str = None) -> bool:
        """
        Permite actualizar el monto y/o método de pago en estado REGISTRADO.
        """
        cambios_realizados = []
        
        if nuevo_monto is not None and nuevo_monto > 0:
            monto_anterior = pago.monto
            pago.monto = nuevo_monto
            cambios_realizados.append(f"monto: ${monto_anterior:.2f} → ${nuevo_monto:.2f}")
        
        if nuevo_metodo is not None:
            metodo_anterior = pago.metodo_pago
            pago.metodo_pago = nuevo_metodo
            cambios_realizados.append(f"método: {metodo_anterior} → {nuevo_metodo}")
        
        if cambios_realizados:
            print(f"✓ Pago {pago.id} actualizado: {', '.join(cambios_realizados)}")
            return True
        else:
            print(f"ℹ No se especificaron cambios válidos para el pago {pago.id}")
            return False
    
    def get_nombre_estado(self) -> str:
        """Retorna el nombre del estado."""
        return "REGISTRADO"
    
    def _validar_pago(self, metodo_pago: str, monto: float) -> bool:
        """
        Simula la validación del pago según el método seleccionado.
        
        Args:
            metodo_pago: Método de pago a validar
            monto: Monto del pago
            
        Returns:
            bool: True si la validación es exitosa, False en caso contrario
        """
        # Simulamos diferentes validaciones según el método de pago
        validaciones = {
            "tarjeta_credito": 0.85,  # 85% de éxito
            "tarjeta_debito": 0.90,   # 90% de éxito
            "paypal": 0.80,           # 80% de éxito
            "transferencia": 0.95,    # 95% de éxito
            "efectivo": 1.0           # 100% de éxito
        }
        
        # Si el método no está reconocido, usamos una probabilidad baja
        probabilidad_exito = validaciones.get(metodo_pago.lower(), 0.50)
        
        # Validamos también que el monto sea válido
        if monto <= 0:
            return False
        
        # Simulamos el resultado de la validación
        return random.random() < probabilidad_exito