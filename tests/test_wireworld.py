"""Testes da lógica Wireworld sem abrir a janela gráfica do Pyxel."""
import sys
import types
import unittest
from pathlib import Path

# A biblioteca gráfica é necessária para executar a interface, mas não para
# testar as regras de transição dos estados da grade.
sys.modules.setdefault("pyxel", types.ModuleType("pyxel"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from wireworld import Wireworld, EMPTY, CONDUCTOR, ELECTRON_HEAD, ELECTRON_TAIL


def simular(matriz):
    app = Wireworld.__new__(Wireworld)
    app.grid = [linha[:] for linha in matriz]
    app.grid_h = len(matriz)
    app.grid_w = len(matriz[0])
    app.generation = 0
    app.step()
    return app


class TestWireworld(unittest.TestCase):
    def test_cabeca_vira_cauda(self):
        self.assertEqual(simular([[ELECTRON_HEAD]]).grid, [[ELECTRON_TAIL]])

    def test_cauda_vira_condutor(self):
        self.assertEqual(simular([[ELECTRON_TAIL]]).grid, [[CONDUCTOR]])

    def test_vazio_permanece_vazio(self):
        self.assertEqual(simular([[EMPTY]]).grid, [[EMPTY]])

    def test_condutor_sem_cabeca_permanece_condutor(self):
        self.assertEqual(simular([[CONDUCTOR]]).grid, [[CONDUCTOR]])

    def test_condutor_com_uma_cabeca_vira_cabeca(self):
        self.assertEqual(simular([[CONDUCTOR, ELECTRON_HEAD]]).grid[0][0], ELECTRON_HEAD)

    def test_condutor_com_duas_cabecas_vira_cabeca(self):
        self.assertEqual(simular([[ELECTRON_HEAD, CONDUCTOR, ELECTRON_HEAD]]).grid[0][1], ELECTRON_HEAD)

    def test_condutor_com_tres_cabecas_nao_muda(self):
        matriz = [[ELECTRON_HEAD, ELECTRON_HEAD, EMPTY], [ELECTRON_HEAD, CONDUCTOR, EMPTY]]
        self.assertEqual(simular(matriz).grid[1][1], CONDUCTOR)

    def test_vizinhanca_diagonal(self):
        self.assertEqual(simular([[CONDUCTOR, EMPTY], [EMPTY, ELECTRON_HEAD]]).grid[0][0], ELECTRON_HEAD)

    def test_contador_incrementa_uma_vez(self):
        self.assertEqual(simular([[EMPTY]]).generation, 1)

    def test_geracao_simultanea(self):
        # O condutor da direita não deve reagir à cabeça recém-criada no centro.
        matriz = [[ELECTRON_HEAD, CONDUCTOR, CONDUCTOR]]
        self.assertEqual(simular(matriz).grid, [[ELECTRON_TAIL, ELECTRON_HEAD, CONDUCTOR]])


if __name__ == "__main__":
    unittest.main()
