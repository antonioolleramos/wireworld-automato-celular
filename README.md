# ⚡ Wireworld — Autômato Celular Interativo

Simulador gráfico do **Wireworld**, um autômato celular que representa a propagação de sinais por condutores em uma grade bidimensional. Desenvolvido em **Python** com **Pyxel** como projeto acadêmico por **Antonio Ollé Ramos** e **Leandro da Rocha Jorge**.

O projeto permite desenhar circuitos, acompanhar o avanço das gerações e controlar a velocidade da simulação. É um exemplo prático de **matrizes, regras locais de transição de estados, vizinhança de Moore, cópia de estruturas de dados e interface interativa**.

## 🧠 Como funciona

Cada célula da grade pode assumir um dos quatro estados:

| Estado | Cor no simulador | Comportamento |
| --- | --- | --- |
| Vazio | Preto | Continua vazio |
| Condutor | Amarelo | Vira cabeça de elétron quando há **1 ou 2** cabeças nas 8 células vizinhas |
| Cabeça de elétron | Azul-claro | Vira cauda de elétron |
| Cauda de elétron | Vermelho | Volta a ser condutor |

A geração seguinte é calculada a partir do estado anterior da grade, de modo que as alterações de uma célula não interferem no cálculo das demais durante a mesma etapa.

## ▶️ Executar localmente

Pré-requisitos: **Python 3** e `pip`.

1. Baixe ou clone o repositório.
2. Abra o terminal na pasta do projeto.
3. Instale a biblioteca gráfica:

   ```bash
   python -m pip install -r requirements.txt
   ```

4. Execute o simulador:

   ```bash
   python wireworld.py
   ```

No Windows, caso o comando `python` não funcione, experimente `py -m pip install -r requirements.txt` e `py wireworld.py`.

A janela inicia com uma **grade vazia de 80 × 60 células**. Para ver a propagação, desenhe um caminho de condutores, escolha a ferramenta *Cabeça* (tecla `2`), clique em uma das células do caminho e pressione **Espaço** para iniciar.

## 🎮 Controles

| Tecla / mouse | Ação |
| --- | --- |
| `Espaço` | Iniciar / pausar |
| `N` | Avançar uma geração (enquanto pausado) |
| `R` | Limpar a grade e zerar o contador |
| `1` | Pincel condutor |
| `2` | Pincel cabeça de elétron |
| `3` | Pincel cauda de elétron |
| `0` | Pincel vazio |
| Botão esquerdo | Desenhar na grade |
| Botão direito | Apagar célula |
| `←` / `→` | Ajustar o intervalo entre gerações (esquerda acelera, direita desacelera) |
| `Q` | Sair |

## 🗂️ Estrutura

```text
wireworld-automato-celular/
├── wireworld.py          # Implementação original do simulador
├── tests/
│   └── test_wireworld.py # Testes da lógica de transição
├── requirements.txt      # Dependência gráfica
├── .gitignore
└── README.md
```

## ✅ Testar a lógica

Os testes usam a biblioteca padrão `unittest` e isolam a dependência gráfica. Para rodar:

```bash
python -m unittest discover -s tests -v
```

## 📌 Observações

- A aplicação é executada **localmente** em uma janela Pyxel; não é um site web.
- Os circuitos são desenhados pelo usuário e não são salvos automaticamente entre execuções.
- Este repositório não contém senhas, chaves de API ou dados de terceiros.

## 👥 Autoria

Projeto acadêmico desenvolvido por **Antonio Ollé Ramos** e **Leandro da Rocha Jorge**. A publicação e o uso do código devem respeitar a participação de ambos os autores.
