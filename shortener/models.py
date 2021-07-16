from django.db import models
from django.conf import settings
from django.urls import reverse

from .utils import code_check
from .validators import validate_url, validate_dot_com

# Create your models here.
SHORTCODE_MAX= getattr(settings, 'SHORTCODE_MAX', 16)

class BitURLManager(models.Manager):
    def all(self, *args, **kwargs):
        qs_all = super(BitURLManager, self).all(*args, **kwargs) 
        qs = qs_all.filter(active = True)
        return qs 

    def refresh_shortcodes(self):
        qs_all = BitURL.objects.all()
        count = 0
        for qs in qs_all:
            qs.shortcode = code_check(qs)
            qs.save()
            count += 1
        return "ShortCode refresh count : {c}".format(c = count)

class BitURL(models.Model):
    url = models.CharField(max_length=255, unique=True, validators=[validate_url, validate_dot_com])
    shortcode = models.CharField(max_length = SHORTCODE_MAX, unique=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default = True)

    objects = BitURLManager()

    def save(self, *args, **kwargs):
        if self.shortcode is None or self.shortcode == "":
            self.shortcode = code_check(self)
            
        # this is much better way of adding http:// instead of doing in clean_url method of forms.py
        if not "http" in self.url:
            self.url = "http://" + self.url
        super(BitURL, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.url)
    
    def get_short_url(self):
        # short_url = reverse('redirect_url', kwargs={'shortcode':self.shortcode}) 
        print('-------'+self.shortcode)
        return "http://127.0.0.1:8000" + self.shortcode