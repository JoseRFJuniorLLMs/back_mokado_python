from flask import Flask, jsonify, request
import os
import json

app = Flask(__name__)

# Define o caminho para a pasta onde os arquivos JSON estão localizados
pasta_dados = os.path.join(os.path.dirname(__file__), "dados")

# Define o número de registros por página
REGISTROS_POR_PAGINA = 10


# Função para ler os arquivos JSON e criar endpoints REST
def criar_endpoints_para_arquivos_json():
    for arquivo in os.listdir(pasta_dados):
        if arquivo.endswith(".json"):
            nome_endpoint = os.path.splitext(arquivo)[0]
            path_arquivo = os.path.join(pasta_dados, arquivo)

            # Define a função para manipular a requisição GET
            def get_handler(file_path):
                def handler():
                    start = int(request.args.get('start', 0))  # Obtém o índice de início da página
                    end = start + REGISTROS_POR_PAGINA  # Calcula o índice de fim da página

                    with open(file_path, "r") as f:
                        data = json.load(f)  # Carregar dados do arquivo JSON

                    page_data = data[start:end]  # Obtém os registros para a página atual
                    return jsonify(page_data)
                return handler

            # Adiciona o endpoint REST para o arquivo JSON
            app.add_url_rule(f"/{nome_endpoint}", endpoint=nome_endpoint, view_func=get_handler(path_arquivo), methods=["GET"])


# Chama a função para criar os endpoints REST
criar_endpoints_para_arquivos_json()

if __name__ == "__main__":
    # Inicia o servidor Flask na porta 8080
    app.run(port=8080)
