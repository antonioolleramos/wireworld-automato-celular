import pyxel

# --- Constantes dos Estados, Cores e Nomes ---
EMPTY = 0
CONDUCTOR = 1
ELECTRON_HEAD = 2
ELECTRON_TAIL = 3

# Dicionários para mapeamento e exibição
COLORS = {
    EMPTY: 0,           # Preto
    CONDUCTOR: 10,      # Amarelo
    ELECTRON_HEAD: 12,  # Ciano (Azul claro)
    ELECTRON_TAIL: 8,   # Vermelho
}
STATE_NAMES = {
    EMPTY: "Vazio",
    CONDUCTOR: "Condutor",
    ELECTRON_HEAD: "Cabeca",
    ELECTRON_TAIL: "Cauda"
}

# --- Configurações da Grade Inicial ---
GRID_WIDTH = 80
GRID_HEIGHT = 60


class Wireworld:
    def __init__(self, width, height, cell_size=10):
        self.grid_w = width
        self.grid_h = height
        self.cell_size = cell_size

        self.grid = [[EMPTY for _ in range(self.grid_w)] for _ in range(self.grid_h)]

        self.screen_w = self.grid_w * self.cell_size
        self.screen_h = (self.grid_h * self.cell_size) + 60

        # Controle da simulação
        self.is_paused = True
        self.generation = 0
        self.simulation_speed = 8
        self.frame_count = 0
        
        self.drawing_state = CONDUCTOR

        pyxel.init(self.screen_w, self.screen_h, title="Wireworld Interativo", fps=60)
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def deep_copy_grid(self, grid):
        return [row[:] for row in grid]

    def reset(self):
        self.grid = [[EMPTY for _ in range(self.grid_w)] for _ in range(self.grid_h)]
        self.generation = 0
        self.is_paused = True
        print("Grade limpa.")

    def step(self):
        next_grid = self.deep_copy_grid(self.grid)
        for y in range(self.grid_h):
            for x in range(self.grid_w):
                state = self.grid[y][x]
                if state == ELECTRON_HEAD:
                    next_grid[y][x] = ELECTRON_TAIL
                elif state == ELECTRON_TAIL:
                    next_grid[y][x] = CONDUCTOR
                elif state == CONDUCTOR:
                    head_neighbors = self.count_neighbor_heads(x, y)
                    if head_neighbors in [1, 2]:
                        next_grid[y][x] = ELECTRON_HEAD
        self.grid = next_grid
        self.generation += 1

    def count_neighbor_heads(self, x, y):
        count = 0
        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dx == 0 and dy == 0: continue
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.grid_w and 0 <= ny < self.grid_h:
                    if self.grid[ny][nx] == ELECTRON_HEAD:
                        count += 1
        return count

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q): pyxel.quit()
        if pyxel.btnp(pyxel.KEY_SPACE): self.is_paused = not self.is_paused
        if self.is_paused and pyxel.btnp(pyxel.KEY_N): self.step()
        if pyxel.btnp(pyxel.KEY_R): self.reset()
            
        if pyxel.btnp(pyxel.KEY_RIGHT): self.simulation_speed += 1
        if pyxel.btnp(pyxel.KEY_LEFT): self.simulation_speed = max(1, self.simulation_speed - 1)

        if pyxel.btnp(pyxel.KEY_1): self.drawing_state = CONDUCTOR
        if pyxel.btnp(pyxel.KEY_2): self.drawing_state = ELECTRON_HEAD
        if pyxel.btnp(pyxel.KEY_3): self.drawing_state = ELECTRON_TAIL
        if pyxel.btnp(pyxel.KEY_0): self.drawing_state = EMPTY

        if not self.is_paused:
            self.frame_count += 1
            if self.frame_count >= self.simulation_speed:
                self.frame_count = 0
                self.step()

        mouse_x = pyxel.mouse_x // self.cell_size
        mouse_y = pyxel.mouse_y // self.cell_size

        if 0 <= mouse_x < self.grid_w and 0 <= mouse_y < self.grid_h:
            if pyxel.btn(pyxel.MOUSE_BUTTON_LEFT):
                self.grid[mouse_y][mouse_x] = self.drawing_state
            if pyxel.btn(pyxel.MOUSE_BUTTON_RIGHT):
                self.grid[mouse_y][mouse_x] = EMPTY

    def draw(self):
        pyxel.cls(1) # Fundo Azul Escuro (Navy)

        for y in range(self.grid_h):
            for x in range(self.grid_w):
                color = COLORS[self.grid[y][x]]
                pyxel.rect(x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size, color)
        
    
        ui_y = self.grid_h * self.cell_size
        pyxel.rect(0, ui_y, self.screen_w, 60, 5)
        
        # Cores
        WHITE = 7
        LIGHT_GRAY = 6

        # --- Coluna 1: Status da Simulação ---
        pyxel.text(10, ui_y + 7, "--- SIMULACAO ---", LIGHT_GRAY)
        
        status_text = "PAUSADO" if self.is_paused else "RODANDO"
        status_color = 9 if self.is_paused else 11
        pyxel.text(10, ui_y + 19, "Status:", WHITE)
        pyxel.text(45, ui_y + 19, status_text, status_color)
        
        pyxel.text(10, ui_y + 29, f"Geracao: {self.generation}", WHITE)
        pyxel.text(10, ui_y + 39, f"Velocidade: {self.simulation_speed} (<-/->)", WHITE)

        # --- Coluna 2: Controles ---
        pyxel.text(200, ui_y + 7, "--- CONTROLES ---", LIGHT_GRAY)
        pyxel.text(200, ui_y + 19, "[ESPACO] : Play/Pause", WHITE)
        pyxel.text(200, ui_y + 29, "[N]        : Proximo Passo", WHITE)
        pyxel.text(200, ui_y + 39, "[R]        : Limpar Tudo", WHITE)

        # --- Coluna 3: Desenho ---
        pyxel.text(400, ui_y + 7, "--- DESENHO ---", LIGHT_GRAY)
        
        draw_tool_text = f": {STATE_NAMES[self.drawing_state]}"
        pyxel.text(400, ui_y + 19, "Pincel Atual", WHITE)
        pyxel.rect(465, ui_y + 17, 7, 7, COLORS[self.drawing_state])
        pyxel.text(475, ui_y + 19, draw_tool_text, WHITE)

        pyxel.text(400, ui_y + 29, "[TECLAS 0-3] : Seleciona Pincel", WHITE)
        pyxel.text(400, ui_y + 39, "[MOUSE ESQ]  : Desenha", WHITE)
        pyxel.text(400, ui_y + 49, "[MOUSE DIR]  : Apaga", WHITE)


if __name__ == "__main__":
    Wireworld(GRID_WIDTH, GRID_HEIGHT)


# Desenvolvido por Antonio Ollé Ramos e Leandro da Rocha Jorge
