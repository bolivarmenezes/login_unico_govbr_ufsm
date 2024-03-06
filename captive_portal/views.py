from datetime import datetime
from urllib import request
import requests
from django.views import View
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from captive_portal.api.integra_api import IntegraAPI
from captive_portal.models import UserGov
from configs import configs as confs
from captive_portal.src.banco_de_dados import BancoDeDados
from captive_portal.api.criptografa import Criptografa
from .api.exceptions import AuthorizeError


class IndexView(View):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(confs.url_redirect_default)

class LoginView(TemplateView):
    template_name = 'login.html'

    def get_context_data(self, **kwargs):

        context = super(LoginView, self).get_context_data(**kwargs)
        # esse coockie serve para testar se o IP. Ele está sendo inicializado com "vazio"
        self.request.session['ip_ja_autenticado'] = 'vazio'

        ip = self.request.META.get('REMOTE_ADDR')
        # salva ip no cookie
        self.request.session['ip'] = ip
        # cria um cookie para a variável token
        self.request.session['token'] = '0'


        #IMPORTANTE!!!
        # o funcionamento deste metodo é totalmente dependente da forma de com que a Cisco Controller trata o url da requisição
        # se estiver testando sem a controladora, será redirecionada para a página administrativa do django
        # pega a url que aparece para o cliente, e a utiliza para obter os parâmetros
        url = self.request.build_absolute_uri()
        self.trata_url(url)

        # session id atual
        session_key = self.request.session.session_key

        ######################################################################################
        ######## identifica em qual controladora o usuário está logado  ######################
        ######## precisei fazer esse teste porque temos duas versões de controladoras  #######
        ######################################################################################
        controladora = self.identifica_controladora(url)
        ######################################################################################

        ######################################################################################
        ######## Primeira etapa do processo de autenticação: autenticação oAuth2 gov.br#######
        ######################################################################################
        integra = IntegraAPI()
        authorize = integra.authorize()
        uri_authorize = authorize['uri']

        context['uri_authorize'] = uri_authorize
        # o link gerado aqui (uri_authorize), contém todos os parâmetros necessários para a
        # API fazer a primeira solicitação para o gov.br
        ######################################################################################
        ######################################################################################

        ######################################################################################
        ## Verifica na base de dados se o usuário Possui um login ativo. Se sim, deixa passar#
        ######################################################################################
        db = BancoDeDados()
        session_db = db.verifica_sessao(ip, session_key)

        if session_db == 'existe':
            ip = self.request.session.get('ip')
            # criptografa o ip. Isso serve para descriptografar e garantir que foi o mesmo ip que fez a requisição
            cpt_ip = Criptografa()
            ip_cpt_passa_direto = cpt_ip.criptografa(ip)
            # salva ip criptografado na sessão
            self.request.session['ip_ja_autenticado'] = ip_cpt_passa_direto
            # nesse caso, ao invés de redirecionar para o gov.br, redireciona para o acesso direto
            context['uri_authorize'] = controladora
        else:
            # setar expire_date para 4 horas
            self.request.session.set_expiry(confs.session_expire_gov * 60 * 60)
        ######################################################################################
        ######################################################################################

        ######################################################################################
        ###### Guarda os parâmetros contidos no URI authorize, para uso posterior ############
        ######################################################################################
        nonce = authorize['nonce']
        self.request.session['nonce'] = nonce
        code_verifier = authorize['code_verifier']
        self.request.session['code_verifier'] = code_verifier
        return context

    def trata_url(self, url):        
        parametros = ''
        switch_url = ''
        ap_mac = ''
        client_mac = ''
        wlan = ''
        if 'statusCode' not in url:
            try:
                parametros = url.split("&")
                switch_url = parametros[0].split("=")[1]
                ap_mac = parametros[1].split("=")[1]
                client_mac = parametros[2].split("=")[1]
                wlan = parametros[3].split("=")[1]

            except IndexError:
                print(f"Erro ao obter parâmetros da URL (use apenas para rede WiFi)\n{url}\n")

        else:
            parametros = url.split("&")
            switch_url = parametros[0].split("=")[1]
            ap_mac = parametros[1].split("=")[1]
            client_mac = ''
            wlan = parametros[2].split("=")[1]
        # cria um cookie para a variável switch_url
        self.request.session['switch_url'] = switch_url
        # salva ap_mac no cookie
        self.request.session['ap_mac'] = ap_mac
        # salva client_mac no cookie
        self.request.session['client_mac'] = client_mac
        # salva wlan no cookie
        self.request.session['wlan'] = wlan

    def identifica_controladora(self, url):
        parametros = url.split("&")
        try:
            switch_url = parametros[0].split("=")[1]
            print("\n\n")
            print(switch_url)
        except IndexError:
            switch_url = None
            
        if switch_url is None:
            controladora = '/rede_cabeada'        
        elif switch_url == f"{confs.scaptive_cisco1}/login.html":  # controladora velha
            controladora = '/controladora1/'  # controladora velha
        elif switch_url == f"{confs.scaptive_cisco2}/login.html":  # controladora nova
            controladora = '/controladora/'  # controladora nova
        else:
            controladora = '/error'
        # salva tipo da controladora no cookie
        self.request.session['controladora'] = controladora
        return controladora

