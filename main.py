import json

from fastapi import FastAPI
from Pago import Pago

STATUS = "status"
AMOUNT = "amount"
PAYMENT_METHOD = "payment_method"

STATUS_REGISTRADO = "REGISTRADO"
STATUS_PAGADO = "PAGADO"
STATUS_FALLIDO = "FALLIDO"

DATA_PATH = "data.json"

app = FastAPI()


def load_all_payments():
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


def save_all_payments(data):
    with open(DATA_PATH, "w") as f:
        json.dump(data, f, indent=4)


def load_payment(payment_id):
    data = load_all_payments()[payment_id]
    return data


def save_payment_data(payment_id, data):
    all_data = load_all_payments()
    all_data[str(payment_id)] = data
    save_all_payments(all_data)


def save_payment(payment_id, amount, payment_method, status):
    data = {
        AMOUNT: amount,
        PAYMENT_METHOD: payment_method,
        STATUS: status,
    }
    save_payment_data(payment_id, data)


""" if __name__ == "__main__":        
    pago_cargado = Pago.load_from_json("TC001")
    print(pago_cargado)
    
    pago_cargado.pagar()
    print(pago_cargado) """

# Endpoints a implementar:

# * POST en el path /payments/{payment_id} que registre un nuevo pago.
# * POST en el path /payments/{payment_id}/update que cambie los parametros de una pago (amount, payment_method)
# * POST en el path /payments/{payment_id}/pay que intente.
# * POST en el path /payments/{payment_id}/revert que revertir el pago.


# * GET en el path /payments que retorne todos los pagos.
@app.get("/payments")
async def get_payments():
    return load_all_payments()
