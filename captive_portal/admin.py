from django.contrib import admin

from .models import SessionGov, UserGov, UserPreference


class UserGovAdmin(admin.ModelAdmin):
    list_display = ('name', 'cpf', 'email', 'login_wifi', 'internal_user')


class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('cpf', 'termos', 'date')


class SessionGovAdmin(admin.ModelAdmin):
    list_display = ('ip', 'cpf', 'session_id', 'date', 'internal_user')


class LogsWifiAdmin(admin.ModelAdmin):
    list_display = ('mac', 'cpf', 'cisco_controller', 'date')


admin.site.register(UserGov, UserGovAdmin)
admin.site.register(UserPreference, UserPreferenceAdmin)
admin.site.register(SessionGov, SessionGovAdmin)
