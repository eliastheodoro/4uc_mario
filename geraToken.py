def obterToken(uri, client_id, client_secret, code=None, refresh_token=None, redirect_uri=None):
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