class LogoutView(TemplateView):
    template_name = 'logout.html'
    # Na prática não está sendo utilizado, mas era uma exigência do gov.br

    def get_context_data(self, **kwargs):
        context = super(LogoutView, self).get_context_data(**kwargs)
        context['logout'] = confs.logout
        context['message_logout'] = confs.message_logout
        # context['mensagem'] = ""
        self.request.session.flush()
        return context

class AuthView(View):
    template_name = 'auth.html'
    # recebe o retorno do Gov.br
    # nesse retorno, entre outras coisas, vem o code, necessário para obtenção do token

    def get(self, request):
        # o request contem o 'code' e o 'state', que serão utilizados para obter o token

        # como os parâmetros podem ser utilizados apenas uma vez, esses testes
        # servem para verificar se já foram utilizados e apresentar um erro mais amigável

        if 'code_verifier' not in self.request.session:
            print('code_verifier não foi setado')
            return HttpResponse('''<br><h1>Login Único gov.br passando por instabilidade (cv)</h1>
                                <br><h3>Por favor, utilize outra forma de acesso''')
        elif 'nonce' not in self.request.session:
            return HttpResponse('Dados inválidos! (n1)')

        # salva o code na session
        try:
            self.request.session['code'] = request.GET['code']
        except KeyError:
            return HttpResponse('Dados inválidos! (cd)')
        # salva o status da requisição na session
        try:
            self.request.session['status'] = request.GET['state']
        except KeyError:
            return HttpResponse('Dados inválidos! (st)')
        # passar o status depois
        return HttpResponseRedirect('/token.html')

