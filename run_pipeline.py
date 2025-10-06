# run_pipeline.py
from utils import importar_planilhas, padronizar_colunas, consolidar_dados, gerar_relatorios
import os

UPLOADS = "uploads"
SAIDA = "relatorios"

os.makedirs(UPLOADS, exist_ok=True)
os.makedirs(SAIDA, exist_ok=True)

def main():
    print("1) Importando planilhas...")
    planilhas = importar_planilhas(UPLOADS)
    if not planilhas:
        print("Nenhum arquivo encontrado em 'uploads/'. Coloque .xlsx/.csv lá e rode novamente.")
        return

    print(f"{len(planilhas)} arquivo(s) importado(s). Padronizando colunas...")
    planilhas_pad = [padronizar_colunas(df) for df in planilhas]

    print("Consolidando dados...")
    df_final = consolidar_dados(planilhas_pad)

    print("Gerando relatórios...")
    gerar_relatorios(df_final, SAIDA)
    print("Pipeline concluído.")

if __name__ == "__main__":
    main()