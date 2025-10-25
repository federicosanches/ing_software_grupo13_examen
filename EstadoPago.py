from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Pago import Pago


class EstadoPago(ABC):
    """
    Interfaz abstracta que define las operaciones disponibles 
    para los diferentes estados de un pago.
    """
    
    @abstractmethod
    def pagar(self, pago: 'Pago') -> bool:
        """
        Intenta procesar el pago según el método de pago seleccionado.
        
        Args:
            pago: El objeto pago que cambiará de estado
            
        Returns:
            bool: True si el pago fue exitoso, False si falló
        """
        pass
    
    @abstractmethod
    def revertir(self, pago: 'Pago') -> bool:
        """
        Revierte el pago al estado REGISTRADO.
        
        Args:
            pago: El objeto pago que cambiará de estado
            
        Returns:
            bool: True si la reversión fue exitosa, False si no es posible
        """
        pass
    
    @abstractmethod
    def actualizar(self, pago: 'Pago', nuevo_monto: float = None, nuevo_metodo: str = None) -> bool:
        """
        Actualiza los atributos del pago.
        
        Args:
            pago: El objeto pago a actualizar
            nuevo_monto: Nuevo monto del pago (opcional)
            nuevo_metodo: Nuevo método de pago (opcional)
            
        Returns:
            bool: True si la actualización fue exitosa, False si no es posible
        """
        pass
    
    @abstractmethod
    def get_nombre_estado(self) -> str:
        """
        Retorna el nombre del estado actual.
        
        Returns:
            str: Nombre del estado
        """
        pass