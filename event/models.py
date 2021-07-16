from django.db import models

from shortener.models import BitURL

class ClickEventManager(models.Manager):
    def create_event(self, instance):
        if isinstance(instance, BitURL):
            obj, created = self.get_or_create(bit_url = instance)
            obj.count += 1
            obj.save()
            return obj.count
        return None

class ClickEvent(models.Model):
    bit_url = models.OneToOneField(BitURL, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default = 0)
    timestamp = models.DateTimeField(auto_now_add= True)
    updated = models.DateTimeField(auto_now= True)

    objects = ClickEventManager()

    def __str__(self):
        return "{} - {}".format(self.count, self.bit_url.url[:50])