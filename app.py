from flask import Flask, jsonify, request
import cx_Oracle
import datetime

app = Flask(__name__)

# Configuração do banco Oracle
USER = "rm561090"
PASSWORD = "fiap25"
DSN = cx_Oracle.makedsn("oracle.fiap.com.br", 1521, service_name="orcl")

def conectar():
    try:
        conn = cx_Oracle.connect(user=USER, password=PASSWORD, dsn=DSN)
        return conn
    except cx_Oracle.DatabaseError as e:
        print("Erro ao conectar ao banco:", e)
        return None

def convert_value(value):
    if value is None:
        return None
    elif isinstance(value, datetime.datetime):
        return value.isoformat()
    elif isinstance(value, datetime.date):
        return value.isoformat()
    elif isinstance(value, bytes):
        return value.decode('utf-8', errors='ignore')
    elif isinstance(value, cx_Oracle.LOB):
        return value.read()
    else:
        return str(value)

def fetch_all_from(table):
    try:
        conn = conectar()
        if conn is None:
            return jsonify({"erro": "Não foi possível conectar ao banco."}), 500

        cur = conn.cursor()
        cur.execute(f"SELECT * FROM {table}")
        colnames = [col[0] for col in cur.description]
        rows = cur.fetchall()
        cur.close()
        conn.close()

        result = []
        for row in rows:
            row_dict = {colnames[i]: convert_value(value) for i, value in enumerate(row)}
            result.append(row_dict)

        return jsonify(result)
    except Exception as e:
        print(f"Erro ao buscar dados da tabela {table}: {e}")
        return jsonify({"erro": f"Erro ao buscar dados da tabela {table}."}), 500

@app.route("/usuarios", methods=["GET"])
def get_usuarios():
    return fetch_all_from("SF_Usuario")

@app.route("/contatos", methods=["GET"])
def get_contatos():
    return fetch_all_from("SF_ContatoEmergencia")

@app.route("/autoridades", methods=["GET"])
def get_autoridades():
    return fetch_all_from("SF_Autoridade")

@app.route("/categorias", methods=["GET"])
def get_categorias():
    return fetch_all_from("SF_CategoriaEvento")

@app.route("/sos", methods=["GET"])
def get_sos():
    return fetch_all_from("SF_SOS")

@app.route("/notificacoes", methods=["GET"])
def get_notificacoes():
    return fetch_all_from("SF_Notificacao")

@app.route("/mensagens", methods=["GET"])
def get_mensagens():
    return fetch_all_from("SF_Mensagem")

@app.route("/ocorrencias", methods=["GET"])
def get_ocorrencias():
    return fetch_all_from("SF_Ocorrencia")

@app.route("/cadastro", methods=["POST"])
def cadastro():
    data = request.json
    cpf = data.get("cpf")
    senha = data.get("senha")
    confirmar = data.get("confirmar_senha")

    if senha != confirmar:
        return jsonify({"erro": "Senhas não conferem."}), 400

    try:
        conn = conectar()
        if conn is None:
            return jsonify({"erro": "Erro ao conectar ao banco."}), 500

        cur = conn.cursor()
        cur.execute("""
            INSERT INTO SF_Usuario (id_usuario, cpf, senha, telefone)
            VALUES (SF_USUARIO_SEQ.NEXTVAL, :cpf, :senha, NULL)
        """, {"cpf": cpf, "senha": senha})
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"mensagem": "Usuário cadastrado com sucesso."})
    except cx_Oracle.IntegrityError:
        return jsonify({"erro": "CPF já cadastrado."}), 409
    except Exception as e:
        print(f"Erro no cadastro: {e}")
        return jsonify({"erro": "Erro interno no servidor."}), 500

if __name__ == "__main__":
    app.run(debug=True)
