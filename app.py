from flask import Flask, render_template_string, request, send_from_directory
import pandas as pd
from utils import padronizar_colunas
from db import SessionLocal, Lancamento, init_db
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = "segredo123"

# -----------------------------
# HTML templates simples
# -----------------------------
HTML_FORM = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Upload de Planilha</title>
</head>
<body>
    <h2>Upload de Planilha - Escritório Piratininga</h2>
    <form method="post" enctype="multipart/form-data" action="{{ url_for('upload') }}">
        <label>Nome da Empresa:</label>
        <input type="text" name="empresa" required><br><br>
        <label>Escolha a planilha:</label>
        <input type="file" name="file" accept=".xlsx,.csv" required><br><br>
        <button type="submit">Enviar</button>
    </form>
    <p style="color: green;">{{ mensagem }}</p>
    <hr>
    <a href="{{ url_for('listar_clientes') }}">📊 Ver clientes cadastrados</a>
</body>
</html>
"""

HTML_LISTA = """
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <title>Clientes Cadastrados</title>
</head>
<body>
    <h2>Clientes já cadastrados no banco</h2>
    {% if clientes %}
        <ul>
        {% for cliente in clientes %}
            <li>
                {{ cliente }}
                | <a href="{{ url_for('baixar_planilha', cliente=cliente) }}">📥 Baixar planilha padronizada</a>
            </li>
        {% endfor %}
        </ul>
    {% else %}
        <p>Nenhum cliente encontrado.</p>
    {% endif %}
    <hr>
    <a href="{{ url_for('index') }}">⬅ Voltar</a>
</body>
</html>
"""

# -----------------------------
# Rotas principais
# -----------------------------
@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_FORM, mensagem="")

@app.route("/upload", methods=["POST"])
def upload():
    empresa = request.form["empresa"].strip()
    file = request.files["file"]

    if not file:
        return render_template_string(HTML_FORM, mensagem="❌ Nenhum arquivo enviado.")

    try:
        # Ler planilha enviada
        if file.filename.endswith(".csv"):
            df = pd.read_csv(file)
        else:
            df = pd.read_excel(file)

        # Padronizar colunas
        df_padronizado = padronizar_colunas(df)
        df_padronizado["Cliente"] = empresa

        # Criar pasta de saída
        pasta_saida = os.path.join("uploads_padronizados", empresa.replace(" ", "_"))
        os.makedirs(pasta_saida, exist_ok=True)

        caminho_saida = os.path.join(
            pasta_saida, f"{empresa.replace(' ', '_')}_padronizado.xlsx"
        )
        df_padronizado.to_excel(caminho_saida, index=False)

        # Enviar para o banco
        init_db()
        session = SessionLocal()

        for _, row in df_padronizado.iterrows():
            lanc = Lancamento(
                cliente=row["Cliente"] or empresa,
                data=row["Data"].date() if pd.notna(row["Data"]) else datetime.now().date(),
                descricao=row["Descrição"] or "",
                receita=float(row["Receita (R$)"]) if pd.notna(row["Receita (R$)"]) else 0.0,
                despesa=float(row["Despesa (R$)"]) if pd.notna(row["Despesa (R$)"]) else 0.0,
            )
            session.add(lanc)

        session.commit()
        session.close()

        return render_template_string(
            HTML_FORM, mensagem=f"✅ Dados de {empresa} enviados com sucesso!"
        )

    except Exception as e:
        return render_template_string(HTML_FORM, mensagem=f"❌ Erro: {e}")

@app.route("/clientes", methods=["GET"])
def listar_clientes():
    # Buscar clientes distintos do banco
    session = SessionLocal()
    clientes = session.query(Lancamento.cliente).distinct().all()
    session.close()

    clientes_lista = [c[0] for c in clientes]
    return render_template_string(HTML_LISTA, clientes=clientes_lista)

@app.route("/download/<cliente>", methods=["GET"])
def baixar_planilha(cliente):
    pasta = os.path.join("uploads_padronizados", cliente.replace(" ", "_"))
    if not os.path.exists(pasta):
        return f"❌ Nenhuma planilha encontrada para {cliente}"

    # Sempre pega o último arquivo salvo
    arquivos = sorted(os.listdir(pasta), reverse=True)
    if not arquivos:
        return f"❌ Nenhuma planilha encontrada para {cliente}"

    arquivo = arquivos[0]  # mais recente
    return send_from_directory(pasta, arquivo, as_attachment=True)

# -----------------------------
# Inicializar servidor
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)