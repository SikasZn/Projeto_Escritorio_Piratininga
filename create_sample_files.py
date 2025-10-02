# create_sample_files.py
import pandas as pd
import os

os.makedirs("uploads", exist_ok=True)

df1 = pd.DataFrame({
    "Empresa": ["Padaria Pão Doce"]*3,
    "Data": ["01/09/2025", "05/09/2025", "10/09/2025"],
    "Detalhes": ["Venda de pães", "Compra farinha", "Venda bolos"],
    "Valor": ["5.000,00", "0,00", "3.500,00"],
    "Despesa": ["0,00", "2.000,00", "0,00"]
})
df1.to_excel("uploads/Padaria_Pao_Doce.xlsx", index=False)

df2 = pd.DataFrame({
    "Cliente": ["Oficina Rocha"]*3,
    "dia": ["02/09/2025", "12/09/2025", "22/09/2025"],
    "Descricao": ["Serviço X", "Compra peças", "Serviço Y"],
    "Receita": ["2.200,00", "0,00", "3.000,00"],
    "Custo": ["0,00", "800,00", "0,00"]
})
df2.to_excel("uploads/Oficina_Rocha.xlsx", index=False)

df3 = pd.DataFrame({
    "Cliente": ["Escritorio Teste"]*3,
    "dia": ["05/09/2025", "12/09/2025", "22/09/2025"],
    "Descricao": ["Serviço X", "Compra peças", "Serviço Y"],
    "Receita": ["2.200,00", "0,00", "3.000,00"],
    "Custo": ["0,00", "800,00", "0,00"]
})
df3.to_excel("uploads/Escritorio_Teste.xlsx", index=False)

df3 = pd.DataFrame({
    "Cliente": ["Oficina Boq Parafuso"]*3,
    "dia": ["05/09/2025", "12/09/2025", "22/09/2025"],
    "Descricao": ["Serviço Boq Parafuso", "Compra peças", "Serviço Reestocagem"],
    "Receita": ["2.200,00", "0,00", "3.000,00"],
    "Custo": ["0,00", "1.000,00", "0,00"]
})
df3.to_excel("uploads/Oficina_Boq_Parafuso.xlsx", index=False)

print("Arquivos de exemplo criado")