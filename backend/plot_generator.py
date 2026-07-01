import os
import pandas as pd
import matplotlib.pyplot as plt


def generate_scatter_plot(file_path, x_column, y_column):

    df = pd.read_csv(file_path)

    os.makedirs("plots", exist_ok=True)

    plt.figure(figsize=(6, 3))
    plt.scatter(df[x_column], df[y_column])

    plt.xlabel(x_column)
    plt.ylabel(y_column)
    plt.title(f"{x_column} vs {y_column}")

    plot_path = f"plots/{x_column}_vs_{y_column}.png"

    plt.savefig(plot_path)
    plt.close()

    return plot_path