import requests
import json

uri = 'https://api.mercadolibre.com/oauth/token'
client_id = '1196296498468732'
client_secret = 'Ef4utzldvpALfFUygJZdJxzHooRen3Ng'
# code = 'TG-6655f0d7836be00001b3f403-17415698'
redirect_uri = 'https://www.google.com'
nome_arquivo = 'Z:\\Dados\\OneDrive\\Documentos\\codigo\\4uc_mario\\4uc_mario\\tokens.json'
nome_arquivo_output = 'Z:\\Dados\\OneDrive\\Documentos\\codigo\\4uc_mario\\4uc_mario\\out.json'


def geraToken(uri, client_id, client_secret, code=None, refresh_token=None, redirect_uri=None, access_token=None):
    param = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
    }

    if code:
        param['grant_type'] = 'authorization_code'
        param['code'] = code
    elif refresh_token:
        param['grant_type'] = 'refresh_token'
        param['refresh_token'] = refresh_token
    else:
        raise ValueError("É necessário fornecer 'code' ou 'refresh_token'.")

    headers = {
        'accept': 'application/json',
        'content-type': 'application/x-www-form-urlencoded'
    }

    response = requests.post(uri, headers=headers, data=param)

    if response.status_code == 400:
        print('Erro 400: Requisição inválida. Você deve gerar outro CODE ou usar um refresh token válido.')
        return response.json()
    else:
        # Coloque aqui o código para salvar o access token e o refresh token (se aplicável)
        # Salvar as variáveis em um arquivo
        salvar_variaveis_em_json(nome_arquivo, access_token=access_token, refresh_token=refresh_token)
        return response.json()

def salvar_variaveis_em_json(nome_arquivo, **variaveis):
    with open(nome_arquivo, 'w') as file:
        json.dump(variaveis, file)

def carregar_variaveis_do_json(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as file: 
            loaded_data = json.load(file)
            return loaded_data
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' não encontrado.")
        return {}

def salvar_output(nome_arquivo_output, **variaveis):
    with open(nome_arquivo, 'w') as file:
        json.dump(variaveis, file)

def main():


    # Carregar as variáveis do arquivo 'tokens.json'
    loaded_data = carregar_variaveis_do_json(nome_arquivo)
    access_token = loaded_data.get("access_token")
    refresh_token = loaded_data.get("refresh_token")

    url = f"https://api.mercadolibre.com/sites/MLB/search?seller_id=1317250329"

    headers = {
    'Authorization': f'Bearer {access_token}'
    }

# teste consulta api
    response = requests.request("GET", url, headers=headers)


    if response.status_code == 400:
        print('Erro 400: Requisição inválida. Você deve gerar outro CODE ou usar um refresh token válido.')
        print('Tentando refresh_token...')
        geraToken(uri, client_id, client_secret, refresh_token=refresh_token, redirect_uri=redirect_uri)
        return response.json()
    else:
        print("teste")
        salvar_output(nome_arquivo_output, access_token=access_token, refresh_token=refresh_token)
        # return response.json()
        print(response.text)

main()