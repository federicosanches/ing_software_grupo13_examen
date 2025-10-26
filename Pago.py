from EstadoPago import EstadoPago
from EstadoPagado import EstadoPagado
from EstadoFallido import EstadoFallido
from EstadoRegistrado import EstadoRegistrado
from utils import (
    STATUS,
    STATUS_REGISTRADO,
    STATUS_PAGADO,
    STATUS_FALLIDO,
    AMOUNT,
    PAYMENT_METHOD,
    load_payment,
    load_all_payments,
    save_payment_data,
)


class Pago:
    """
    Clase principal que representa un pago y utiliza el patrón State.
    Esta clase actúa como el contexto que delega las operaciones al estado actual.
    """

    def __init__(self, id, amount: float = None, payment_method: str = None):
        self.id = str(id)
        all_data = load_all_payments()

        # Si el pago no existe todavía se crea en estado REGISTRADO
        if self.id not in all_data:
            if amount is None or payment_method is None:
                raise ValueError("Para crear un nuevo pago se requieren amount y payment_method.")
            self.data = {
                AMOUNT: amount,
                PAYMENT_METHOD: payment_method,
                STATUS: STATUS_REGISTRADO,
            }
            save_payment_data(self.id, self.data)
        else:
            self.data = all_data[self.id]

        status = self.data.get(STATUS)
        if status == STATUS_PAGADO:
            self._estado: EstadoPago = EstadoPagado(self)
        elif status == STATUS_FALLIDO:
            self._estado: EstadoPago = EstadoFallido(self)
        else:
            self._estado: EstadoPago = EstadoRegistrado(self)

    def get_estado(self):
        """
        Obtiene el nombre del estado actual.
        """
        return self._estado.get_nombre_estado()

    def _cambiar_estado(self, nuevo_estado: EstadoPago):
        """
        Método interno para cambiar el estado del pago.
        """
        estado_anterior = self._estado.get_nombre_estado()
        self._estado = nuevo_estado
        self.data[STATUS] = nuevo_estado.get_nombre_estado()
        self.save()

    def pagar(self):
        self._estado.pagar(self)
        self.save()

    def revertir(self):
        self._estado.revertir(self)
        self.save()

    def actualizar(self, amount=None, payment_method=None):
        self._estado.actualizar(self, amount, payment_method)
        self.save()

    def save(self):
        save_payment_data(self.id, self.data)