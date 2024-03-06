import datetime

from captive_portal.models import SessionGov, UserGov, UserPreference


class BancoDeDados:

    def __init__(self) -> None:
        pass

    def insert_log(self, cpf, name, email, email_verified, phone_number, phone_number_verified, iat, exp, nonce, last_update, ap_mac, client_mac, wlan, ip, login_wifi, logout_wifi, internal_user):
        response = 'ok'

        try:
            user = UserGov(
                cpf=cpf, 
                name=name, 
                email=email, 
                email_verified=email_verified, 
                phone_number=phone_number, 
                phone_number_verified=phone_number_verified, 
                iat=iat, 
                exp=exp, 
                nonce=nonce, 
                last_update=last_update, 
                ap_mac=ap_mac, 
                client_mac=client_mac, 
                wlan=wlan, 
                ip=ip, 
                login_wifi=login_wifi, 
                logout_wifi=logout_wifi, 
                internal_user=internal_user
                )
            user.save(force_insert=True)

        except Exception as e:
            response = f'Erro ao salvar no banco de dados: {e}'

        return response

    def insert_preference(self, cpf, termos):
        cpfDB = 'vazio'
        response = 'ok'
        date = datetime.datetime.now()
        # busca cpf no banco de dados
        try:
            resp = UserPreference.objects.filter(cpf=cpf).order_by('-cpf')[0]
            cpfDB = resp.cpf
            termos = resp.termos
            # se tiver cpf no banco de dados, verificar se o termo é true ou false
            if termos == False:
                # atualiza o termo para true
                UserPreference.objects.filter(cpf=cpf).update(termos=True)

        except IndexError:
            pass

        # se o cpf já existe, não faz nada
        if cpfDB != 'vazio':
            return response
        # se o cpf não existe, insere
        try:
            user = UserPreference(cpf=cpf, termos=termos, date=date)
            user.save(force_insert=True)
        except Exception as e:
            response = f'Erro ao salvar preference no banco de dados: {e}'
        return response

    def insert_session(self, ip, cpf, session_id, internal_user):
        response = 'ok'
        date = datetime.datetime.now()
        try:
            user = SessionGov(ip=ip, cpf=cpf, session_id=session_id, date=date, internal_user=internal_user)
            user.save(force_insert=True)
        except Exception as e:
            response = f'Erro ao salvar session_id no banco de dados: {e}'
        return response

    def verifica_sessao(self, ip, session_key) -> str:
        session = 'vazio'
        # busca a sessão no banco de dados
        try:
            resp = SessionGov.objects.filter(
                ip=ip).order_by('-date')[0]
            sessionDb = resp.session_id

            # testa se a sessão é a mesma do banco
            if sessionDb == session_key:
                session = 'existe'

        except IndexError:
            pass

        except Exception as e:
            print(f'\nErro na busca pela sessão: {e}\n')

        return session

    def get_termos(self, cpf):
        # testa se o usuário já aceitou os termos. Se sim não pergunta novamente
        response = False
        # criar uma nova thread para fazer a inserção

        try:
            resp = UserPreference.objects.filter(cpf=cpf).order_by('-cpf')[0]
            response = resp.termos
            return response
        except Exception as e:
            response = f'Erro ao buscar termos no banco de dados: {e}'
        return response

    def get_all_access(self):
        # busca todos os acessos
        try:
            resp = UserGov.objects.all()
            return resp
        except Exception as e:
            response = f'Erro ao buscar acessos no banco de dados: {e}'
            return response
