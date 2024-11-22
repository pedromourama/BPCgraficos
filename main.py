import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import warnings
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

warnings.filterwarnings('ignore')

sns.set(style="whitegrid")

def carregar_dados(caminho_arquivo):
    dados = pd.read_csv(caminho_arquivo, encoding='latin1')
    dados['Referência'] = pd.to_datetime(dados['Referência'], format='%m/%Y') + pd.offsets.MonthBegin(0)
    dados['Valor Repassado a PCDs pelo BPC'] = dados['Valor Repassado a PCDs pelo BPC'].str.replace(',', '').astype(float)
    dados['Valor Repassado a Idosos pelo BPC'] = dados['Valor Repassado a Idosos pelo BPC'].str.replace(',', '').astype(float)
    dados['Valor Total repassado ao BPC'] = dados['Valor Total repassado ao BPC'].str.replace(',', '').astype(float)
    return dados

def gerar_graficos(dados, tipo_grafico):
    if tipo_grafico == "PCDs vs Idosos":
        plt.figure(figsize=(14, 7))
        sns.lineplot(data=dados, x='Referência', y='Pessoas com Deficiência (PCD) beneficiárias do BPC', label='PCDs', marker='o')
        sns.lineplot(data=dados, x='Referência', y='Idosos beneficiários do BPC', label='Idosos', marker='o')
        plt.title('Comparação de Beneficiários do BPC (PCDs x Idosos)')
        plt.xlabel('Ano')
        plt.ylabel('Número de Beneficiários')
        plt.grid(True)
        plt.legend()
        plt.show()
    elif tipo_grafico == "Valor Total":
        plt.figure(figsize=(14, 7))
        sns.lineplot(data=dados, x='Referência', y='Valor Total repassado ao BPC', color='green', label='Valor Total', marker='o')
        plt.title('Evolução do Valor Total Repassado pelo BPC')
        plt.xlabel('Ano')
        plt.ylabel('Valor Total Repassado (R$)')
        plt.grid(True)
        plt.legend()
        plt.show()
    elif tipo_grafico == "Valores Repassados":
        plt.figure(figsize=(14, 7))
        sns.lineplot(data=dados, x='Referência', y='Valor Repassado a PCDs pelo BPC', label='PCDs', marker='o')
        sns.lineplot(data=dados, x='Referência', y='Valor Repassado a Idosos pelo BPC', label='Idosos', marker='o')
        plt.title('Comparação de Valores Repassados (PCDs x Idosos)')
        plt.xlabel('Ano')
        plt.ylabel('Valor Repassado (R$)')
        plt.grid(True)
        plt.legend()
        plt.show()
    elif tipo_grafico == "Previsão de Valores":
        plt.figure(figsize=(14, 7))
        dados.set_index('Referência', inplace=True)
        modelo = ExponentialSmoothing(dados['Valor Total repassado ao BPC'], trend='add', seasonal='add', seasonal_periods=12).fit()
        previsao = modelo.forecast(60)  # 60 meses para 5 anos
        dados['Valor Total repassado ao BPC'].plot(label='Valor Total')
        previsao.plot(label='Previsão')
        plt.title('Previsão de Valores Repassados ao BPC')
        plt.xlabel('Ano')
        plt.ylabel('Valor Total Repassado (R$)')
        plt.grid(True)
        plt.legend()
        plt.show()
    elif tipo_grafico == "Histograma":
        plt.figure(figsize=(14, 7))
        sns.histplot(dados['Valor Total repassado ao BPC'], bins=30, kde=True, color='blue')
        plt.title('Distribuição do Valor Total Repassado ao BPC')
        plt.xlabel('Valor Total Repassado Em Milhões (R$)')
        plt.ylabel('Frequência')
        plt.grid(True)
        plt.show()
    elif tipo_grafico == "Boxplot":
        plt.figure(figsize=(14, 7))
        sns.boxplot(data=dados[['Valor Repassado a PCDs pelo BPC', 'Valor Repassado a Idosos pelo BPC']])
        plt.title('Distribuição dos Valores Repassados (PCDs x Idosos)')
        plt.xlabel('Categoria')
        plt.ylabel('Valor Repassado (R$)')
        plt.grid(True)
        plt.show()
    elif tipo_grafico == "Scatter Plot":
        plt.figure(figsize=(14, 7))
        sns.scatterplot(data=dados, x='Pessoas com Deficiência (PCD) beneficiárias do BPC', y='Valor Repassado a PCDs pelo BPC', color='purple', label='PCDs')
        sns.scatterplot(data=dados, x='Idosos beneficiários do BPC', y='Valor Repassado a Idosos pelo BPC', color='orange', label='Idosos')
        plt.title('Relação entre Beneficiários e Valores Repassados (PCDs x Idosos)')
        plt.xlabel('Número de Beneficiários')
        plt.ylabel('Valor Repassado (R$)')
        plt.grid(True)
        plt.legend()
        plt.show()

def abrir_arquivo():
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if caminho_arquivo:
        try:
            dados = carregar_dados(caminho_arquivo)
            label_arquivo['text'] = f"Arquivo Carregado: {caminho_arquivo.split('/')[-1]}"
            return dados
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível carregar o arquivo: {e}")
            return None

def selecionar_grafico():
    dados = abrir_arquivo()
    if dados is not None:
        tipo_grafico = var_grafico.get()
        gerar_graficos(dados, tipo_grafico)

root = tk.Tk()
root.title("Análise de Dados do BPC")

style = ttk.Style()
style.configure("TFrame", background="#2e3f4f")
style.configure("TButton", background="#007acc", foreground="white", font=("Arial", 12))
style.configure("TLabel", background="#2e3f4f", foreground="white", font=("Arial", 10))
style.configure("TOptionMenu", background="#2e3f4f", foreground="white", font=("Arial", 12))

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

label_titulo = ttk.Label(frame, text="Selecione o Gráfico que Deseja Visualizar", font=("Arial", 16), background="#2e3f4f", foreground="white")
label_titulo.grid(row=0, column=0, columnspan=2, pady=10)

var_grafico = tk.StringVar(value="PCDs vs Idosos")
opcoes_grafico = ["PCDs vs Idosos", "Valor Total", "Valores Repassados", "Previsão de Valores", "Histograma", "Boxplot", "Scatter Plot"]

menu_grafico = ttk.OptionMenu(frame, var_grafico, *opcoes_grafico)
menu_grafico.grid(row=1, column=0, columnspan=2, pady=5)

botao_carregar = ttk.Button(frame, text="Carregar Dados e Visualizar Gráfico", command=selecionar_grafico)
botao_carregar.grid(row=2, column=0, columnspan=2, pady=20)

label_arquivo = ttk.Label(frame, text="Nenhum arquivo carregado", font=("Arial", 10), background="#2e3f4f", foreground="white")
label_arquivo.grid(row=3, column=0, columnspan=2, pady=5)

for child in frame.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()
