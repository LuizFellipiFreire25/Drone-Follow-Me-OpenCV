# 🤖 Protótipo Físico de Sistema 'Siga-me' com IA e Arduino (v1.1)


Este projeto é um protótipo físico funcional de um sistema "Siga-me", que integra Visão Computacional de alto nível com controle de hardware de baixo nível. O sistema utiliza Python e OpenCV para análise de vídeo e se comunica via serial com um Arduino Uno para controlar atuadores físicos (um servo motor e LEDs) em tempo real.

## ✨ Funcionalidades

### Módulo de Software (Python)
-   **Detecção Automática com IA:** Usa o modelo MobileNet SSD com TensorFlow para localizar e classificar objetos em um feed de vídeo ao vivo.
-   **Seleção de Alvo por Clique:** Permite que o usuário simplesmente clique no objeto detectado que deseja seguir.
-   **Rastreamento Robusto:** Emprega o rastreador CSRT do OpenCV para um acompanhamento rápido e eficiente do alvo.
-   **Correção de "Drift":** O sistema usa a IA para corrigir periodicamente a posição do rastreador, prevenindo a perda do alvo.
-   **Controle Proporcional:** Calcula um sinal de "velocidade" (`vel`) baseado no erro de posição do alvo. Este sinal é então convertido em um ângulo preciso para o servo motor.
-   **Comunicação Serial:** Envia os comandos de ângulo e estado (distância) para o Arduino via porta serial.

### Módulo de Hardware (Arduino)
-   **Controle de Servo Proporcional:** Um servo motor replica o movimento horizontal do alvo de forma suave e proporcional ao sinal recebido do Python.
-   **Sinalização de Distância com LEDs:** Dois LEDs fornecem feedback visual sobre a distância relativa do alvo: um para "APROXIMAR" e outro para "AFASTAR".

## 🛠️ Tecnologias Utilizadas

| Software | Hardware |
| :--- | :--- |
| Python 3 | Arduino Uno |
| OpenCV (`opencv-contrib-python`) | Servo Motor SG90 |
| TensorFlow | LEDs |
| PySerial | Resistores 330Ω |

## 🔌 Montagem do Circuito

O hardware foi montado conforme o esquema abaixo:
-   **Servo Motor:** Sinal no pino `~9` (PWM), VCC em `5V`, GND em `GND`.
-   **LED Verde (Aproximar):** Conectado ao pino `7` através de um resistor de 220Ω.
-   **LED Vermelho (Afastar):** Conectado ao pino `8` através de um resistor de 220Ω.

## 🚀 Como Executar o Protótipo

Para replicar o projeto, siga os dois estágios abaixo:

### Estágio 1: Preparar o Arduino
1.  **Monte o circuito** conforme descrito acima.
2.  **Abra a Arduino IDE** e cole o código do arquivo `.ino` do projeto.
3.  **Verifique a Porta:** Em `Ferramentas > Porta`, certifique-se de que a porta correta para o seu Arduino está selecionada.
4.  **Faça o Upload:** Clique no botão de upload para enviar o firmware para a placa Arduino.

### Estágio 2: Executar o Script Python
1.  **Clone ou baixe** este repositório.
2.  **Instale as dependências:** Abra um terminal na pasta do projeto e execute:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configure a Porta Serial:** Abra o script Python (`main.py`) e altere a variável `port` na linha de configuração do `serial.Serial` para a mesma porta que você viu na Arduino IDE (ex: `'COM4'`).
4.  **Execute o Programa:**
    ```bash
    python main.py
    ```
    * O script irá se conectar ao Arduino, e o sistema estará pronto para uso!
