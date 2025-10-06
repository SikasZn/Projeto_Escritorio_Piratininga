from db import SessionLocal, Lancamento
import pandas as pd
from utils import gerar_relatorios
import os

def gerar_relatorio_cliente(nome_cliente: str):
    session = SessionLocal()
    # Busca no banco por cliente (ignora maiúsculas/minúsculas)
    registros = session.query(Lancamento).filter(Lancamento.cliente.ilike(f"%{nome_cliente}%")).all()
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
        print(f"⚠️ Nenhum lançamento encontrado para o cliente: {nome_cliente}")
        return

    # Cria pasta do cliente em relatorios/
    pasta_saida = os.path.join("relatorios", nome_cliente.replace(" ", "_"))
    os.makedirs(pasta_saida, exist_ok=True)

    # Gera Excel/PDF diretamente do banco
    gerar_relatorios(df, pasta_saida)
    print(f"✅ Relatório gerado para o cliente '{nome_cliente}' em {pasta_saida}/")


if __name__ == "__main__":
    nome = input("Digite o nome do cliente: ")
    gerar_relatorio_cliente(nome)