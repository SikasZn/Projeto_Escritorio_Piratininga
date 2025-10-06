import os
import re
import pandas as pd
from fpdf import FPDF
from datetime import datetime

# ---------------------------
# Padronização de colunas
# ---------------------------
def _parse_currency(x):
    if pd.isna(x):
        return None
    if isinstance(x, (int, float)):
        return float(x)
    s = str(x).strip().replace("R$", "").replace(" ", "")
    s = s.replace(".", "").replace(",", ".")
    s = re.sub(r"[^0-9\.\-]", "", s)
    return float(s) if s else None

def padronizar_colunas(df):
    equivalencias = {
        "cliente": "Cliente", "empresa": "Cliente", "nome": "Cliente",
        "data": "Data", "dia": "Data",
        "descrição": "Descrição", "descricao": "Descrição", "detalhes": "Descrição",
        "valor": "Receita (R$)", "receita": "Receita (R$)", "entrada": "Receita (R$)",
        "despesa": "Despesa (R$)", "custo": "Despesa (R$)", "saida": "Despesa (R$)"
    }
    colunas = {}
    for col in df.columns:
        chave = col.lower().strip()
        colunas[col] = equivalencias.get(chave, col)
    df = df.rename(columns=colunas)

    for c in ["Cliente", "Data", "Descrição", "Receita (R$)", "Despesa (R$)"]:
        if c not in df.columns:
            df[c] = None

    df["Receita (R$)"] = df["Receita (R$)"].apply(_parse_currency)
    df["Despesa (R$)"] = df["Despesa (R$)"].apply(_parse_currency)
    df["Data"] = pd.to_datetime(df["Data"], errors="coerce", dayfirst=True)

    return df[["Cliente", "Data", "Descrição", "Receita (R$)", "Despesa (R$)"]]

# ---------------------------
# Importar planilhas
# ---------------------------
def importar_planilhas(pasta="uploads"):
    arquivos = []
    for f in os.listdir(pasta):
        if f.lower().endswith((".xlsx", ".xls", ".csv")):
            caminho = os.path.join(pasta, f)
            try:
                df = pd.read_excel(caminho) if f.endswith("x") else pd.read_csv(caminho)
                df["Arquivo_Origem"] = f
                arquivos.append(df)
            except Exception as e:
                print(f"Erro ao ler {f}: {e}")
    return arquivos

# ---------------------------
# Gerar relatórios
# ---------------------------
def gerar_relatorios(df, pasta_saida="relatorios"):
    os.makedirs(pasta_saida, exist_ok=True)
    if df.empty:
        print("⚠️ Nenhum dado para gerar relatório.")
        return

    df["Data"] = pd.to_datetime(df["Data"], errors="coerce", dayfirst=True)
    df = df.dropna(subset=["Data"])
    df["Mes"] = df["Data"].dt.to_period("M").astype(str)

    for mes, grupo in df.groupby("Mes"):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nome_excel = os.path.join(pasta_saida, f"Relatorio_{mes}_{timestamp}.xlsx")
        nome_pdf   = os.path.join(pasta_saida, f"Relatorio_{mes}_{timestamp}.pdf")

        grupo.sort_values(by="Data").to_excel(nome_excel, index=False)
        print(f"✅ Excel gerado: {nome_excel}")

        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(0, 8, f"Relatório Mensal - {mes}", ln=True, align="C")
        pdf.ln(8)

        total_receita = grupo["Receita (R$)"].sum(min_count=1)
        total_despesa = grupo["Despesa (R$)"].sum(min_count=1)
        saldo = (total_receita or 0) - (total_despesa or 0)

        pdf.cell(0, 6, f"Total Receita: R$ {total_receita:.2f}", ln=True)
        pdf.cell(0, 6, f"Total Despesa: R$ {total_despesa:.2f}", ln=True)
        pdf.cell(0, 6, f"Saldo: R$ {saldo:.2f}", ln=True)
        pdf.ln(6)

        pdf.set_font("Arial", style="B", size=10)
        pdf.cell(35, 6, "Data")
        pdf.cell(60, 6, "Cliente / Descrição")
        pdf.cell(40, 6, "Receita", align="R")
        pdf.cell(40, 6, "Despesa", align="R")
        pdf.ln(6)

        pdf.set_font("Arial", size=9)
        for _, row in grupo.iterrows():
            data_txt = row["Data"].strftime("%d/%m/%Y") if pd.notna(row["Data"]) else ""
            desc = f"{row['Cliente']} - {row['Descrição']}"
            rec = f"{row['Receita (R$)']:.2f}" if pd.notna(row['Receita (R$)']) else ""
            desp = f"{row['Despesa (R$)']:.2f}" if pd.notna(row['Despesa (R$)']) else ""
            pdf.cell(35, 6, data_txt)
            pdf.cell(60, 6, desc[:50])
            pdf.cell(40, 6, rec, align="R")
            pdf.cell(40, 6, desp, align="R")
            pdf.ln(6)

        pdf.output(nome_pdf)
        print(f"✅ PDF gerado: {nome_pdf}")