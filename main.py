from fastapi import FastAPI
from Pago import Pago
from utils import load_all_payments

app = FastAPI()

# * GET en el path /payments que retorne todos los pagos.
@app.get("/payments")
async def get_payments():
    return load_all_payments()


# * POST en el path /payments/{payment_id} que registre un nuevo pago.
@app.post("/payments/{payment_id}")
async def create_payment(payment_id: str, amount: float, payment_method: str):
    pago = Pago(payment_id, amount, payment_method)
    return {
            "message": f"Pago {payment_id} registrado correctamente.",
            "estado": pago.get_estado(),
            "data": pago.data,
        }


# * POST en el path /payments/{payment_id}/update que cambie los parametros de una pago (amount, payment_method)
@app.post("/payments/{payment_id}/update")
async def update_payment(payment_id: str, amount: float, payment_method: str):
    pago = Pago(payment_id)
    pago.actualizar(amount, payment_method)
    return {"data": pago.data}


# * POST en el path /payments/{payment_id}/pay que intente.
@app.post("/payments/{payment_id}/pay")
async def pay_payment(payment_id: str):
    pago = Pago(payment_id)
    pago.pagar()
    return {
            "message": f"Pago {payment_id} procesado.",
            "estado": pago.get_estado(),
            "data": pago.data,
        }


# * POST en el path /payments/{payment_id}/revert que revertir el pago.
@app.post("/payments/{payment_id}/revert")
async def revert_payment(payment_id: str):
    pago = Pago(payment_id)
    pago.revertir()
    return {
            "message": f"Pago {payment_id} revertido correctamente.",
            "estado": pago.get_estado(),
            "data": pago.data,
        }