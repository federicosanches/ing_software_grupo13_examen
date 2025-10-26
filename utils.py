import json

STATUS = "status"
AMOUNT = "amount"
PAYMENT_METHOD = "payment_method"

STATUS_REGISTRADO = "REGISTRADO"
STATUS_PAGADO = "PAGADO"
STATUS_FALLIDO = "FALLIDO"

DATA_PATH = "data.json"

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