from EstadoPago import EstadoPago
from EstadoRegistrado import EstadoRegistrado
from datetime import datetime


class Pago:
    """
    Clase principal que representa un pago y utiliza el patrón State.
    Esta clase actúa como el contexto que delega las operaciones al estado actual.
    """
    
    def __init__(self, id_pago: str, monto: float, metodo_pago: str):
        """
        Inicializa un nuevo pago en estado REGISTRADO.
        
        Args:
            id_pago: Identificador único del pago
            monto: Monto del pago (debe ser mayor a 0)
            metodo_pago: Método de pago (ej: "tarjeta_credito", "paypal", etc.)
        """
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        
        if not id_pago or not id_pago.strip():
            raise ValueError("El ID del pago no puede estar vacío")
        
        if not metodo_pago or not metodo_pago.strip():
            raise ValueError("El método de pago no puede estar vacío")
        
        self.id = id_pago.strip()
        self.monto = float(monto)
        self.metodo_pago = metodo_pago.strip()
        self.fecha_creacion = datetime.now()
        self.fecha_ultima_modificacion = datetime.now()
        
        # Estado inicial: REGISTRADO
        self._estado: EstadoPago = EstadoRegistrado()
        
        print(f"✓ Pago creado: ID={self.id}, Monto=${self.monto:.2f}, Método={self.metodo_pago}")
    
    def pagar(self) -> bool:
        """
        Intenta procesar el pago delegando la operación al estado actual.
        
        Returns:
            bool: True si el pago fue exitoso, False si falló
        """
        resultado = self._estado.pagar(self)
        if resultado:
            self.fecha_ultima_modificacion = datetime.now()
        return resultado
    
    def revertir(self) -> bool:
        """
        Intenta revertir el pago delegando la operación al estado actual.
        
        Returns:
            bool: True si la reversión fue exitosa, False si no es posible
        """
        resultado = self._estado.revertir(self)
        if resultado:
            self.fecha_ultima_modificacion = datetime.now()
        return resultado
    
    def actualizar(self, nuevo_monto: float = None, nuevo_metodo: str = None) -> bool:
        """
        Intenta actualizar los datos del pago delegando la operación al estado actual.
        
        Args:
            nuevo_monto: Nuevo monto del pago (opcional)
            nuevo_metodo: Nuevo método de pago (opcional)
            
        Returns:
            bool: True si la actualización fue exitosa, False si no es posible
        """
        # Validaciones antes de delegar al estado
        if nuevo_monto is not None and nuevo_monto <= 0:
            print(f"✗ Error: El nuevo monto debe ser mayor a 0 (recibido: {nuevo_monto})")
            return False
        
        if nuevo_metodo is not None and (not nuevo_metodo or not nuevo_metodo.strip()):
            print(f"✗ Error: El nuevo método de pago no puede estar vacío")
            return False
        
        resultado = self._estado.actualizar(self, nuevo_monto, nuevo_metodo)
        if resultado:
            self.fecha_ultima_modificacion = datetime.now()
        return resultado
    
    def get_estado(self) -> str:
        """
        Obtiene el nombre del estado actual.
        
        Returns:
            str: Nombre del estado actual
        """
        return self._estado.get_nombre_estado()
    
    def _cambiar_estado(self, nuevo_estado: EstadoPago) -> None:
        """
        Método interno para cambiar el estado del pago.
        Solo debe ser llamado por los estados concretos.
        
        Args:
            nuevo_estado: El nuevo estado al que cambiar
        """
        estado_anterior = self._estado.get_nombre_estado()
        self._estado = nuevo_estado
        print(f"🔄 Estado del pago {self.id}: {estado_anterior} → {nuevo_estado.get_nombre_estado()}")
    
    def get_info(self) -> dict:
        """
        Obtiene información completa del pago.
        
        Returns:
            dict: Diccionario con toda la información del pago
        """
        return {
            "id": self.id,
            "monto": self.monto,
            "metodo_pago": self.metodo_pago,
            "estado": self.get_estado(),
            "fecha_creacion": self.fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
            "fecha_ultima_modificacion": self.fecha_ultima_modificacion.strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def mostrar_info(self) -> None:
        """Muestra la información del pago de forma legible."""
        info = self.get_info()
        print(f"\n--- Información del Pago ---")
        print(f"ID: {info['id']}")
        print(f"Estado: {info['estado']}")
        print(f"Monto: ${info['monto']:.2f}")
        print(f"Método: {info['metodo_pago']}")
        print(f"Creado: {info['fecha_creacion']}")
        print(f"Modificado: {info['fecha_ultima_modificacion']}")
        print("--- ------------------------ ---\n")
    
    def __str__(self) -> str:
        """Representación string del pago."""
        return f"Pago(id={self.id}, estado={self.get_estado()}, monto=${self.monto:.2f}, metodo={self.metodo_pago})"
    
    def __repr__(self) -> str:
        """Representación técnica del pago."""
        return self.__str__()