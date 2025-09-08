import cv2
import sys

# --- MODOS DE OPERAÇÃO ---
MODO_DETECCAO = 0
MODO_RASTREAMENTO = 1
# -------------------------

# --- CONFIGURAÇÃO DO MODELO DE IA (DA AULA 13) ---
# Carrega as labels (nomes das classes)
with open("coco_class_labels.txt") as fp:
    labels = fp.read().split("\n")

# Caminhos para os arquivos do modelo TensorFlow
modelFile = "models/ssd_mobilenet_v2_coco_2018_03_29/frozen_inference_graph.pb"
configFile = "models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt"

# Carrega a rede neural na memória
net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)
# ---------------------------------------------------

# --- VARIÁVEIS GLOBAIS ---
# Inicia o programa no modo de detecção
modo_atual = MODO_DETECCAO
# Lista para guardar as caixas detectadas no frame atual
deteccoes_frame_atual = []
# -------------------------

# --- FUNÇÃO DE CALLBACK DO MOUSE ---


def selecionar_alvo_por_clique(event, x, y, flags, param):
    global modo_atual, deteccoes_frame_atual, frame, tracker, area_referencia, bbox

    # Se o evento for um clique do botão esquerdo
    if event == cv2.EVENT_LBUTTONDOWN:
        # Se estivermos no modo de detecção
        if modo_atual == MODO_DETECCAO:
            # Percorre todas as caixas detectadas no último frame
            for i, (caixa, label, conf) in enumerate(deteccoes_frame_atual):
                (x_caixa, y_caixa, w_caixa, h_caixa) = caixa
                # Verifica se o clique (x, y) está dentro da caixa atual
                if x >= x_caixa and x <= x_caixa + w_caixa and y >= y_caixa and y <= y_caixa + h_caixa:
                    print(f"Alvo selecionado: {label} [{i}]")
                    # Define a caixa selecionada como a bbox para o tracker
                    bbox = caixa
                    # Reinicia o tracker
                    tracker = cv2.TrackerCSRT_create()
                    tracker.init(frame, bbox)
                    # Define a área de referência para o controle de distância
                    area_referencia = bbox[2] * bbox[3]
                    # Muda para o modo de rastreamento
                    modo_atual = MODO_RASTREAMENTO
                    # Limpa a lista de detecções para não interferir
                    deteccoes_frame_atual = []
                    break  # Sai do loop assim que encontrar o alvo
# ------------------------------------


# --- CONFIGURAÇÃO INICIAL DO VÍDEO E JANELA ---
s = 0
if len(sys.argv) > 1:
    s = int(sys.argv[1])
video = cv2.VideoCapture(s)
if not video.isOpened():
    print("Erro ao abrir o vídeo")
    sys.exit()

# Cores e fontes
cor_sucesso = (0, 255, 0)
cor_falha = (0, 0, 255)
cor_info = (0, 255, 255)
cor_caixa_ia = (255, 178, 50)
fonte = cv2.FONT_HERSHEY_SIMPLEX

# Variáveis do tracker
tracker = cv2.TrackerCSRT_create()
area_referencia = 0
bbox = None

# Cria a janela e atribui a função de callback do mouse a ela
win_name = "Simulador Drone Siga-me com IA"
cv2.namedWindow(win_name)
cv2.setMouseCallback(win_name, selecionar_alvo_por_clique)
# ---------------------------------------------


