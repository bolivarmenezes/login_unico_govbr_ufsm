import json
import requests
from authlib.common.security import generate_token
from authlib.jose import jwt
from authlib.oauth2.rfc7636 import create_s256_code_challenge
import configs.configs as confs
from authlib.integrations.requests_client import OAuth2Session
import random
import hashlib
from captive_portal.api.exceptions import AuthorizeError
from authlib.jose.errors import JoseError


class IntegraAPI:

    def __init__(self) -> None:
        self.url_provider = confs.url_provider
        self.api = confs.api
        self.url_catalogo_selos = confs.url_catalogo_selos
        self.redirect_uri = confs.redirect_uri
        self.scopes = confs.scopes
        self.secret = confs.secret
        self.client_id = confs.client_id
        self.code_challenge_method = confs.code_challenge_method
        self.jwk = confs.url_jwt
        self.client = OAuth2Session(client_id=self.client_id, client_secret=self.secret, scope=self.scopes,
                                    redirect_uri=self.redirect_uri)
        self.token_endpoint = confs.token_endpoint

        '''
        O processo de autenticação e autorização de recursos ocorre essencialmente em três etapas:

            Etapa 1: Chamada do serviço de autorização do Gov.br;
            Etapa 2: Recuperação do Access Token
            Etapa 3: Validação do Access Token por meio da verificação de sua assinatura.

        Após concluída essas três etapas, a aplicação cliente terá as informações básicas
        para conceder acesso de acordo com suas próprias políticas de autorização.

        '''

    @staticmethod
    def nonce() -> str:
        '''
        Sequência de caracteres usado para associar uma sessão do serviço consumidor a um Token de ID
        e para atenuar os ataques de repetição. Pode ser um valor aleatório, mas que não seja de fácil dedução.
        Item obrigatório.

        :return: hash de um valor random
        '''
        md5_hash = hashlib.md5()
        md5_hash.update(str(random.getrandbits(32)).encode())
        return md5_hash.hexdigest()

    def authorize(self) -> dict:
        # PKCE for Authorization Code
        code_verifier = generate_token(48)
        nonce = generate_token()
        code_challenge = create_s256_code_challenge(code_verifier)

        uri, state = self.client.create_authorization_url(
            url=confs.url_authorize,
            response_type='code',
            scope=self.scopes,
            nonce=nonce,
            code_verifier=code_verifier,
            code_challenge=code_challenge,
            code_challenge_method='S256',
        )
        response = {
            'uri': uri,
            'state': state,
            'code_verifier': code_verifier,
            'nonce': nonce
        }
        return response

    def valida_token(self, token) -> dict:
        token_dic = json.loads(token)

        access_token = token_dic['id_token']
        # JwtClaims

        # busca via get jwk
        public_key = requests.get(self.jwk)
        if public_key == 404:
            raise (AuthorizeError(
                'Erro 404: jwk não encontrado! Verificar arquivo configs.py'))

        public_key = public_key.text
        public_key = json.loads(public_key)
        public_key = public_key['keys'][0]

        # testa se recebeu um erro no token
        if "error" in token:
            raise (AuthorizeError(token['error']))

        try:
            options = {"verify_signature": True,
                       "verify_aud": True,
                       "exp": True}

            token = jwt.decode(access_token,
                               key=public_key,
                               claims_options=options,
                               )
            cpf = token['sub']

        except JoseError as e:
            print(AuthorizeError("Erro de Token: {}".format(e)))
            return False

        response = {
            "cpf": cpf,
            "access_token": token
        }
        return response

    def get_nivel(self, cpf_dados: dict, access_token: str):
        # converte access_token para json
        access_token = json.loads(access_token)['access_token']
        api = self.api
        cpf = cpf_dados['cpf']

        url_nivel = f"{api}/confiabilidades/v3/contas/{cpf}/niveis?response-type=ids"
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {access_token}"
                   }
        # print(url_nivel)
        nivel = requests.get(url_nivel, headers=headers)
        # print(json.loads(nivel.text))
        return json.loads(nivel.text)[0]['id']

    def get_data_atualizacao(self, cpf_dados: dict, access_token: str):
        # converte access_token para json
        access_token = json.loads(access_token)['access_token']
        api = self.api
        cpf = cpf_dados['cpf']

        url_nivel = f"{api}/confiabilidades/v3/contas/{cpf}/niveis?response-type=ids"
        headers = {"Accept": "application/json",
                   "Authorization": f"Bearer {access_token}"
                   }
        dataAtualizacao = requests.get(url_nivel, headers=headers)
        # print(dataAtualizacao.text)
        return json.loads(dataAtualizacao.text)[0]['dataAtualizacao']


if __name__ == '__main__':
    integra = IntegraAPI()
    integra.valida_token()
