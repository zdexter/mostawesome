from django.db import models
from django.db.models import Count
from random import randint

class RandomItemManager(models.Manager):
    def random(self):
        # For this demo, assume no deletion of objects or other gaps in ids.
        c = self.aggregate(count=Count('id'))['count']
        rand_index = randint(0, c-1)
        return self.all()[rand_index]

class Thing(models.Model):
    times_defeated = models.IntegerField(editable=False,default=0)
    times_won = models.IntegerField(editable=False,default=0)
    current_score = models.FloatField(editable=False,default=0)
    
    randoms = RandomItemManager()
    objects = models.Manager()
    name = models.CharField(max_length=64,verbose_name="What's awesome?")
    
    def __unicode__(self):
        return self.name