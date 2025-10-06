from db import SessionLocal, Lancamento, init_db
from sqlalchemy import text

def limpar_banco():
    init_db()  # garante que a tabela existe
    session = SessionLocal()

    try:
        # Apaga todos os registros da tabela lancamentos
        num = session.query(Lancamento).delete()
        session.commit()
        print(f"✅ {num} registros apagados do banco de dados.")

        # Resetar o ID da tabela (PostgreSQL)
        session.execute(text("ALTER SEQUENCE lancamentos_id_seq RESTART WITH 1;"))
        session.commit()
        print("🔄 Sequência de IDs resetada para 1.")

    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao limpar banco: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    limpar_banco()