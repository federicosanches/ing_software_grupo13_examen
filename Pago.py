from EstadoPago import EstadoPago
from EstadoRegistrado import EstadoRegistrado
from datetime import datetime
import json

# Importar constantes de main.py
STATUS = "status"
AMOUNT = "amount"
PAYMENT_METHOD = "payment_method"

STATUS_REGISTRADO = "REGISTRADO"
STATUS_PAGADO = "PAGADO"
STATUS_FALLIDO = "FALLIDO"

DATA_PATH = "data.json"


class Pago:
    """
    Clase principal que representa un pago y utiliza el patrón State.
    Esta clase actúa como el contexto que delega las operaciones al estado actual.
    """
    
    def __init__(self, id_pago: str, monto: float, metodo_pago: str, auto_save: bool = True):
        """
        Inicializa un nuevo pago en estado REGISTRADO.
        
        Args:
            id_pago: Identificador único del pago
            monto: Monto del pago (debe ser mayor a 0)
            metodo_pago: Método de pago (ej: "tarjeta_credito", "paypal", etc.)
            auto_save: Si debe guardar automáticamente en JSON (default: True)
        """
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        
        if not id_pago or not str(id_pago).strip():
            raise ValueError("El ID del pago no puede estar vacío")
        
        if not metodo_pago or not metodo_pago.strip():
            raise ValueError("El método de pago no puede estar vacío")
        
        self.id = str(id_pago).strip()
        self.monto = float(monto)
        self.metodo_pago = metodo_pago.strip()
        self.fecha_creacion = datetime.now()
        self.fecha_ultima_modificacion = datetime.now()
        self.auto_save = auto_save
        
        # Estado inicial: REGISTRADO
        self._estado: EstadoPago = EstadoRegistrado()
        
        print(f"✓ Pago creado: ID={self.id}, Monto=${self.monto:.2f}, Método={self.metodo_pago}")
        
        # Guardar automáticamente si está habilitado
        if self.auto_save:
            self.save_to_json()
    
    def pagar(self) -> bool:
        """
        Intenta procesar el pago delegando la operación al estado actual.
        
        Returns:
            bool: True si el pago fue exitoso, False si falló
        """
        resultado = self._estado.pagar(self)
        if resultado:
            self.fecha_ultima_modificacion = datetime.now()
            if self.auto_save:
                self.save_to_json()
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
            if self.auto_save:
                self.save_to_json()
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
            if self.auto_save:
                self.save_to_json()
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
        
        # Guardar automáticamente el cambio de estado
        if self.auto_save:
            self.save_to_json()
    
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
    
    # Métodos de integración con JSON (compatible con main.py)
    
    def save_to_json(self) -> None:
        """Guarda este pago en el archivo JSON usando el formato de main.py."""
        try:
            all_data = self.load_all_payments()
            all_data[str(self.id)] = {
                AMOUNT: self.monto,
                PAYMENT_METHOD: self.metodo_pago,
                STATUS: self.get_estado(),
            }
            self.save_all_payments(all_data)
        except Exception as e:
            print(f"⚠ Error guardando pago {self.id}: {e}")
    
    @staticmethod
    def load_all_payments():
        """Carga todos los pagos desde el archivo JSON (compatible con main.py)."""
        try:
            with open(DATA_PATH, "r") as f:
                content = f.read().strip()
                if not content:  # Archivo vacío
                    return {}
                data = json.loads(content)
            return data
        except FileNotFoundError:
            # Si el archivo no existe, retornamos un diccionario vacío
            return {}
        except json.JSONDecodeError:
            # Si hay un error de JSON, retornamos un diccionario vacío
            print(f"Warning: Error leyendo {DATA_PATH}, iniciando con datos vacíos")
            return {}
    
    @staticmethod
    def save_all_payments(data):
        """Guarda todos los pagos en el archivo JSON (compatible con main.py)."""
        with open(DATA_PATH, "w") as f:
            json.dump(data, f, indent=4)
    
    @classmethod
    def load_from_json(cls, payment_id: str) -> 'Pago':
        """
        Carga un pago específico desde el archivo JSON y crea una instancia de Pago.
        
        Args:
            payment_id: ID del pago a cargar
            
        Returns:
            Pago: Instancia de Pago cargada desde JSON
            
        Raises:
            KeyError: Si el pago no existe
            ValueError: Si los datos del JSON son inválidos
        """
        all_data = cls.load_all_payments()
        
        if str(payment_id) not in all_data:
            raise KeyError(f"Pago {payment_id} no encontrado en {DATA_PATH}")
        
        pago_data = all_data[str(payment_id)]
        
        # Crear instancia de Pago sin auto-guardado para evitar recursión
        pago = cls(
            id_pago=str(payment_id),
            monto=pago_data[AMOUNT],
            metodo_pago=pago_data[PAYMENT_METHOD],
            auto_save=False
        )
        
        # Establecer el estado correcto basado en el JSON
        estado_json = pago_data[STATUS]
        if estado_json != STATUS_REGISTRADO:
            pago._simular_estado(estado_json)
        
        # Reactivar auto-guardado
        pago.auto_save = True
        
        return pago
    
    def _simular_estado(self, estado_deseado: str) -> None:
        """
        Método interno para simular un estado específico (para carga desde JSON).
        
        Args:
            estado_deseado: Estado al que se debe cambiar ("PAGADO" o "FALLIDO")
        """
        if estado_deseado == STATUS_PAGADO:
            from EstadoPagado import EstadoPagado
            self._estado = EstadoPagado()
        elif estado_deseado == STATUS_FALLIDO:
            from EstadoFallido import EstadoFallido
            self._estado = EstadoFallido()
        # Si es REGISTRADO, no hacer nada (ya es el estado por defecto)
    
    @classmethod
    def get_all_from_json(cls) -> dict:
        """
        Obtiene todos los pagos desde el archivo JSON como instancias de Pago.
        
        Returns:
            dict: Diccionario con payment_id como clave y instancia Pago como valor
        """
        all_data = cls.load_all_payments()
        pagos = {}
        
        for payment_id in all_data.keys():
            try:
                pagos[payment_id] = cls.load_from_json(payment_id)
            except Exception as e:
                print(f"⚠ Error cargando pago {payment_id}: {e}")
        
        return pagos
    
    def delete_from_json(self) -> bool:
        """
        Elimina este pago del archivo JSON.
        
        Returns:
            bool: True si se eliminó exitosamente, False si no existía
        """
        try:
            all_data = self.load_all_payments()
            if str(self.id) in all_data:
                del all_data[str(self.id)]
                self.save_all_payments(all_data)
                print(f"✓ Pago {self.id} eliminado del archivo JSON")
                return True
            else:
                print(f"ℹ Pago {self.id} no encontrado en el archivo JSON")
                return False
        except Exception as e:
            print(f"⚠ Error eliminando pago {self.id}: {e}")
            return False