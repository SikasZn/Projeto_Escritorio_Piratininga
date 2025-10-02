from db import init_db, SessionLocal, Lancamento
from datetime import date

# Criar tabelas no banco
init_db()

# Testar inserção
session = SessionLocal()
novo = Lancamento(
    cliente="Padaria Pão Doce",
    data=date.today(),
    descricao="Venda de produtos",
    receita=5000,
    despesa=0
)
session.add(novo)
session.commit()

session = SessionLocal()
novo = Lancamento(
    cliente="Oficina Boq Parafuso",
    data=date.today(),
    descricao="Venda de parafusos",
    receita=20,
    despesa=0
)
session.add(novo)
session.commit()

session = SessionLocal()
novo = Lancamento(
    cliente="Oficina Boq Parafuso",
    data=date.today(),
    descricao="compra de parafuso",
    receita=0,
    despesa=5
)
session.add(novo)
session.commit()

# Testar leitura
dados = session.query(Lancamento).all()
for d in dados:
    print(d.id, d.cliente, d.receita, d.despesa)
session.close()