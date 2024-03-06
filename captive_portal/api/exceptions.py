'''
Importa onde irá usar e depois chama com o raise
é preciso herdar o Exception, por se tratar da classe base, do qual
buscamos as  funcionalidades
def __int__(self, message='', saldo= None, valor=None):


import traceback
traceback.print_exc()
'''
class AuthorizeError(Exception):

    def __int__(self, message='', *args):
        msg = "Erro durante a obtenção do code"
        self.msg = message or msg  #caso message esteja em branco, mostra msg
        super(AuthorizeError, self).__init__(self.msg, *args)