class TokenView(View):
    template_name = 'token.html'
    # uma vez que o code foi obtido, é necessário obter o token
    # por medidas de segurança, é necessário comparar se o nonce recebido
    # é o mesmo que foi enviado, assim como o code_verifier
    # essa medida visa evitar ataques de replay e man-in-the-middle

    def fetch_token(self):
        # recupera o code da session
        code = self.request.session.get('code')
        # recupera o code_verifier da session
        code_verifier = self.request.session.get('code_verifier')

        # monta um pacote com os dados necessários para a obtenção do token
        # em seguida, realiza a requisição POST
        try:
            data_json = {
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": confs.redirect_uri,
                "code_verifier": code_verifier,
            }
            headers = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": confs.authorization64
            }

            uri = f"{confs.url_provider}/token?grant_type=authorization_code&code={code}&redirect_uri={confs.redirect_uri}&code_verifier={code_verifier}"
            r = request.post(
                url=uri,
                headers=headers,
                json=data_json
            )
            token = r.text

            # pega o ip do cliente
            ip = self.request.META.get('REMOTE_ADDR')
            cpt = Criptografa()
            ip_cpt = cpt.criptografa(ip)

            # salva ip_cpt no cookie
            self.request.session['ip_cpt'] = ip_cpt

            if 'error_description' in token:
                raise AuthorizeError(r.json()['error_description'])

        except AuthorizeError as E:
            print(f"Error: {E}")
            if E == 'Code not valid':
                return -1  # code inválido

            print(f"Error: {E}")
            return HttpResponseRedirect('Erro de autorização na obtenção do token')
        except requests.exceptions.ConnectionError:
            return HttpResponseRedirect('Não conseguiu conectar: verificar o DNS e/ou a conexão com a internet')

        return token

    def get(self, request, *args, **kwargs):
        # pega os dados armazenadas na session para realizar as verificações de segurança
        if 'code_verifier' not in self.request.session:
            # testa se o code_verifier está na session
            return HttpResponse('Dados inválidos! (cv)')
        elif 'nonce' not in self.request.session:
            # testa se o nonce está na session
            return HttpResponse('Dados inválidos! (n1)')

        # obtem o token
        token = self.fetch_token()

        # antes de validar o token, verifica se o code é válido
        if 'access_token' not in token:
            if token.status_code == 302:
                return HttpResponse(f'Code inválido ou já utilizado')
        # essa classe é responsável por fazer as requisições para a API e validações
        integra = IntegraAPI()

        # valida o token e recupera os dados do usuário
        cpf_dados = integra.valida_token(token)

        # testa se o nonce é válido
        nonce = self.request.session.get('nonce')

        if nonce != cpf_dados['access_token']['nonce']:
            return HttpResponse('Nonce inválido')

        # salva o token na session
        self.request.session['token'] = token

        # Buscando a data da última atualização que o usuário fez em seus dados no gov.br
        last_update = integra.get_data_atualizacao(cpf_dados, token)
        email = True
        phone_number_verified = True
        if cpf_dados['access_token']['email_verified'] == 'false':
            email = False
        if cpf_dados['access_token']['phone_number_verified'] == 'false':
            phone_number_verified = False

        ######################################################################################
        ############### busca informações para salvar na base de dados########################
        ######################################################################################

        # data e hora de agora
        now = datetime.datetime.now()
        # tempo de expiração do acesso
        duracao = datetime.timedelta(hours=confs.session_expire_gov)
        end_session = now + duracao

        cpf = cpf_dados['access_token']['preferred_username']

        name = cpf_dados['access_token']['name']
        # salva name na session
        self.request.session['name'] = name

        dados_gov = {
            'cpf': cpf,
            'name': name,
            'email': cpf_dados['access_token']['email'],
            'email_verified': email,
            'phone_number': cpf_dados['access_token']['phone_number'],
            'phone_number_verified': phone_number_verified,
            # 'picture': cpf_dados['access_token']['picture'],
            'iat': cpf_dados['access_token']['iat'],
            'exp': cpf_dados['access_token']['exp'],
            # 'amr': cpf_dados['access_token']['amr'],
            'nonce': cpf_dados['access_token']['nonce'],
            # 'profile': cpf_dados['access_token']['profile'],
            'login_wifi': now,
            'logout_wifi': end_session,
        }
        dados_gov['last_update'] = str(last_update)

        # busca ap_mac dos cookies
        ap_mac = self.request.session.get('ap_mac')
        # busca client_mac dos cookies
        client_mac = self.request.session.get('client_mac')
        # busca wlan dos cookies
        wlan = self.request.session.get('wlan')
        # busca o ip dos cookies
        ip = self.request.session.get('ip')

        # verifica se o usuário é da institucional
        internal_user = True
        '''internal_user = True
        try:
            ldap = LDAPSearch()
            internal_user = ldap.get_if_exist(cpf)
            dados_gov['internal_user'] = internal_user
        except:
            dados_gov['internal_user'] = True  
        '''          
        
        dados_gov['ap_mac'] = ap_mac
        dados_gov['client_mac'] = client_mac
        dados_gov['wlan'] = wlan
        dados_gov['ip'] = ip
        # salvar no banco de dados os logs de acesso
        bd = BancoDeDados()
        response = bd.insert_log(**dados_gov)
        if response != 'ok':
            return HttpResponse(f'Erro ao salvar no banco de dados: {response}')

        # pega a sessão atual
        session_id = self.request.session.session_key
        # salva no banco de dados os dados o id da sessão atual
        # pega o ip do usuário
        response = bd.insert_session(
            ip=ip, cpf=cpf, session_id=session_id, internal_user=internal_user)
        # salva cpf no cookie
        self.request.session['cpf'] = cpf
        # redireciona para outra página
        return HttpResponseRedirect('/termos.html')

