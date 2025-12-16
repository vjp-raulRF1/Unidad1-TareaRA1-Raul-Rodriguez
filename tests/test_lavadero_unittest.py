import unittest
from src.lavadero import Lavadero

class TestLavadero(unittest.TestCase):
    def setUp(self):
        self.lavadero = Lavadero()

    def test1_estado_inicial_correcto(self):
        """Test 1: Estado inicial del lavadero."""
        self.assertEqual(self.lavadero.fase, Lavadero.FASE_INACTIVO)
        self.assertEqual(self.lavadero.ingresos, 0.0)
        self.assertFalse(self.lavadero.ocupado)
        self.assertFalse(self.lavadero.prelavado_a_mano)
        self.assertFalse(self.lavadero.secado_a_mano)
        self.assertFalse(self.lavadero.encerado)

    def test2_excepcion_encerado_sin_secado(self):
        """Test 2: Encerado sin secado lanza ValueError."""
        with self.assertRaises(ValueError):
            self.lavadero.hacerLavado(False, False, True)

    def test3_excepcion_lavado_mientras_otro_en_marcha(self):
        """Test 3: Segundo lavado durante primero."""
        self.lavadero.hacerLavado(False, False, False)
        with self.assertRaises(ValueError):
            self.lavadero.hacerLavado(True, True, True)

    def _cobrar_y_devolver_coste(self, prelav, secado, encer):
        """Auxiliar para tests de ingresos."""
        ingresos_antes = self.lavadero.ingresos
        self.lavadero.hacerLavado(prelav, secado, encer)
        self.lavadero.avanzarFase()
        return round(self.lavadero.ingresos - ingresos_antes, 2)

    def test4_ingresos_prelavado_mano(self):
        """Test 4: Prelavado mano = 6.50€."""
        coste = self._cobrar_y_devolver_coste(True, False, False)
        self.assertEqual(coste, 6.50)

    def test5_ingresos_secado_mano(self):
        """Test 5: Secado mano = 6.00€."""
        coste = self._cobrar_y_devolver_coste(False, True, False)
        self.assertEqual(coste, 6.00)

    def test6_ingresos_secado_encerado(self):
        """Test 6: Secado + encerado = 7.20€."""
        coste = self._cobrar_y_devolver_coste(False, True, True)
        self.assertEqual(coste, 7.20)

    def test7_ingresos_prelavado_secado(self):
        """Test 7: Prelavado + secado = 7.50€."""
        coste = self._cobrar_y_devolver_coste(True, True, False)
        self.assertEqual(coste, 7.50)

    def test8_ingresos_todos_extras(self):
        """Test 8: Todos extras = 8.70€."""
        coste = self._cobrar_y_devolver_coste(True, True, True)
        self.assertEqual(coste, 8.70)

    def _ejecutar_y_obtener_fases(self, prelavado, secado, encerado):
        """Auxiliar para tests de fases."""
        fases = [self.lavadero.fase]
        self.lavadero.hacerLavado(prelavado, secado, encerado)
        while self.lavadero.ocupado:
            self.lavadero.avanzarFase()
            fases.append(self.lavadero.fase)
        return fases

    def test9_flujo_sin_extras(self):
        """Test 9: Sin extras [0,1,3,4,5,6,0]."""
        fases = self._ejecutar_y_obtener_fases(False, False, False)
        self.assertEqual(fases, [0, 1, 3, 4, 5, 6, 0])

    def test10_flujo_prelavado(self):
        """Test 10: Prelavado [0,1,2,3,4,5,6,0]."""
        fases = self._ejecutar_y_obtener_fases(True, False, False)
        self.assertEqual(fases, [0, 1, 2, 3, 4, 5, 6, 0])

    def test11_flujo_secado(self):
        """Test 11: Secado [0,1,3,4,5,7,0]."""
        fases = self._ejecutar_y_obtener_fases(False, True, False)
        self.assertEqual(fases, [0, 1, 3, 4, 5, 7, 0])

    def test12_flujo_secado_encerado(self):
        """Test 12: Secado+encerado [0,1,3,4,5,7,8,0]."""
        fases = self._ejecutar_y_obtener_fases(False, True, True)
        self.assertEqual(fases, [0, 1, 3, 4, 5, 7, 8, 0])

    def test13_flujo_prelavado_secado(self):
        """Test 13: Prelavado+secado [0,1,2,3,4,5,7,0]."""
        fases = self._ejecutar_y_obtener_fases(True, True, False)
        self.assertEqual(fases, [0, 1, 2, 3, 4, 5, 7, 0])

    def test14_flujo_todos_extras(self):
        """Test 14: Todos extras [0,1,2,3,4,5,7,8,0]."""
        fases = self._ejecutar_y_obtener_fases(True, True, True)
        self.assertEqual(fases, [0, 1, 2, 3, 4, 5, 7, 8, 0])

if __name__ == "__main__":
    unittest.main()
