from django.db import models
import datetime
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import arrow

# Create your models here.
class Purchase(models.Model):

    def __unicode__(self):
        return unicode(self.purchase_date)

    class Meta:
        ordering = ['-purchase_date']

    user = models.ForeignKey(User)
    purchase_date = models.DateTimeField("Purchase Date",auto_now_add=True,default=datetime.datetime.now())
    amt = models.DecimalField("Purchase Amount",default=0,decimal_places=2,max_digits=7,validators=[MinValueValidator(0)])
    rack_cleared = models.BooleanField("Cleared The Rack",default=False)
    com_trip = models.BooleanField("Camaraderie Trip",default=False)
    free_coffee = models.BooleanField("Free Coffee",default=False)

class Item(models.Model):

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['active','name']

    name = models.CharField("Item Name",default="",max_length=200)
    active = models.BooleanField("Active Item",default=True)

class ItemStock(models.Model):

    def __unicode__(self):
        return unicode(self.item)

    class Meta:
        ordering = ['-entry_date']

    item = models.ForeignKey(Item,limit_choices_to={'active':True})
    user = models.ForeignKey(User)
    stock_status = models.IntegerField("Stock Status",default=0,validators=[MaxValueValidator(11),MinValueValidator(0)])
    entry_date = models.DateTimeField("Entry Time",auto_now_add=True,default=datetime.datetime.now())

