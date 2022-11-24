from django.conf import settings
from django.db import models
from django.forms import model_to_dict


class BaseModel(models.Model):
    user_creation = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                      related_name='%(app_label)s_%(class)s_creation', null=True, blank=True)
    date_creation = models.DateField(auto_now_add=True, null=True, blank=True)
    user_updated = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                     related_name='%(app_label)s_%(class)s_updated',  null=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    # def tojson(self):
    #     item = model_to_dict(self)
    #     item['user_creation'] = self.user_creation.__str__()
    #     item['user_updated'] = self.user_updated.__str__()
    #     item['date_creation'] = self.date_creation.strftime('%Y-%m-%d')
    #     item['date_updated'] = self.date_updated.strftime('%Y-%m-%d')
    #     return item

    class Meta:
        abstract = True
