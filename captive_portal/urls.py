from django.urls import path
from .views import LogarControladoraAntiga, LogarControladoraAntiga, LoginView, AuthView, TokenView, LogoutView, \
    TermosView, LogarControladora, SessionView, ErrorView, RedeCabeadaView

urlpatterns = [    
    path('', LoginView.as_view(), name='index'),
    path('login.html/', LoginView.as_view(), name='login'),
    path('auth.html/', AuthView.as_view(), name='auth'), # essa foi a rota definida no redirect_uri da integração
    path('token.html/', TokenView.as_view(), name='token'), # rota para o token de autenticação
    path('logout.html/', LogoutView.as_view(), name='logout'), #rota para permitir o usuário efituar o logout
    path('termos.html/', TermosView.as_view(), name='termos'), # solicitação de permissão para gurdar os dados sa sessão
    path('session.html/', SessionView.as_view(), name='session'),
    path('controladora/', LogarControladora.as_view(), name='controladora'), #controladora cisco 9800
    path('controladora1/', LogarControladoraAntiga.as_view(), name='controladora1'), #controladora cisco 5500
    path('error/', ErrorView.as_view(), name='error'), # página de erro personalizada
    path('rede_cabeada/', RedeCabeadaView.as_view(), name='error'), # caso o usuário tente acessar por rede cabeada, é redirecionado para esta rota    
]