class TermosView(TemplateView):
    template_name = 'termos.html'

    def get_context_data(self, **kwargs):
        context = super(TermosView, self).get_context_data(**kwargs)
        context['sessao_ativa'] = False
        context['termos'] = False
        bd = BancoDeDados()
        # verificar se já aceitou os termos
        cpf = self.request.session.get('cpf')
        response = False
        if cpf:
            response = bd.get_termos(cpf)
            if response is True:
                context['termos'] = response

        context['session_info'] = ''
        context['logout'] = confs.logout

        # busca controladora nos coockies
        controladora = self.request.session.get('controladora')
        context['controladora'] = controladora

        if 'code_verifier' not in self.request.session:
            context['session_info'] = 'error (cv)'
            return context
        elif 'nonce' not in self.request.session:
            context['session_info'] = 'error (n)'
            return context
        elif 'uri_authorize' not in self.request.session:
            # self.request.session.flush()
            context['session_info'] = 'error (ua)'
            return context

        # recupera o token da session
        token = self.request.session.get('token')
        # testa se o token está setado
        if token == '0':
            context['session_info'] = 'error'
            return context

        try:
            urlController = self.request.session.get('urlController')
            url = urlController.split('switch_url=')
            url_action = url[1].split('&')[0]
            context['url_action'] = url_action
            # retonar o usuário e senha fixados no radius e que serão utilizados para autenticar na controladora
            context['user_gov'] = confs.user_gov # esse usuário é o que permite logar na controladora após o sucesso na autenticação
            context['password_gov'] = confs.password_gov 
        except:
            pass
        return context

class LogarControladora(TemplateView):
    # caso o usuário esteja utilizando a controladora nova,
    # é pra esse lugar que ele vai ser redirecionado
    template_name = 'logar_controladora.html'

    def get_context_data(self, **kwargs):

        # informa que o usuário aceitou os termos, para não pedir novamente
        cpf = self.request.session.get('cpf')
        bd = BancoDeDados()
        bd.insert_preference(cpf, termos=1)

        context = super(LogarControladora,
                        self).get_context_data(**kwargs)

        # testa se o usuário já estava logado####################################
        ip_cpt_passa_direto = self.request.session['ip_ja_autenticado']
        if ip_cpt_passa_direto != 'vazio':
            # pega o ip do usuário
            ip = self.request.session.get('ip')
            # descriptografar o ip_cpt_passa_direto
            des = Criptografa()
            ip_cpt_passa_direto = des.descriptografa(ip_cpt_passa_direto)
            if ip_cpt_passa_direto == ip:
                context['user_gov'] = confs.user_gov
                context['password_gov'] = confs.password_gov
                # busca switch_url dos cookies
                switch_url = self.request.session.get('switch_url')
                context['url_action'] = switch_url

                # limpa cookie ip_cpt
                self.request.session['ip_cpt'] = '0'
                # passou direto porque já estava logado
                return context
        ########################################################################
        ip_dpt = '0'
        # busca ip_cpt dos cookies
        ip_cpt = self.request.session.get('ip_cpt')

        # descriptografa o ip_cpt, se for diferente de 0
        if ip_cpt != '0' and ip_cpt is not None:
            cpt = Criptografa()
            ip_dpt = cpt.descriptografa(ip_cpt)
            # compara com o ip atual do usuário com o criptografado no inicio da sessão
            ip_cpt = '0'

        ip = self.request.META.get('REMOTE_ADDR')
        # se for diferente ou se já tiver sido utilizado, não passa daqui
        if ip_dpt != ip or ip_dpt == '0':
            self.request.session.flush()
            context['user_gov'] = 'error'
            context['password_gov'] = 'error'
            context['url_action'] = '/error/'
            return context
        ip_dpt = '0'

        context['user_gov'] = confs.user_gov
        context['password_gov'] = confs.password_gov
        # busca switch_url dos cookies
        switch_url = self.request.session.get('switch_url')
        context['url_action'] = switch_url

        # limpa cookie ip_cpt
        self.request.session['ip_cpt'] = '0'

        return context

