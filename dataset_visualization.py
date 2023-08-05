import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import argparse
import logging

# Configuração do logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def main(annotation_dir, output_dir):
    logging.info("PROCESSANDO INFORMAÇÕES...")

    CLASSES = ["Postes", "braco", "luminaria", "gerador", "placa"]
    CLASS_COUNT = {cls: 0 for cls in CLASSES}
    data = []

    # Iteração das anotações
    for annotation_file in os.listdir(annotation_dir):
        if annotation_file.endswith(".txt"):
            annotation_path = os.path.join(annotation_dir, annotation_file)

            with open(annotation_path, "r") as file:
                lines = file.readlines()
            for line in lines:
                class_id = int(line.split()[0])
                if class_id < len(CLASSES):
                    class_name = CLASSES[class_id]
                    CLASS_COUNT[class_name] += 1

                    # Lendo dimensões x1, y1, w, h
                    x_center, y_center, width, height = map(float, line.split()[1:])
                    x1 = x_center - width / 2
                    y1 = y_center - height / 2
                    data.append([annotation_file, class_name, x1, y1, width, height])
    logging.info("CRIANDO GRÁFICOS...")

    # Gráfico
    sns.set(style="whitegrid")
    plt.figure(figsize=(8, 4))
    sns.barplot(x=list(CLASS_COUNT.keys()), y=list(CLASS_COUNT.values()))
    plt.xlabel("Classes")
    plt.ylabel("Número de Anotações")
    plt.title("Número de Anotações por Classe (2D)")
    plt.xticks(rotation=45)
    plt.savefig(os.path.join(output_dir, "grafico_2d.png"))
    plt.close()
    logging.info("GRÁFICO 2D CRIADO")

    # Gráfico 3D
    fig = plt.figure(figsize=(8, 4))
    ax = fig.add_subplot(111, projection="3d")
    class_names = list(CLASS_COUNT.keys())
    y_pos = np.arange(len(class_names))
    count_values = list(CLASS_COUNT.values())
    ax.bar3d(y_pos, y_pos, np.zeros(len(class_names)), 0.5, 0.5, count_values)
    ax.set_xticks(y_pos)
    ax.set_xticklabels(class_names, rotation=45, color="blue")
    ax.set_xlabel("Classes", color="red")
    ax.set_ylabel("Classes", color="red")
    ax.set_zlabel("Número de Anotações", color="red")
    ax.set_title("Número de Anotações por Classe (3D)")
    plt.savefig(os.path.join(output_dir, "grafico_3d.png"))
    plt.close()
    logging.info("GRÁFICO 3D CRIADO")

    # Criação da planilha
    df = pd.DataFrame(
        data, columns=["Arquivo", "Classe", "X1", "Y1", "Largura", "Altura"]
    )
    excel_filename = os.path.join(output_dir, "DATA.xlsx")
    df.to_excel(excel_filename, index=False)
    logging.info("PLANILHA DE DADOS CRIADA!")
    logging.info(f"Dados das anotações exportados para {excel_filename}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Processa anotações de objetos em imagens."
    )
    parser.add_argument(
        "-r",
        "--annotation_dir",
        type=str,
        required=True,
        help="Caminho para o diretório com as anotações",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        default="output",
        help="Caminho para o diretório de saída",
    )

    args = parser.parse_args()
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
    main(args.annotation_dir, args.output_dir)
