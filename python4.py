from flask import Flask, jsonify, request
import os
import json

app = Flask(__name__)

# Define o caminho para a pasta onde os arquivos JSON estão localizados
pasta_dados = os.path.join(os.path.dirname(__file__), "dados")

# Define o número de registros por consulta
REGISTROS_POR_CONSULTA = 10

# Função para ler os arquivos JSON e retornar registros
def get_registros(arquivo, start, end):
    path_arquivo = os.path.join(pasta_dados, arquivo)

    with open(path_arquivo, "r") as f:
        data = json.load(f)  # Carregar dados do arquivo JSON

    return data[start:end]

# Rota para retornar os registros de um arquivo JSON específico dentro de um intervalo
@app.route('/<arquivo>/consultar', methods=['GET'])
def consultar_registros(arquivo):
    start = int(request.args.get('start', 0))  # Obtém o índice de início da consulta
    end = int(request.args.get('end', start + REGISTROS_POR_CONSULTA))  # Obtém o índice de fim da consulta

    # Obtém os registros para o intervalo especificado do arquivo especificado
    registros = get_registros(arquivo + ".json", start, end)

    return jsonify(registros)

# Rota para a página inicial
@app.route('/')
def index():
    return 'Hello, world!'

if __name__ == "__main__":
    # Inicia o servidor Flask na porta 8080
    app.run(host='0.0.0.0', port=8080)
