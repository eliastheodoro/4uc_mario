import requests
import json
import os
from dotenv import load_dotenv

class ApiClient:
    def __init__(self):
        # Carrega as variáveis de ambiente do arquivo .env
        load_dotenv()

        # Configurações
        self.CONFIG = {
            'URI': os.getenv('URI'),
            'CLIENT_ID': os.getenv('CLIENT_ID'),
            'CLIENT_SECRET': os.getenv('CLIENT_SECRET'),
            'REDIRECT_URI': os.getenv('REDIRECT_URI'),
            'NOME_ARQUIVO': os.getenv('NOME_ARQUIVO'),
            'NOME_ARQUIVO_OUTPUT': os.getenv('NOME_ARQUIVO_OUTPUT'),
            'USER_ID': os.getenv('USER_ID')        }

        self.uri = self.CONFIG['URI']
        self.client_id = self.CONFIG['CLIENT_ID']
        self.client_secret = self.CONFIG['CLIENT_SECRET']
        self.redirect_uri = self.CONFIG['REDIRECT_URI']
        self.nome_arquivo = self.CONFIG['NOME_ARQUIVO']
        self.nome_arquivo_output = self.CONFIG['NOME_ARQUIVO_OUTPUT']

    def geraToken(self, code=None, refresh_token=None):
        """Gera um novo token."""
        param = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'redirect_uri': self.redirect_uri,
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

        response = requests.post(self.uri, headers=headers, data=param)

        if response.status_code == 400:
            print('Erro 400: Requisição inválida. Você deve gerar outro CODE ou usar um refresh token válido.')
            return response.json()
        else:
            data = response.json()
            self.salvar_variaveis_em_json(self.nome_arquivo, access_token=data.get("access_token"), refresh_token=data.get("refresh_token"))
            return data

    def salvar_variaveis_em_json(self, **variaveis):
        """Salva variáveis em um arquivo JSON."""
        with open(self.nome_arquivo, 'w') as file:
            json.dump(variaveis, file)

    def carregar_variaveis_do_json(self):
        """Carrega variáveis de um arquivo JSON."""
        try:
            with open(self.nome_arquivo, 'r') as file: 
                return json.load(file)
        except FileNotFoundError:
            print(f"Arquivo '{self.nome_arquivo}' não encontrado.")
            return {}

    def load_tokens_from_file(self):
        """Carrega tokens de um arquivo."""
        loaded_data = self.carregar_variaveis_do_json()
        return loaded_data.get("access_token"), loaded_data.get("refresh_token")

    def make_request(self, url, token):
        """Faz uma requisição GET para a URL fornecida com o token de autorização."""
        headers = {'Authorization': f'Bearer {token}'}
        return requests.request("GET", url, headers=headers)

    def get_all_listings(self, user_id):
        """Obtém todos os anúncios de um usuário."""
        url = f"https://api.mercadolibre.com/users/{user_id}/items/search?&limit=100&sub_status=out_of_stock"
        access_token, _ = self.load_tokens_from_file()
        response = self.make_request(url, access_token)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Erro ao obter anúncios: {response.json()}")
            return None

    def get_listing_status(self, listing_id):
        """Obtém o status e o substatus de um anúncio."""
        url = f"https://api.mercadolibre.com/items/{listing_id}"
        access_token, _ = self.load_tokens_from_file()
        response = self.make_request(url, access_token)
        if response.status_code == 200:
            data = response.json()
            return data.get("status"), data.get("sub_status")
        else:
            print(f"Erro ao obter status do anúncio: {response.json()}")
            return None, None

    def update_listing_status(self, user_id):
        """Atualiza o status e o substatus de todos os anúncios de um usuário a cada hora."""
        listings = self.get_all_listings(user_id)
        if listings:
            for listing_id in listings['results']:
                status, sub_status = self.get_listing_status(listing_id)
                print(f"Anúncio ID: {listing_id}, Status: {status}, Substatus: {sub_status}")    

    def main(self):
        """Função principal."""
        # Carrega arquivo de parametros e faz chamada na api
        access_token, refresh_token = self.load_tokens_from_file()
        url = f"https://api.mercadolibre.com/orders/search?seller={self.CONFIG['USER_ID']}"
        response = self.make_request(url, access_token)

        if response.status_code in [400, 401, 403]:
            print(response.json())
            print('Regerando Bearer code a partir do refresh token...')
            self.geraToken(refresh_token=refresh_token)

            # Recarrega o arquivo de parametros e faz o request novamente
            access_token, _ = self.load_tokens_from_file()
            response = self.make_request(url, access_token)
            print(response.json())
        else:
            self.salvar_variaveis_em_json(nome_arquivo=self.nome_arquivo_output, response=response.json())
            print(response.text)

if __name__ == "__main__":
    client = ApiClient() 
    client.update_listing_status(user_id=client.CONFIG['USER_ID'])