import base64
import os

### roteiro de integração #########################################################################
## https://manual-roteiro-integracao-login-unico.servicos.gov.br/pt/stable/iniciarintegracao.html###
###################################################################################################

script_dir = os.path.dirname(__file__)
# parâmetros informados pelo roteiro de integração do gov.br
token_endpoint = 'ADICIONAR O ENDPOINT DO TOKEN' #para ambiente de teste é diferente do de produção
code_challenge_method = "S256"
url_action = "https://endereco-da-controladora-wifi"

# links de produção ##########################################################################
url_provider = "" # deve ser informado
api = "" #deve ser informado
url_authorize = url_provider+"/authorize"
url_jwt = url_provider+"/jwk"
pagina_de_logout = "logout" #deve ser informado
url_catalogo_selos = "https://confiabilidades.staging.acesso.gov.br"
logout = url_provider+f"/logout?post_logout_redirect_uri={pagina_de_logout}"
redirect_uri = "auth" #mesmo endereço informado na solictação de acesso
scopes = ["openid", "email", "phone", "profile",
          "govbr_empresa", "govbr_confiabilidades"]

###############################################################################################
# credenciais de produção #####################################################################
client_id = "meuclienteid.br"#deve ser informado
secret = "minhasenhasecreta" #deve ser informado
authorization = f"{client_id}:{secret}" #após concatenar o client_id e o secret é necessário converter para base64
authorization64 = base64.b64encode(authorization.encode('utf-8')).decode('utf-8')
# o autorization64 é o client_id e o secret concatenados com : e convertidos para base64
# é um dos parâmetros passados no header da requisWSição de token
authorization64 = f"Basic {authorization64}"

# user gov fixado no radius. Se mudar no radius, será necessário alterar somente aqui
user_gov = "govbr"
password_gov = "teste001"
message_logout = "Você foi desconectado do gov.br!"
session_expire_gov = 4  # 4 horas
title_session_conn = "Conectado WiFi institucional"
title_session = "Conectado na rede WiFi institucional"
title_session_error = "Você não está utilizando o login único Gov.br"
##########################
url_redirect_default = "https://ufsm.br" #para onde será redirecionado após o login


#endereço da controladora 
captive_cisco1 = "https://endereco_cisoc_1.br"
captive_cisco2 = "https://endereco_cisco_2.br"

#chaves para criptografia (opcional para criptogravas dados nos coockies
private_key = "keys/private.pem"
public_key = "keys/public.pem"

#É necessário liberar essas URLs na controladora para que o usuário possa acessar alguns serviços externos, necessário para autenticação
#Sem essa liberação, autenticações externas não funcionam
'''*.gov.br
*.1e100.net
*.hcaptcha.com
cdn.globalsigncdn.*
*googletagmanager.com
stats.g.doubleclick.net
www.google-analytics.com*
windowsupdatebg*
'''
