from EstadoPago import EstadoPago
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Pago import Pago


class EstadoFallido(EstadoPago):
    """
    Estado FALLIDO - El pago falló durante el procesamiento.
    Permite: revertir (vuelve a REGISTRADO)
    No permite: pagar (debe revertirse primero), actualizar
    """
    
    def pagar(self, pago: 'Pago') -> bool:
        """
        No se puede procesar un pago que está en estado FALLIDO.
        Debe revertirse primero.
        """
        print(f"✗ Error: No se puede procesar el pago {pago.id} porque se encuentra en estado FALLIDO.")
        print("  Para procesar el pago, primero debe revertirlo al estado REGISTRADO.")
        return False
    
    def revertir(self, pago: 'Pago') -> bool:
        """
        Revierte el pago fallido al estado REGISTRADO para permitir un nuevo intento.
        """
        print(f"↺ Revirtiendo pago {pago.id} de FALLIDO a REGISTRADO...")
        from EstadoRegistrado import EstadoRegistrado
        pago._cambiar_estado(EstadoRegistrado())
        print(f"✓ Pago {pago.id} revertido exitosamente. Ahora puede ser procesado nuevamente.")
        return True
    
    def actualizar(self, pago: 'Pago', nuevo_monto: float = None, nuevo_metodo: str = None) -> bool:
        """
        No se pueden actualizar los datos de un pago fallido.
        Debe revertirse primero.
        """
        print(f"✗ Error: No se puede actualizar el pago {pago.id} porque se encuentra en estado FALLIDO.")
        print("  Para modificar el pago, primero debe revertirlo al estado REGISTRADO.")
        return False
    
    def get_nombre_estado(self) -> str:
        """Retorna el nombre del estado."""
        return "FALLIDO"