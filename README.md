# 🤖 Simulador de Drone "Siga-me" com IA e OpenCV


Este projeto é um simulador de drone autônomo "Siga-me" desenvolvido em Python. Ele utiliza um modelo de IA pré-treinado para detectar objetos em tempo real e, após a seleção de um alvo pelo usuário, emprega um rastreador de alta performance do OpenCV para seguir o objeto, gerando comandos de controle direcionais e de distância.

## ✨ Principais Funcionalidades

-   **Detecção Automática com IA:** Usa o modelo MobileNet SSD com TensorFlow para localizar e classificar objetos comuns em um feed de vídeo ao vivo.
-   **Seleção de Alvo por Clique:** Uma interface interativa permite que o usuário simplesmente clique no objeto detectado que deseja seguir.
-   **Rastreamento Robusto:** Após a seleção, o rastreador CSRT do OpenCV assume o acompanhamento quadro a quadro, garantindo velocidade e eficiência.
-   **Correção de "Drift":** O sistema reavalia e corrige a posição do rastreador a cada segundo usando o detector de IA, prevenindo a perda do alvo.
-   **Controle Proporcional:** Gera comandos de "velocidade" variáveis para um controle de movimento mais suave e realista, simulando um drone real.

## 🛠️ Tecnologias Utilizadas

-   **Python 3**
-   **OpenCV (`opencv-contrib-python`)**
-   **TensorFlow**

## 🚀 Como Executar

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/LuizFellipiFreire25/Drone-Follow-Me-OpenCV]
    ```

2.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Execute o script:**
    ```bash
    python main.py
    ```

## 🎥 Vídeo de Demonstração

