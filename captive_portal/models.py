from django.db import models


class UserGov(models.Model):
    _id = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=30, blank=False, null=False)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    email_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=30)
    phone_number_verified = models.BooleanField(default=False)    
    iat = models.CharField(max_length=100, default='', blank=False)
    exp = models.CharField(max_length=100, default='', blank=False)    
    nonce = models.CharField(max_length=100, default='', blank=False)    
    last_update = models.CharField(max_length=200, default='', blank=False)    
    ap_mac = models.CharField(max_length=30, default='', blank=True)
    client_mac = models.CharField(max_length=30, default='', blank=True)
    wlan = models.CharField(max_length=30, default='', blank=True)
    ip = models.CharField(max_length=200, default='', blank=True)
    login_wifi = models.CharField(max_length=100, default='', blank=True)
    logout_wifi = models.CharField(max_length=100, default='', blank=True)
    internal_user = models.BooleanField(default=False)
    

    class Meta:
        ordering = ['-login_wifi']
        verbose_name = u'name'
        verbose_name_plural = u'names'

    def __str__(self):
        return self.name

    full_name = property(__str__)


class UserPreference(models.Model):
    _id = models.AutoField(primary_key=True)
    cpf = models.CharField(max_length=30, blank=False, null=False)
    termos = models.BooleanField(default=False)
    date = models.CharField(max_length=100, default='', blank=True)

    def __str__(self):
        return self.cpf


class SessionGov(models.Model):
    _id = models.AutoField(primary_key=True)
    ip = models.CharField(max_length=200, default='', blank=False)
    cpf = models.CharField(max_length=30, default='', null=False)
    session_id = models.CharField(max_length=300, default='', blank=False)
    date = models.CharField(max_length=100, default='', blank=True)
    internal_user = models.BooleanField(default=False)

    def __str__(self):
        return self.ip

