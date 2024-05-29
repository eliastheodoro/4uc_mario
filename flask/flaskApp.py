import requests
from flask_test import Flask, redirect, request, url_for
import urllib.parse

app = Flask(__name__)

# Credenciais do cliente OAuth2
client_id = '6024824416511325'
client_secret = 'HochGPffTDwqP2FK5p31gt6MtVdkoVQo'
redirect_uri = 'https://www.google.com'  # Certifique-se de que esta URL está registrada no Mercado Livre
authorization_base_url = 'https://auth.mercadolivre.com.br/authorization'
token_url = 'https://api.mercadolibre.com/oauth/token'

# Rota para iniciar o processo de autorização
@app.route('/')
def index():
    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri
    }
    

# Rota de callback para processar o código de autorização
@app.route('/callback')
def callback():
    authorization_code = request.args.get('code')
    if authorization_code:
        token = fetch_token(authorization_code)
        return f'Token de Acesso: {token["access_token"]}<br>Token de Atualização: {token["refresh_token"]}'
    else:
        return 'Código de autorização não encontrado.'

# Função para buscar o token usando o código de autorização
def fetch_token(authorization_code):
    data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': redirect_uri,
        'client_id': client_id,
        'client_secret': client_secret
    }
    response = requests.post(token_url, data=data)
    response.raise_for_status()  # Verifica se houve erro na requisição
    return response.json()

if __name__ == '__main__':
    app.run(debug=True)
