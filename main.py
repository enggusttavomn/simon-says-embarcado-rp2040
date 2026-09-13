from machine import PWM, Pin, SoftI2C, ADC
import time
import random
from ssd1306 import SSD1306_I2C
import math
import neopixel

## Configuração do display OLED via I2C
i2c = SoftI2C(scl=Pin(3), sda=Pin(2))
oled = SSD1306_I2C(128, 64, i2c)

## Botão do joystick
joystick_button = Pin(22, Pin.IN, Pin.PULL_UP)
## Joystick eixo X (ADC)
adc_vrx = ADC(Pin(26))  # Eixo X
## Joystick eixo Y (ADC)
adc_vry = ADC(Pin(27))  # Eixo Y

## Botão A
button_a = Pin(5, Pin.IN, Pin.PULL_UP)
## Botão B
button_b = Pin(6, Pin.IN, Pin.PULL_UP)

## Buzzer conectado ao pino 21
buzzer = PWM(Pin(21))
buzzer.freq(1000)
buzzer.duty_u16(0)

## Lista de comandos válidos no jogo
COMMANDS = ['UP', 'RIGHT', 'DOWN', 'LEFT', 'A', 'B']

## Símbolos exibidos no OLED para cada comando
COMMAND_SYMBOLS = {
    'UP': 'Cima',
    'RIGHT': 'Direita',
    'DOWN': 'Baixo',
    'LEFT': 'Esquerda',
    'A': 'Botao A',
    'B': 'Botao B'
}

## Sons (frequências Hz) associados a cada comando
COMMAND_SOUNDS = {
    'UP': 880,
    'RIGHT': 660,
    'DOWN': 440,
    'LEFT': 330,
    'A': 523,
    'B': 784
}

## Mapeamento da matriz 5x5 de LEDs (NeoPixel)
LED_MATRIX = [
    [24, 23, 22, 21, 20],
    [15, 16, 17, 18, 19],
    [14, 13, 12, 11, 10],
    [5, 6, 7, 8, 9],
    [4, 3, 2, 1, 0]
]

## Definição das cores RGB (intensidade até 255)
RED = (50, 0, 0)
GREEN = (0, 50, 0)
BLUE = (0, 0, 50)
YELLOW = (30, 30, 0)
MAGENTA = (30, 0, 30)
CYAN = (0, 30, 30)
WHITE = (25, 25, 25)
BLACK = (0, 0, 0)


