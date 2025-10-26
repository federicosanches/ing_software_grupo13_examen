from EstadoPago import EstadoPago
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Pago import Pago


class EstadoPagado(EstadoPago):
    """
    Estado PAGADO - El pago fue procesado exitosamente.
    No permite: pagar (ya está pagado), revertir, actualizar
    Es un estado final.
    """
    def __init__(self, pago):
        self.pago = pago
        
    def pagar(self, pago: 'Pago') -> bool:
        """
        No se puede pagar un pago que ya está en estado PAGADO.
        """
        print(f"✗ Error: El pago {pago.id} ya se encuentra PAGADO. No se puede procesar nuevamente.")
        return False
    
    def revertir(self, pago: 'Pago') -> bool:
        """
        No se puede revertir un pago que ya fue procesado exitosamente.
        """
        print(f"✗ Error: No se puede revertir el pago {pago.id} porque ya fue procesado exitosamente.")
        print("  Los pagos PAGADOS no pueden ser revertidos por motivos de seguridad.")
        return False
    
    def actualizar(self, pago: 'Pago', nuevo_monto: float = None, nuevo_metodo: str = None) -> bool:
        """
        No se pueden actualizar los datos de un pago ya procesado.
        """
        print(f"✗ Error: No se puede actualizar el pago {pago.id} porque ya fue procesado.")
        print("  Los pagos PAGADOS son inmutables por motivos de auditoría.")
        return False
    
    def get_nombre_estado(self) -> str:
        """Retorna el nombre del estado."""
        return "PAGADO"