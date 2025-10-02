import os
import shutil
import pandas as pd
from datetime import datetime
from utils import importar_planilhas, padronizar_colunas
from db import SessionLocal, Lancamento, init_db

# -------------------------------
# 1) Importar planilhas -> Banco
# -------------------------------
def importar_para_db():
    init_db()
    session = SessionLocal()

    pasta_uploads = "uploads"
    pasta_processados = "uploads_processados"
    os.makedirs(pasta_processados, exist_ok=True)

    planilhas = importar_planilhas(pasta_uploads)
    if not planilhas:
        print("⚠️ Nenhuma planilha encontrada em 'uploads/'.")
        return
    
    arquivos_processados = []

    for df in planilhas:
        df = padronizar_colunas(df)
        for _, row in df.iterrows():
            lanc = Lancamento(
                cliente=row["Cliente"] or "Desconhecido",
                data=row["Data"].date() if not pd.isna(row["Data"]) else datetime.now().date(),
                descricao=row["Descrição"] or "",
                receita=float(row["Receita (R$)"]) if not pd.isna(row["Receita (R$)"]) else 0.0,
                despesa=float(row["Despesa (R$)"]) if not pd.isna(row["Despesa (R$)"]) else 0.0
            )
            session.add(lanc)

        # Pega o nome do arquivo de origem (marcado no importar_planilhas)
        if "Arquivo_Origem" in df.columns:
            arquivos_processados.append(df["Arquivo_Origem"].iloc[0])

    session.commit()
    session.close()
    print("✅ Uploads jogados no banco com sucesso!")

    # Mover arquivos processados
    for arq in arquivos_processados:
        origem = os.path.join(pasta_uploads, arq)
        destino = os.path.join(pasta_processados, arq)
        if os.path.exists(origem):
            shutil.move(origem, destino)
            print(f"📂 Arquivo movido para {pasta_processados}: {arq}")

# -------------------------------
# 2) Gerar relatórios do Banco
# -------------------------------
def gerar_relatorios_db():
    session = SessionLocal()
    registros = session.query(Lancamento).all()
    session.close()

    dados = [{
        "Cliente": r.cliente,
        "Data": r.data,
        "Descrição": r.descricao,
        "Receita (R$)": r.receita,
        "Despesa (R$)": r.despesa
    } for r in registros]

    df = pd.DataFrame(dados)
    if df.empty:
        print("⚠️ Nenhum dado no banco para gerar relatório.")
    else:
        gerar_relatorios(df, "relatorios")
        print("✅ Relatórios gerados em 'relatorios/'.")

# -------------------------------
# Execução principal
# -------------------------------
if __name__ == "__main__":
    importar_para_db()      # 1) Sobe Excel para o banco
    gerar_relatorios_db()   # 2) Gera relatórios do banco