# --- LOOP PRINCIPAL ---
while True:
    ok, frame = video.read()
    if not ok:
        break

    frame = cv2.flip(frame, 1)
    altura, largura, _ = frame.shape

    if modo_atual == MODO_RASTREAMENTO:
        ok, bbox = tracker.update(frame)

        if ok:
            # --- LÓGICA DE CONTROLE PROPORCIONAL (P-Controller) ---

            # --- 1. Controle de Posição (Esquerda/Direita) ---
            centro_frame_x = largura // 2
            centro_obj_x = int(bbox[0] + bbox[2] / 2)

            # Calcula o "erro" de posição. Negativo = objeto à esquerda, Positivo = objeto à direita
            erro_posicao = centro_obj_x - centro_frame_x

            # Define uma "velocidade" de movimento baseada no erro.
            # O valor Kp (ganho proporcional) determina o quão "agressiva" é a resposta.
            # Você pode ajustar este valor!
            Kp_posicao = 0.1
            velocidade_horizontal = Kp_posicao * erro_posicao

            # Gera o comando de texto baseado na velocidade calculada
            zona_morta = 30  # Usamos a zona morta para o comando "PARADO"
            if erro_posicao < -zona_morta:
                comando_posicao = f"MOVER ESQUERDA (Vel: {abs(velocidade_horizontal):.1f})"
            elif erro_posicao > zona_morta:
                comando_posicao = f"MOVER DIREITA (Vel: {velocidade_horizontal:.1f})"
            else:
                comando_posicao = "CENTRALIZADO"
                velocidade_horizontal = 0

            # --- 2. Controle de Distância (Frente/Trás) ---
            area_atual = bbox[2] * bbox[3]

            # Calcula o erro de área em relação à referência.
            # Positivo = objeto muito perto, Negativo = objeto muito longe
            erro_area = area_atual - area_referencia

            # Ganho proporcional para o controle de distância
            Kp_area = 0.001  # Este valor costuma ser bem menor
            # Negativo para inverter a ação (se perto, afasta)
            velocidade_profundidade = - (Kp_area * erro_area)

            # Gera o comando de texto
            threshold_area = 0.15  # 15% de margem
            if area_atual > area_referencia * (1 + threshold_area):
                comando_distancia = f"AFASTAR (Vel: {abs(velocidade_profundidade):.1f})"
            elif area_atual < area_referencia * (1 - threshold_area):
                comando_distancia = f"APROXIMAR (Vel: {velocidade_profundidade:.1f})"
            else:
                comando_distancia = "MANTER DISTANCIA"
                velocidade_profundidade = 0

            # --- FIM DO CONTROLE PROPORCIONAL ---

            # Para um drone real, você enviaria os valores `velocidade_horizontal` e `velocidade_profundidade`
            # via comunicação serial, em vez de apenas mostrar o texto.

            # Lógica de exibição (desenhar caixa e texto)
            p1, p2 = (int(bbox[0]), int(bbox[1])), (int(
                bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, cor_sucesso, 2, 1)

            comando_final = f"Pos: {comando_posicao} | Dist: {comando_distancia}"
            cv2.putText(frame, comando_final, (10, 30),
                        fonte, 0.6, cor_info, 2)

    elif modo_atual == MODO_DETECCAO:
        deteccoes_frame_atual = []  # Limpa a lista a cada frame
        # --- LÓGICA DE DETECÇÃO (ADAPTADA DA AULA 13) ---
        blob = cv2.dnn.blobFromImage(frame, 1.0, size=(
            300, 300), mean=(0, 0, 0), swapRB=True, crop=False)
        net.setInput(blob)
        detections = net.forward()

        # Itera sobre todas as detecções encontradas
        for i in range(detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            # Filtra detecções com baixa confiança
            if confidence > 0.5:
                class_id = int(detections[0, 0, i, 1])

                # Para simplificar, vamos focar em alguns objetos comuns.
                # Você pode remover ou alterar este 'if' para detectar tudo.
                objetos_alvo = ["person", "car",
                                "bottle", "cat", "dog", "cell phone"]
                if labels[class_id] in objetos_alvo:
                    # Calcula as coordenadas da caixa
                    x = int(detections[0, 0, i, 3] * largura)
                    y = int(detections[0, 0, i, 4] * altura)
                    w = int(detections[0, 0, i, 5] * largura) - x
                    h = int(detections[0, 0, i, 6] * altura) - y

                    caixa = (x, y, w, h)
                    label = labels[class_id]

                    # Guarda a detecção para a função de clique
                    deteccoes_frame_atual.append((caixa, label, confidence))

                    # Desenha a caixa e o texto na tela
                    cv2.rectangle(frame, (x, y), (x + w, y + h),
                                  cor_caixa_ia, 2)
                    texto = f"{label}: {confidence:.2f}"
                    cv2.putText(frame, texto, (x, y - 5),
                                fonte, 0.5, cor_caixa_ia, 2)

        cv2.putText(frame, "Clique em um objeto para seguir",
                    (10, 30), fonte, 0.75, cor_info, 2)

    # Exibe o resultado final na janela
    cv2.imshow(win_name, frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC para sair
        break

video.release()
cv2.destroyAllWindows()
