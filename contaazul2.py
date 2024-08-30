from urllib.parse import urlparse, parse_qs, urlencode
import requests
import base64
import pandas as pd

BASE_URL = 'https://api.contaazul.com/'
REDIRECT_URI = 'https://lmautopartsdistribuidoralt.mercadoshops.com.br'
AUTH_URL = f'{BASE_URL}auth/authorize'
TOKEN_URL = f'{BASE_URL}oauth2/token'
API_URL = f'{BASE_URL}v1/'
SCOPE = 'sales'
STATE = 'DCEeFWf45A53sdfKef424'

CLIENT_ID = 'u70YCOhwwPt3NvT3KGBcpZAsHz10wxyw'
CLIENT_SECRET = '0IHhfyvv0dEIUGJLEMrfjNpjxxq2kgPt'
EMAIL = 'edipron@contaazul.com'
PASS = r"9!J24%97by!%apA%fV2x"

def get_token():
    auth_params = {
        'redirect_uri': REDIRECT_URI,
        'client_id': CLIENT_ID,
        'scope': SCOPE,
        'state': STATE,
        'response_type': 'code'
    }

    authorize_url = f"{AUTH_URL}?{urlencode(auth_params)}"

    session = requests.Session()
    response = session.get(authorize_url)
    if response.status_code != 200:
        print("Erro ao acessar a URL de autorização:", response.text)
        return None

    login_data = {
        'email': EMAIL,
        'password': PASS
    }

    login_response = session.post(response.url, data=login_data)
    if login_response.status_code != 200:
        print("Erro ao fazer login:", login_response.text)
        return None

    current_url = login_response.url
    parsed_url = urlparse(current_url)
    authorization_code = parse_qs(parsed_url.query).get('code', [None])[0]
    state_code = parse_qs(parsed_url.query).get('state', [None])[0]
    credentials = f'{CLIENT_ID}:{CLIENT_SECRET}'
    credentials_base64 = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

    token_data = {
        'grant_type': 'authorization_code',
        'code': authorization_code,
        'redirect_uri': REDIRECT_URI,
    }

    headers = {
        'Authorization': f'Basic {credentials_base64}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    access_token = None
    
    if state_code == STATE:
        response = requests.post(TOKEN_URL, data=token_data, headers=headers)
        if response.status_code == 200:
            access_token = response.json()['access_token']
            refresh_token = response.json()['refresh_token']
            expires_in = response.json()['expires_in']
            token_type = response.json()['token_type']
            print(f'RETORNO OK --> {access_token}')
        else:
            print("Erro ao obter o token de acesso:", response.text)

    headers = {
        "Authorization": f"Bearer {access_token}",
        'Content-Type': 'application/json'
    }
    return headers

     
def get_product_categories(headers):
     response = requests.get(f"{API_URL}product-categories", headers=headers)
     if response.status_code == 200:
         data = response.json()
         return pd.DataFrame(data)
     else:
         print("Erro ao obter o token de acesso:", response.text)
         return None
    # response = requests.get(f"{API_URL}product-categories", headers=headers)
    # if response.status_code == 200:
    #     data = response.json()
    #     df = pd.DataFrame(data)
    #     return df
    # else:
    #     print("Erro ao obter o token de acesso:", response.text)
    #     return None

def save_product_categories(df):
    print(df)

def main():
    print("Iniciando processamento")
    headers = get_token()
    product_categories = get_product_categories(headers)
    if product_categories != None:
        save_product_categories(product_categories)

    # products = get_products(headers)
    # if products != None:
    #     save_products(products)

if __name__ == "__main__":
    main()