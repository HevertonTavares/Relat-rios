
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from fpdf import FPDF
from tempfile import NamedTemporaryFile

st.set_page_config(page_title="Gerador de Relatórios PDF", layout="centered")
st.title("Gerador de Relatórios PDF por Loja")

uploaded_file = st.file_uploader("Envie a planilha .xlsx", type=["xlsx"])
logo_path = "Appmax.png"

def format_currency(value):
    return f"R${value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def tratar_valor_percentual(valor):
    if pd.isna(valor):
        return 0.0
    if isinstance(valor, str):
        valor = valor.replace("%", "").strip().replace(",", ".")
        try:
            return float(valor) / 100 if float(valor) > 1 else float(valor)
        except:
            return 0.0
    try:
        return float(valor)
    except:
        return 0.0

def tratar_valor_numerico(valor):
    if pd.isna(valor):
        return 0
    if isinstance(valor, str):
        valor = valor.strip().replace("R$", "").replace(".", "").replace(",", ".")
    try:
        return int(float(valor))
    except:
        return 0

class RelatorioPDF(FPDF):
    def header(self):
        self.set_fill_color(155, 106, 250)
        self.rect(0, 0, 210, 297, 'F')
        self.set_text_color(255, 255, 255)

    def render(self, row, grafico_path, logo_path):
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", "B", 18)
        self.set_y(15)
        self.cell(0, 10, "Relatório de Resultados Mensal", ln=True, align="C")

        self.set_font("Arial", "", 12)
        self.cell(0, 8, f"{row['Loja'].upper()} - {row['Mês']}", ln=True, align="C")

        self.ln(6)
        self.set_font("Arial", "B", 14)
        self.cell(0, 9, "Taxas de Aprovação", ln=True, align="C")

        x = 25
        y = self.get_y() + 4
        w = 160
        h = 20
        self.set_draw_color(255, 255, 255)
        self.rect(x, y, w, h, style='D')
        self.line(x + w / 2, y, x + w / 2, y + h)

        self.set_xy(x, y + 3)
        self.set_font("Arial", "", 10)
        self.cell(w / 2, 5, "Cartão", align="C")
        self.cell(w / 2, 5, "Pix", align="C", ln=True)

        self.set_x(x)
        self.set_font("Arial", "B", 12)
        self.cell(w / 2, 8, f"{int(tratar_valor_percentual(row['Taxa Aprovação cartão']) * 100)}%", align="C")
        self.cell(w / 2, 8, f"{int(tratar_valor_percentual(row['Taxa Aprovação PIX']) * 100)}%", align="C", ln=True)

        self.ln(14)
        self.set_font("Arial", "B", 14)
        self.cell(0, 8, "Total de pedidos referente ao mês anterior", ln=True, align="C")
        self.set_font("Arial", "", 11)
        self.cell(0, 7, f"{tratar_valor_numerico(row['Número de vendas'])} pedidos", ln=True, align="C")
        self.cell(0, 6,
                  f"Cartão: {tratar_valor_numerico(row['Pedidos de Cartão'])}  |  PIX: {tratar_valor_numerico(row['Pedidos de PIX'])}  |  Boleto: {tratar_valor_numerico(row['Pedidos Boleto'])}",
                  ln=True, align="C")

        self.ln(8)
        self.set_font("Arial", "B", 14)
        self.cell(0, 8, f"Valor processado em 30 dias: {format_currency(tratar_valor_numerico(row['Processamento 30 dias']))}", ln=True, align="C")

        self.ln(8)
        self.image(grafico_path, x=60, w=90)

        self.ln(5)
        self.set_font("Arial", "B", 14)
        self.cell(0, 8, "Recuperação de vendas", ln=True, align="C")

        x = 15
        y = self.get_y() + 3
        col_w = 60
        row_h = 9
        headers = ["Carrinho Abandonado", "Recuperação Banco Emissor", "Custo envios disparos"]
        valores = [
            format_currency(tratar_valor_numerico(row['Recuperação de Carrinho'])),
            format_currency(tratar_valor_numerico(row['Recuperação Banco Emissor'])),
            format_currency(tratar_valor_numerico(row['Custo de envios']))
        ]

        self.set_draw_color(255, 255, 255)
        self.set_fill_color(155, 106, 250)
        self.set_text_color(255, 255, 255)

        self.set_font("Arial", "", 10)
        for i in range(3):
            self.set_xy(x + col_w * i, y)
            self.cell(col_w, row_h, headers[i], border=1, align="C")
        self.ln(row_h)

        self.set_font("Arial", "B", 12)
        for i in range(3):
            self.set_xy(x + col_w * i, y + row_h)
            self.cell(col_w, row_h, valores[i], border=1, align="C")

        self.image(logo_path, x=160, y=275, w=35)

if uploaded_file:
    df = pd.read_excel(uploaded_file)

    def gerar_grafico(row):
        valores = [
            tratar_valor_numerico(row['Pedidos de Cartão']),
            tratar_valor_numerico(row['Pedidos de PIX']),
            tratar_valor_numerico(row['Pedidos Boleto'])
        ]
        labels = ['Cartão', 'PIX', 'Boleto']
        cores = ['#FFCCFF', '#CCFFFF', '#3399FF']
        fig, ax = plt.subplots(figsize=(4, 4), facecolor='#9B6AFA')
        ax.pie(valores, labels=labels, colors=cores, autopct='%1.1f%%', startangle=90,
               textprops={'color': 'white'})
        ax.axis('equal')
        path = NamedTemporaryFile(delete=False, suffix=".png").name
        plt.savefig(path, dpi=300, bbox_inches='tight', facecolor='#9B6AFA')
        plt.close()
        return path

    for _, row in df.iterrows():
        grafico_path = gerar_grafico(row)
        pdf = RelatorioPDF()
        pdf.add_page()
        pdf.render(row, grafico_path, logo_path)

        with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            pdf.output(tmp_file.name)
            with open(tmp_file.name, "rb") as f:
                st.download_button(
                    label=f"📄 Baixar PDF - {row['Loja']}",
                    data=f.read(),
                    file_name=f"relatorio_{row['Loja'].lower().replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )
