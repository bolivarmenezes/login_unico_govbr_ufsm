Python3 + Django para captive portal externo e controladora Cisco 


Projeto “login_unico”, aplicação “captive_portal”


OBS: essa é uma versão para ser utilizada em ambiente de teste. Para realizar o deploy é importante observar os requisitos de segurança necessários, tanto para o Django como para a máquina que irá hospedá-lo!

CONFIGURAÇÕES DO ARQUIVO /login_unico/settings.py 

# Adição da aplicação “captive_portal”
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'captive_portal',
]

#configuração da base de dados (nesse caso, utilizado o postgreSQL)


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'login_unico',
        'USER': 'nome_user',
        'PASSWORD': 'senha_user',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


#connfigurando o django para português do Brasil
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True

#configura
STATIC_URL = 'static/'

#configurando o arquivo de media, caso quei fazer upload de arquivos
MEDIA_URL = '/media/'

#não esquecer de importar o 'os'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
# configura para retornar para o index quando sair da área administrativa
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'login'
#tempo de sessão
PASSWORD_RESET_TIMEOUT_DAYS = '1'




Configuração dos Arquivos de rotas 

Por questão de organização, foi criar um arquivo de rotas “url.py”, dentro da aplicação “captive_portal”. 

Dessa forma, ficaram dois arquivos de rotas:
captive_portal/urls.py #referencia os caminho do outro arquivo de rotas (url.py) 
login_unico/urls.py #define as rotas utilizadas na aplicação


_______________________________


DIRETÓRIO DE CONFIGURAÇÕES
/configs #substituir as configurações desse arquivo, por as apropriadas
/configs/keys/private.pem
/configs/keys/private.pem
/configs/keys/public.pem
/configs/configs.py

_____________________________


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








