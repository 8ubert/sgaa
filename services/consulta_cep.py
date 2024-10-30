import requests
import json

# URL da API ViaCEP
VIA_CEP_URL = "http://www.viacep.com.br/ws/{}/json"

def consulta_cep(cep):
    # Realiza a requisição para a API do ViaCEP
    resposta = requests.get(VIA_CEP_URL.format(cep))

    # Verifica se a resposta é bem-sucedida
    if resposta.ok:
        endereco = json.loads(resposta.text)

        # Checa se o CEP é inválido
        if 'erro' in endereco:
            return "CEP inválido"

        # Estrutura os dados do endereço
        return {
            "bairro": endereco.get("bairro", ""),
            "cep": endereco.get("cep", ""),
            "cidade": endereco.get("localidade", ""),
            "logradouro": endereco.get("logradouro", ""),
            "uf": endereco.get("uf", ""),
            "complemento": endereco.get("complemento", "")
        }