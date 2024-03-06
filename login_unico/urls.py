from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls), #rota para a parte administrativa do django
    path('', include('captive_portal.urls')), #rota para o outro arquivo de rotas
    path('accounts/', include('django.contrib.auth.urls')), #rota para a parte de autenticação
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #para imagens, caso seja necessário