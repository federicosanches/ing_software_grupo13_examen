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



# * GET en el path /payments que retorne todos los pagos.
@app.get("/payments")
async def get_payments():
    return load_all_payments()

# * GET en el path /payments/{payment_id} que retorne todos los pagos.
@app.get("/payments/{payment_id}")
async def get_payment(payment_id: str):
    pago = Pago.load_from_json(payment_id)
    return pago.get_info()


# * POST en el path /payments/{payment_id} que registre un nuevo pago.
@app.post("/payments/{payment_id}")
async def create_payment(payment_id: str, amount: float, payment_method: str):
    save_payment(payment_id, amount, payment_method, STATUS_REGISTRADO)
    return {"message": "Payment created successfully"}


# * POST en el path /payments/{payment_id}/update que cambie los parametros de una pago (amount, payment_method)
@app.post("/payments/{payment_id}/update")
async def update_payment(payment_id: str, amount: float, payment_method: str):
    pago = Pago.load_from_json(payment_id)
    pago.actualizar(amount, payment_method)
    return pago.get_info()


# * POST en el path /payments/{payment_id}/pay que intente.
@app.post("/payments/{payment_id}/pay")
async def pay_payment(payment_id: str):
    pago = Pago.load_from_json(payment_id)
    pago.pagar()
    return pago.get_info()


# * POST en el path /payments/{payment_id}/revert que revertir el pago.
@app.post("/payments/{payment_id}/revert")
async def revert_payment(payment_id: str):
    pago = Pago.load_from_json(payment_id)
    pago.revertir()
    return pago.get_info()