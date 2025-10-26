from EstadoPago import EstadoPago
from EstadoPagado import EstadoPagado
from EstadoFallido import EstadoFallido
from typing import TYPE_CHECKING
from utils import STATUS, PAYMENT_METHOD, STATUS_REGISTRADO, DATA_PATH
import json

if TYPE_CHECKING:
    from Pago import Pago


class EstadoRegistrado(EstadoPago):
    """
    Estado REGISTRADO - El pago fue registrado pero aún no procesado.
    Permite: pagar, revertir (sin efecto), actualizar
    """
    def __init__(self, pago):
        self.pago = pago

    def pagar(self, pago: 'Pago') -> bool:
        """
        Procesa el pago y cambia al estado PAGADO o FALLIDO según la validación.
        """
        print(f"Procesando pago {pago.id} con método {pago.data['payment_method']}...")
        
        es_valido = self._validar_pago(pago.data['payment_method'], pago.data['amount'])
        
        if es_valido:
            print(f"✓ Pago {pago.id} procesado exitosamente")
            pago._cambiar_estado(EstadoPagado(pago))
            return True
        else:
            print(f"✗ Error al procesar el pago {pago.id}")
            pago._cambiar_estado(EstadoFallido(pago))
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
            monto_anterior = pago.data['amount']
            pago.data['amount'] = nuevo_monto
            cambios_realizados.append(f"monto: ${monto_anterior:.2f} → ${nuevo_monto:.2f}")
        
        if nuevo_metodo is not None:
            metodo_anterior = pago.data['payment_method']
            pago.data['payment_method'] = nuevo_metodo
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
        Valida el pago según el método seleccionado con las reglas específicas.
        
        Args:
            metodo_pago: Método de pago a validar
            monto: Monto del pago
            
        Returns:
            bool: True si la validación es exitosa, False en caso contrario
        """
        
        # Método 1: Tarjeta de Crédito
        if metodo_pago == "tarjeta_credito":
            # Condición 1: Verifica que el pago sea menor a $10,000
            if monto >= 10000:
                print(f"✗ Validación fallida: Monto ${monto:.2f} excede el límite de $10,000 para tarjeta de crédito")
                return False
            
            # Condición 2: Valida que no haya más de 1 pago con este medio en estado REGISTRADO
            pagos_registrados = self._contar_pagos_registrados_por_metodo("tarjeta_credito")
            if pagos_registrados >= 1:
                print(f"✗ Validación fallida: Ya existe {pagos_registrados} pago(s) con tarjeta de crédito en estado REGISTRADO")
                return False
            
            print(f"✓ Validación exitosa para tarjeta de crédito: ${monto:.2f}")
            return True
        
        # Método 2: PayPal
        elif metodo_pago == "paypal":
            # Condición: Verifica que el pago sea menor de $5,000
            if monto >= 5000:
                print(f"✗ Validación fallida: Monto ${monto:.2f} excede el límite de $5,000 para PayPal")
                return False
            
            print(f"✓ Validación exitosa para PayPal: ${monto:.2f}")
            return True
        
        else:
            print(f"✗ Método de pago '{metodo_pago}' no reconocido")
            return False
    
    def _contar_pagos_registrados_por_metodo(self, metodo_pago: str) -> int:
        """
        Cuenta cuántos pagos están en estado REGISTRADO con el método de pago especificado.
        
        Args:
            metodo_pago: Método de pago a contar
            
        Returns:
            int: Número de pagos registrados con ese método
        """
        try:
            # Cargar datos del JSON
            try:
                with open(DATA_PATH, "r") as f:
                    content = f.read().strip()
                    if not content:
                        return 0
                    all_data = json.loads(content)
            except (FileNotFoundError, json.JSONDecodeError):
                return 0
            
            # Contar pagos con el método especificado en estado REGISTRADO
            contador = 0
            for pago_data in all_data.values():
                if (pago_data.get(PAYMENT_METHOD) == metodo_pago and 
                    pago_data.get(STATUS) == STATUS_REGISTRADO):
                    contador += 1
            
            print(f"ℹ Pagos encontrados con {metodo_pago} en estado REGISTRADO: {contador}")
            return contador
            
        except Exception as e:
            print(f"⚠ Error contando pagos registrados: {e}")
            return 0  # En caso de error, asumimos 0 para no bloquear