class LogarControladoraAntiga(TemplateView):
    # caso o usuário esteja utilizando a controladora velha (1 ou a 2),
    # é pra esse lugar que ele vai ser redirecionado
    template_name = 'logar_controladora_antiga.html'

    def get_context_data(self, **kwargs):
        context = super(LogarControladoraAntiga,
                        self).get_context_data(**kwargs)
        ip_cpt_passa_direto = self.request.session['ip_ja_autenticado']
        if ip_cpt_passa_direto != 'vazio':
            # pega o ip do usuário
            ip = self.request.session.get('ip')
            # descriptografar o ip_cpt_passa_direto
            des = Criptografa()
            ip_cpt_passa_direto = des.descriptografa(ip_cpt_passa_direto)
            if ip_cpt_passa_direto == ip:
                context['user_gov'] = confs.user_gov
                context['password_gov'] = confs.password_gov
                # busca switch_url dos cookies
                switch_url = self.request.session.get('switch_url')
                context['url_action'] = switch_url

                # limpa cookie ip_cpt
                self.request.session['ip_cpt'] = '0'
                # passou direto porque já estava logado
                return context
        ########################################################################

        ip_dpt = '0'
        # informa que o usuário aceitou os termos, para não pedir novamente
        cpf = self.request.session.get('cpf')
        bd = BancoDeDados()
        bd.insert_preference(cpf, termos=1)
        # busca ip_cpt dos cookies
        ip_cpt = self.request.session.get('ip_cpt')
        # descriptografa o ip_cpt, se for diferente de 0
        if ip_cpt != '0' and ip_cpt is not None:
            cpt = Criptografa()
            ip_dpt = cpt.descriptografa(ip_cpt)
            # compara com o ip atual do usuário com o criptografado no inicio da sessão
            ip_cpt = '0'

        ip = self.request.META.get('REMOTE_ADDR')
        # se for diferente ou se já tiver sido utilizado, não passa daqui
        if ip_dpt != ip or ip_dpt == '0':
            self.request.session.flush()
            context['user_gov'] = 'error'
            context['password_gov'] = 'error'
            context['url_action'] = '/error/'
            return context
        ip_dpt = '0'

        context['user_gov'] = confs.user_gov
        context['password_gov'] = confs.password_gov
        # busca switch_url dos cookies
        switch_url = self.request.session.get('switch_url')
        context['url_action'] = switch_url

        # limpa cookie ip_cpt
        self.request.session['ip_cpt'] = '0'

        return context

class SessionView(TemplateView):
    template_name = 'session.html'
    # essa página foi criada para atender uma exigência do gob.br
    # após o usuário logar, ele é redirecionado para essa página
    # a qual têm um botão de logout do gov.br
    # no momento, não estamos utilizando

    def get_context_data(self, **kwargs):
        context = super(SessionView, self).get_context_data(**kwargs)
        # impede algumas coisas (só para teste)
        self.request.session.flush()

        # pega mac
        mac = self.request.session.get('client_mac')
        if mac is None:
            # pega ip do cliente
            ip = self.request.META.get('REMOTE_ADDR')
            # print(f"\n\nIP: {ip}\n\n")

        # busca pelo mac do banco de dados
        try:
            # busca pelo ultimo registro do mac
            dados = UserGov.objects.all().filter(
                client_mac=mac).order_by('-login_wifi').first()
        except Exception as e:
            self.request.session.flush()
            print(f"\n\nErro ao busca informações do banco: {e}\n\n")
            return context

        try:
            name = dados.name
            cpf = dados.cpf
            email = dados.email
            phone_number = dados.phone_number
            login_wifi = dados.login_wifi.split('.')[0]
            logout_wifi = dados.logout_wifi.split('.')[0]
            client_mac = dados.client_mac
            ip = dados.ip

            context['title'] = confs.title_session_conn
            context['name'] = name
            context['ip'] = ip
            context['cpf'] = cpf
            context['email'] = email
            context['phone_number'] = phone_number
            context['login_wifi'] = login_wifi
            context['logout_wifi'] = logout_wifi
            context['client_mac'] = client_mac
            context['logout'] = confs.logout
            context['test'] = 1
            self.request.session.flush()
        except Exception as e:
            print(
                f"\n\nErro na busca de informação para a página session: {e}\n\n")
            context['title'] = confs.title_session
            context['ir_site'] = f"{confs.url_redirect_default}"
            context['test'] = 0
            # se cair aqui, é porque o usuário não está logado no gov.br
            # então redireciona para a página institucional
            self.request.session.flush()

            return context

        return context

class ErrorView(TemplateView):
    template_name = 'error.html'
    # página de erro simples, para quando o usuário não conseguir logar na wifi (sem gov.br)

    def get_context_data(self, **kwargs):
        context = super(ErrorView, self).get_context_data(**kwargs)
        # self.request.session.flush()
        return context

class RedeCabeadaView(TemplateView):
    template_name = 'rede_cabeada.html'

    def get_context_data(self, **kwargs):
        context = super(RedeCabeadaView, self).get_context_data(**kwargs)
        return context
