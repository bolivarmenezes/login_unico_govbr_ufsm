# Autenticação WiFi utilizando o login único Gov.Br.

## Python3 + Django para captive portal externo e controladora Cisco.
Nesse exemplo foi criado um projeto Django com nome “login_unico” e uma aplicação com nome de “captive_portal”.

OBS: essa é versão modificado da aplicação implantada na UFSM, para auxiliar a quem interessar utilizar. Para realizar o deploy é importante observar os requisitos de segurança necessários, tanto para o Django como para a máquina que irá hospedá-lo. Lembrando de atender os requisitos do roteiro de integração do [login único gov.br][1].

### Crie um ambiente virtual python 
#### Instale as bibliotecas informadas no requirements.txt


### DJANGO
```shell
django-admin startproject login_unico .
django-admin startapp captive_portal
python3 manage.py makemigrations
python3 manage.py migrate
```
### Criar um superuser para acessar a área administrativa da interface Django
```shell
python3 manage.py createsuperuser
#entrar com as informações solicitadas
```


### CONFIGURAÇÕES DO ARQUIVO /login_unico/settings.py 

### Adição da aplicação “captive_portal”
```shell
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'captive_portal',
]
```

### configuração da base de dados (nesse caso, utilizado o postgreSQL)

```shell
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
```

### configurando o django para português do Brasil
```shell
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_L10N = True
USE_TZ = True
```

### configura arquivos estaticos
STATIC_URL = '/static/'

### configurando o arquivo de media, caso quei fazer upload de arquivos
MEDIA_URL = '/media/'

### não esquecer de importar o 'os'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
### configura para retornar para o index quando sair da área administrativa
LOGIN_REDIRECT_URL = 'index'
LOGOUT_REDIRECT_URL = 'login'
### tempo de sessão
PASSWORD_RESET_TIMEOUT_DAYS = '1'

------------
## Arquivo Views
### A parte principal da lógica (com comentários) da implatanção está no arquivo views
#### captive_portal/views.py
------------

## Configuração dos Arquivos de rotas 

Por questão de organização, foi criar um arquivo de rotas “url.py”, dentro da aplicação “captive_portal”. 

### Dessa forma, ficaram dois arquivos de rotas:
```shell
captive_portal/urls.py #indica o caminho do outro arquivo de rotas (url.py) e dos arquivos estáticos
login_unico/urls.py #define as rotas utilizadas na aplicação
```

------------
### DIRETÓRIO DE CONFIGURAÇÕES
#### substituir as configurações dos arquivos abaixo:
```shell
/configs
/configs/keys/private.pem
/configs/keys/private.pem
/configs/keys/public.pem
/configs/configs.py
```
------------
# Controladora WiFi (Cisco)
Para que o usuário realize o login em um site externo (login único gov.br) é necessário que haja uma liberação prévia de alguns endereços. A forma com que os endereços são liberados depende de qual controladora WiFi e qual versão está sendo utilizada. No caso da UFSM, são utilizadas duas controladoras WiFi Cisco, com diferentes versões cada. Na mais antiga, as liberações foram feitas via ACL e na mais nova, via URL Filter. 

### É necessário liberar essas URLs na CONTROLADORA WIFI para que o usuário possa acessar alguns serviços externos, utilizados na autenticação
#### Sem essa liberação, a autenticação externa não funcionará.
```shell
*.gov.br
*.1e100.net
*.hcaptcha.com
cdn.globalsigncdn.*
*googletagmanager.com
stats.g.doubleclick.net
www.google-analytics.com*
windowsupdatebg*
```
------------

[1]: https://manual-roteiro-integracao-login-unico.servicos.gov.br/pt/stable/index.html "login único gov.br"
