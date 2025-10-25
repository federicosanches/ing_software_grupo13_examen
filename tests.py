import unittest
import os
import json
from Pago import Pago
import Pago as PagoModule


# Usamos un archivo específico para los tests llamado data_tests.json
# Esto nos permite tener un entorno aislado y no tocar data.json de producción.


class TestPagoState(unittest.TestCase):
    def setUp(self):
        # Guardar ruta original para restaurar después
        self._orig_data_path = PagoModule.DATA_PATH

        # Ruta del archivo de pruebas
        self.test_data_path = "data_tests.json"

        # Inicializar archivo de tests vacío
        with open(self.test_data_path, "w", encoding="utf-8") as f:
            json.dump({}, f)

        # Indicar al módulo Pago que use este archivo durante los tests
        PagoModule.DATA_PATH = self.test_data_path

    def tearDown(self):
        # Restaurar ruta original
        PagoModule.DATA_PATH = self._orig_data_path

        # Borrar archivo de tests
        try:
            os.remove(self.test_data_path)
        except OSError:
            pass

    def test_crear_pago_registrado(self):
        """Crear un pago con auto_save=False debe quedar en REGISTRADO y mantener datos."""
        pago = Pago("T1", 100.0, "paypal", auto_save=False)
        self.assertEqual(pago.get_estado(), "REGISTRADO")
        self.assertEqual(pago.monto, 100.0)
        self.assertEqual(pago.metodo_pago, "paypal")

    def test_pago_exitoso_paypal_becomes_pagado(self):
        """Un pago con PayPal y monto válido debe procesarse y quedar PAGADO."""
        pago = Pago("T2", 100.0, "paypal", auto_save=False)
        resultado = pago.pagar()
        self.assertTrue(resultado)
        self.assertEqual(pago.get_estado(), "PAGADO")

    def test_pago_fallido_y_revertir(self):
        """Un pago con tarjeta_credito y monto alto debe FALLAR y poder revertirse a REGISTRADO."""
        pago = Pago("T3", 15000.0, "tarjeta_credito", auto_save=False)
        resultado = pago.pagar()
        self.assertFalse(resultado)
        self.assertEqual(pago.get_estado(), "FALLIDO")

        # Revertir debe devolver al estado REGISTRADO
        revertido = pago.revertir()
        self.assertTrue(revertido)
        self.assertEqual(pago.get_estado(), "REGISTRADO")

    def test_no_actualizar_fallido_y_pagado(self):
        """No se debe poder actualizar un pago en estado FALLIDO ni en PAGADO."""
        # FALLIDO
        pago_f = Pago("F1", 15000.0, "tarjeta_credito", auto_save=False)
        pago_f.pagar()
        self.assertEqual(pago_f.get_estado(), "FALLIDO")
        self.assertFalse(pago_f.actualizar(nuevo_monto=14000.0))

        # PAGADO
        pago_p = Pago("P1", 100.0, "paypal", auto_save=False)
        self.assertTrue(pago_p.pagar())
        self.assertEqual(pago_p.get_estado(), "PAGADO")
        self.assertFalse(pago_p.actualizar(nuevo_monto=200.0))

    def test_no_revertir_pagado(self):
        """Un pago en estado PAGADO no debe poder revertirse."""
        pago = Pago("P2", 100.0, "paypal", auto_save=False)
        pago.pagar()
        self.assertEqual(pago.get_estado(), "PAGADO")
        self.assertFalse(pago.revertir())

    def test_flujo_revertir_actualizar_y_pagar(self):
        """Flujo completo: FALLIDO -> revertir -> actualizar monto -> pagar (exitoso)."""
        pago = Pago("FLOW1", 15000.0, "tarjeta_credito", auto_save=False)
        # falla inicialmente
        self.assertFalse(pago.pagar())
        self.assertEqual(pago.get_estado(), "FALLIDO")

        # revertir a REGISTRADO
        self.assertTrue(pago.revertir())
        self.assertEqual(pago.get_estado(), "REGISTRADO")

        # actualizar a monto válido
        self.assertTrue(pago.actualizar(nuevo_monto=5000.0))

        # intentar pagar de nuevo y que pase
        self.assertTrue(pago.pagar())
        self.assertEqual(pago.get_estado(), "PAGADO")


if __name__ == '__main__':
    unittest.main()