class Lights:
    """
    @class Lights
    @brief Controla a matriz de LEDs NeoPixel e o LED RGB.

    Esta classe gerencia efeitos visuais e sonoros sincronizados,
    incluindo padrões de luz, animações e sons no buzzer.
    """
    
    def __init__(self):
        """
        @brief Inicializa o controlador de LEDs RGB e a matriz NeoPixel.
        """
        self.led_r = PWM(Pin(12))
        self.led_g = PWM(Pin(13))
        self.led_b = PWM(Pin(11))

        self.led_r.freq(1000)
        self.led_g.freq(1000)
        self.led_b.freq(1000)
        
        ## Número de LEDs na matriz 5x5
        NUM_LEDS = 25
        
        ## Inicializar a matriz de NeoPixels no GPIO7
        self.np = neopixel.NeoPixel(Pin(7), NUM_LEDS)
    
    def welcome(self):
        """
        @brief Executa a animação de boas-vindas com LEDs e sons.
        """
        self.clear_all()
        
        ## Chamar a função
        self.gradual_light_sound()

        ## Sequência de LEDs para simular o pulso cardíaco
        sequence = [14, 6, 12, 17, 21, 10]

        ## Especifica o número de repetições desejado
        num_repetitions = 2
        for _ in range(num_repetitions):
            self.heartbeat_effect(sequence)
            ## Exibe o coração grande
            self.heart()
            time.sleep(0.2)

        self.l3_37_sound_and_lights()
        time.sleep(1.5)
    
    def random_color(self, dim_factor=1):
        """
        @brief Gera uma cor RGB aleatória.

        @param dim_factor Fator de atenuação (0-1).
        @return Tupla (R, G, B) com valores entre 0 e 255.
        """
        return (int(random.randint(0, 255) * dim_factor), 
                int(random.randint(0, 255) * dim_factor), 
                int(random.randint(0, 255) * dim_factor))

    def door_swish(self):
        """
        @brief Efeito sonoro de "porta deslizando" no buzzer.
        """
        for freq in range(1000, 2000, 50):
            buzzer.freq(freq)
            buzzer.duty_u16(40000)
            time.sleep(0.005)
        for freq in range(2000, 1000, -50):
            buzzer.freq(freq)
            buzzer.duty_u16(40000)
            time.sleep(0.005)
        buzzer.duty_u16(0)
    
    def l3_37_sound_and_lights(self):
        """
        @brief Animação com LEDs em formato de coração e sons musicais.
        """
        border_heart_leds = [2, 6, 14, 15, 23, 17, 21, 19, 10, 8]
        inner_heart_leds = [7, 13, 12, 11, 16, 18]
        already_illuminated = []

        for freq in [440, 392, 440, 392]:  # Notas: A, G
            random_led = random.choice([led for led in border_heart_leds + inner_heart_leds if led not in already_illuminated])
            already_illuminated.append(random_led)
            color_intensity = 0.5 if random_led in inner_heart_leds else 1  
            self.np[random_led] = self.random_color(color_intensity)
            self.np.write()
            buzzer.freq(freq)
            buzzer.duty_u16(5000)
            time.sleep(0.1)

        for freq in [587, 493, 587, 523]:  # Notas: D, B, D, C
            random_led = random.choice([led for led in border_heart_leds + inner_heart_leds if led not in already_illuminated])
            already_illuminated.append(random_led)
            color_intensity = 0.5 if random_led in inner_heart_leds else 1  
            self.np[random_led] = self.random_color(color_intensity)
            self.np.write()
            buzzer.freq(freq)
            buzzer.duty_u16(5000)
            time.sleep(0.10)

        for led in [l for l in border_heart_leds + inner_heart_leds if l not in already_illuminated]:
            color_intensity = 0.5 if led in inner_heart_leds else 1 
            self.np[led] = self.random_color(color_intensity)
            self.np.write()
            time.sleep(0.1)

            buzzer.duty_u16(0)

    def smile_face(self):
        """
        @brief Desenha um rosto sorridente na matriz de LEDs.
        """
        colors = [
            BLACK, BLUE, BLUE, BLUE, BLACK,
            BLUE, BLACK, BLACK, BLACK, BLUE,
            BLACK, BLACK, BLACK, BLACK, BLACK,
            BLACK, CYAN, BLACK, CYAN, BLACK,
            BLACK, BLACK, BLACK, BLACK, BLACK
        ]
        
        # Atribuindo as cores à matriz np
        for i, color in enumerate(colors):
            self.np[i] = color
        
        self.np.write()
        
    def blink_right_eye(self):
        """
        @brief Pisca o olho direito da carinha azul.
        """
        self.np[0] = BLACK
        self.np[1] = BLUE
        self.np[2] = BLUE
        self.np[3] = BLUE
        self.np[4] = BLACK
        self.np[5] = BLUE
        self.np[6] = BLACK
        self.np[7] = BLACK
        self.np[8] = BLACK
        self.np[9] = BLUE
        self.np[10] = BLACK
        self.np[11] = BLACK
        self.np[12] = BLACK
        self.np[13] = BLACK
        self.np[14] = BLACK
        self.np[15] = BLACK
        self.np[16] = CYAN
        self.np[17] = BLACK
        self.np[18] = BLACK
        self.np[19] = BLACK
        self.np[20] = BLACK
        self.np[21] = BLACK
        self.np[22] = BLACK
        self.np[23] = BLACK
        self.np[24] = BLACK

        self.np.write()
        door_swish()

        # aguardar e retorna a cor azul do olho direito
        time.sleep(.2)
        self.np[18] = CYAN
        self.np.write()
        
    def colour_mouth(self):
        """
        @brief Sincroniza cores da boca com efeitos sonoros.
        """
        def r2d2_beep(self):
            """
            @brief Efeito sonoro inspirado em R2-D2 com LEDs piscando.
            """
            buzzer.freq(4000)
            buzzer.duty_u16(30000)
            time.sleep(0.1)
            buzzer.duty_u16(0)
            self.np[2] = RED
            self.np.write()
            time.sleep(0.2)
        
            # Segundo bipe
            buzzer.freq(5000)
            buzzer.duty_u16(30000)
            time.sleep(0.15)
            buzzer.duty_u16(0)
            self.np[2] = CYAN
            self.np[3] = CYAN
            self.np[1] = CYAN
            self.np.write()
            time.sleep(0.2)
        
            # Terceiro bipe
            buzzer.freq(4500)
            buzzer.duty_u16(30000)
            time.sleep(0.12)
            buzzer.duty_u16(0)
            self.np[2] = RED
            self.np[3] = RED
            self.np[1] = RED
            self.np.write()
            time.sleep(0.2)


        r2d2_beep()

        self.np[2] = BLUE
        self.np[3] = BLUE
        self.np[1] = BLUE
        self.np.write()
        
    def dim_leds(self, led_sequence, current_index):
        """
        @brief Reduz a intensidade dos LEDs já acesos em uma sequência.
        @param led_sequence Lista de LEDs.
        @param current_index Índice atual do LED.
        """
        dim_factor = 255 // (len(led_sequence) - current_index)
        for idx, led in enumerate(led_sequence):
            if idx < current_index:
                r, g, b = self.np[led]
                r = max(r - dim_factor, 0)
                self.np[led] = (r, g, b)

    def clear_all(self):
        """
        @brief Apaga todos os LEDs da matriz.
        """
        for i in range(len(self.np)):
            self.np[i] = BLACK
        self.np.write()
        
    def gradual_light_sound(self, duration=2):
        """
        @brief Animação gradual de luz e som.
        @param duration Duração em segundos.
        """
        step_duration = duration / 100
        for i in range(101):
            duty_cycle = (i * 65535) // 200  # Calcular o ciclo de trabalho atual

            # Ajustar o LED para a intensidade atual
            self.led_r.duty_u16(duty_cycle)
            self.led_g.duty_u16(duty_cycle)
            self.led_b.duty_u16(duty_cycle)

            # Ajustar a frequência do buzzer
            buzzer.freq(50 + i * 2)  # Ajustar a frequência do buzzer
            
            # Ajustar o volume do buzzer
            buzzer.duty_u16(duty_cycle // 4)  # Reduzir o volume para 25% do máximo
            
            time.sleep(step_duration)

        # Desligar o LED e o buzzer no final
        self.led_r.duty_u16(0)
        self.led_g.duty_u16(0)
        self.led_b.duty_u16(0)
        buzzer.duty_u16(0)
        
    def beep(self, freq=1000, duration=0.2):
        """
        @brief Toca um beep no buzzer.
        @param freq Frequência em Hz.
        @param duration Duração em segundos.
        """
        buzzer.freq(freq)
        buzzer.duty_u16(5000)  # Intensidade média
        time.sleep(duration)
        buzzer.duty_u16(0)  # Desliga o buzzer
        
    def heartbeat_effect(self, sequence):
        """
        @brief Anima LEDs simulando batimento cardíaco.
        @param sequence Lista de LEDs a acender.
        """
        initial_delay = 0.3  # tempo inicial entre LEDs
        decrement = 0.05  # valor a ser decrementado a cada LED
        
        # Limpa todos os LEDs
        self.clear_all()

        for idx, led in enumerate(sequence):
            self.np[led] = (255, 0, 0)  # Acende o LED vermelho
            self.dim_leds(sequence, idx)  # Diminui o brilho dos LEDs na sequência
            self.np.write()
            time.sleep(initial_delay - idx * decrement)
            
        # Toca o beep no buzzer
        self.beep()
        
        # Aguarda um pouco e depois desliga todos os LEDs
        time.sleep(0.3)
        self.clear_all()

    def heart(self):
        """
        @brief Acende LEDs formando um coração.
        """
        # Primeiro, desligamos todos os LEDs para garantir que começa "limpo"
        self.clear_all()
        
        # Lista dos LEDs que devem ser acesos para o coração
        heart_leds = [2, 6, 14, 15, 23, 17, 21, 19, 10, 8]
        
        # Acendendo os LEDs em vermelho
        for led in heart_leds:
            self.np[led] = (255, 0, 0)  # RED
        
        self.np.write()

class SimonGame:
    """
    @class SimonGame
    @brief Implementa o jogo Simon Says.

    Controla a lógica do jogo, exibição de comandos,
    entrada do jogador e progressão de níveis.
    """
    
    def __init__(self, lights=None):
        """
        @brief Inicializa o jogo.
        @param lights Instância da classe Lights.
        """
        self.sequence = []
        self.level = 1
        self.score = 0
        self.game_active = False
        self.player_turn = False
        self.lights = lights
        self.clear_display()
        self.show_welcome()
        
    def clear_display(self):
        """
        @brief Limpa o display OLED.
        """
        oled.fill(0)
        oled.show()
        
    def show_welcome(self):
        """
        @brief Exibe a tela inicial no OLED.
        """
        self.clear_display()
        
        oled.text("Simon Says", 30, 10)
        oled.text("Pressione A", 20, 30)
        oled.text("para comecar", 20, 40)
        oled.show()
        
    def show_command(self, command):
        """
        @brief Exibe um comando no OLED e LEDs.
        @param command Comando a ser exibido.
        """
        self.clear_display()
        
        # Show command on RGB LEDs if available
        if self.lights:
            # Clear all NeoPixel LEDs first
            self.lights.clear_all()
            
            if command in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
                # Show directional arrows on RGB LEDs
                self.show_direction_arrow(command)
            else:
                # For A and B buttons, show a different pattern
                self.show_button_pattern(command)
        
        # Keep the OLED clear or show minimal info
        oled.text("Comando:", 30, 20)
        oled.text(command, 50, 40)
        oled.show()
    
    def show_direction_arrow(self, direction):
        """
        @brief Mostra uma seta no LED RGB.
        @param direction Direção (UP/DOWN/LEFT/RIGHT).
        """
        if not self.lights:
            return
            
        # Define arrow patterns for each direction using the 5x5 LED matrix
        arrow_patterns = {
            'UP': [2, 7, 12, 17, 22, 16, 18],  # Upward arrow
            'DOWN': [2, 7, 12, 17, 22, 6, 8 ],  # Downward arrow
            'LEFT': [10, 11, 12, 13, 14, 16, 6],    # Leftward arrow
            'RIGHT': [10, 11, 12, 13, 14, 18, 8]    # Rightward arrow
        }
        
        # Get the pattern for this direction
        pattern = arrow_patterns.get(direction, [])
        
        # Light up the LEDs in green
        for led_index in pattern:
            if 0 <= led_index < 25:  # Ensure valid LED index
                self.lights.np[led_index] = (0, 8, 0)  # Very dim green
        
        # Update the display
        self.lights.np.write()
    
    def show_button_pattern(self, button):
        """
        @brief Mostra um padrão nos LEDs para botões A ou B.
        @param button 'A' ou 'B'.
        """
        if not self.lights:
            return
            
        if button == 'A':
            # Show a pattern for button A (e.g., center cross)
            center_pattern = [1,3,6,8,11,12,13,16,18,21,22,23]
            for led_index in center_pattern:
                if 0 <= led_index < 25:
                    self.lights.np[led_index] = (8, 0, 0)  # Very dim red
        elif button == 'B':
            # Show a different pattern for button B (e.g., corners)
            corner_pattern = [1,2,3,6,8,11,12,13,16,18,21,22,23]
            for led_index in corner_pattern:
                if 0 <= led_index < 25:
                    self.lights.np[led_index] = (0, 0, 8)  # Very dim blue
        
        # Update the display
        self.lights.np.write()
        
    def play_sound(self, freq, duration=0.2):
        """
        @brief Reproduz um som no buzzer.
        @param freq Frequência em Hz.
        @param duration Duração em segundos.
        """
        buzzer.freq(freq)
        buzzer.duty_u16(32768)
        time.sleep(duration)
        buzzer.duty_u16(0)
        
    def play_sequence(self):
        """
        @brief Mostra a sequência gerada pelo jogo.
        """
        self.player_turn = False
        self.clear_display()
        oled.text("Observe a", 35, 20)
        oled.text("sequencia!", 30, 30)
        oled.show()
        time.sleep(1)
        
        for cmd in self.sequence:
            self.show_command(cmd)
            self.play_sound(COMMAND_SOUNDS[cmd])
            time.sleep(0.8)  # Tempo para visualizar o comando
            self.clear_display()
            time.sleep(0.2)  # Pequena pausa entre comandos
            
        self.player_turn = True
        self.clear_display()
        oled.text("Sua vez!", 40, 30)
        oled.show()
        
        if self.lights:
            self.lights.clear_all()
            highlight_leds = [0,1,2,3,4,5,9,10,14,15,19,20,21,22,23,24]
            for led in highlight_leds:
                self.lights.np[led] = (0, 50, 0)  # Verde
            self.lights.np.write()
            time.sleep(0.2)
            self.lights.clear_all()
            highlight_leds = [6, 7, 8, 11, 13, 16, 17, 18]
            for led in highlight_leds:
                self.lights.np[led] = (0, 50, 0)  # Verde
            self.lights.np.write()
            time.sleep(0.2)
            self.lights.clear_all()
            highlight_leds = [12]
            for led in highlight_leds:
                self.lights.np[led] = (0, 50, 0)  # Verde
            self.lights.np.write()
            time.sleep(0.2)
            self.lights.clear_all()
        
    def generate_sequence(self, length):
        """
        @brief Gera uma nova sequência de comandos aleatórios.
        
        @param length Comprimento da sequência (int).
        @details Substitui a sequência atual por uma nova lista
        de comandos escolhidos aleatoriamente da lista COMMANDS.
        """
        self.sequence = []
        for _ in range(length):
            self.sequence.append(random.choice(COMMANDS))
            
    def get_player_input(self):
        """
        @brief Lê a entrada do jogador.
        @return Comando inserido ou None.
        """
        if not button_a.value():
            time.sleep(0.2)  # Debounce
            return 'A'
        if not button_b.value():
            time.sleep(0.2)  # Debounce
            return 'B'
        if not joystick_button.value():
            time.sleep(0.2)  # Debounce
            return 'J' 
            
        # Verificar joystick
        x_val = adc_vrx.read_u16()
        y_val = adc_vry.read_u16()
        
        if x_val < 10000:  # UP
            time.sleep(0.2)
            return 'UP'
        elif x_val > 55000:  # DOWN
            time.sleep(0.2)
            return 'DOWN'
        elif y_val < 10000:  # RIGHT
            time.sleep(0.2)
            return 'RIGHT'
        elif y_val > 55000:  # LEFT
            time.sleep(0.2)
            return 'LEFT'
            
        return None
        
    def check_input(self, expected):
        """
        @brief Verifica se a entrada do jogador corresponde ao esperado.
        
        @param expected Comando esperado (string: 'UP', 'DOWN', 'LEFT', 'RIGHT', 'A' ou 'B').
        @return True se o jogador acertou dentro do tempo limite, False caso contrário.
        
        @details O tempo limite é de 3 segundos. Enquanto isso,
        o método aguarda entrada válida do joystick ou botões.
        """
        start_time = time.ticks_ms()
        while time.ticks_diff(time.ticks_ms(), start_time) < 3000:
            player_input = self.get_player_input()
            if player_input is not None:
                self.show_command(player_input)
                self.play_sound(COMMAND_SOUNDS[player_input], 0.1)
                
                if player_input == expected:
                    return True
                else:
                    return False
            time.sleep(0.01)
        return False
        
    def level_up(self):
        """
        @brief Avança para a próxima rodada, adicionando um comando.
        """
        self.level += 1
        self.score += len(self.sequence) * 10
        self.clear_display()
        oled.text("Acertou!", 40, 10)
        oled.text("Nivel: " + str(self.level), 20, 30)
        oled.text("Pontos: " + str(self.score), 20, 50)
        oled.show()
        self.play_success_sound()
        time.sleep(1.5)
        
    def play_success_sound(self):
        """
        @brief Toca o som de sucesso (acerto).
        
        Reproduz uma sequência curta de notas ascendentes 
        (C5, E5, G5) indicando que o jogador acertou.
        """
        for freq in [523, 659, 784]:  # Notas: C5, E5, G5
            self.play_sound(freq, 0.1)
            
    def play_fail_sound(self):
        """
        @brief Toca o som de falha (erro).
        
        Reproduz uma sequência curta de notas descendentes 
        (G4, E4, C4) indicando que o jogador errou.
        """
        for freq in [392, 330, 262]:  # Notas: G4, E4, C4
            self.play_sound(freq, 0.15)
            
    def game_over(self):
        """
        @brief Encera o jogo e exibe pontuação final.
        """
        self.play_fail_sound()
        self.clear_display()
        oled.text("Game Over!", 30, 10)
        oled.text("Nivel: " + str(self.level), 30, 30)
        oled.text("Pontos: " + str(self.score), 25, 50)
        oled.show()
        time.sleep(2.5)
        
    def start_game(self):
        """
        @brief Inicia uma nova partida.
        """
        self.game_active = True
        self.level = 1
        self.score = 0
        sequence_length = 2  # Começa com sequências mais curtas
        
        # Clear LEDs when starting a new game
        if self.lights:
            self.lights.clear_all()
        
        while self.game_active:
            self.generate_sequence(sequence_length)
            self.play_sequence()
            
            correct = True
            for expected in self.sequence:
                if not self.check_input(expected):
                    correct = False
                    break
                    
            if correct:
                self.level_up()
                sequence_length = min(2 + self.level, 8)  # Limite de 8 comandos
            else:
                self.game_over()
                self.game_active = False
                
        # Clear LEDs before showing welcome screen
        if self.lights:
            self.lights.clear_all()
        self.show_welcome()
        
    def run(self):
        """
        @brief Loop principal do jogo.
        """
        while True:
            # Esperar por entrada para começar
            while self.get_player_input() is not "A":
                time.sleep(0.1)
                
            self.start_game()

## Instância principal do jogo e controlador de LEDs
if __name__ == "__main__":
    lights = Lights()
    lights.welcome()
    lights.clear_all()
    game = SimonGame(lights)
    game.run()
