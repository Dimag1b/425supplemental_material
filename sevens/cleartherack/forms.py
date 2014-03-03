from django import forms
from django.forms import ModelForm
from cleartherack.models import Purchase, Item, ItemStock
from django.contrib.auth.models import User
from django.forms.widgets import Input

class Html5TelephoneInput(Input):
    input_type = 'tel'


class Html5CheckboxInput(Input):
    input_type = "checkbox"


class Html5URLInput(Input):
    input_type = 'url'


class Html5EmailInput(Input):
    input_type = 'email'


class Html5DateTimeInput(Input):
    input_type = 'datetime'


class Html5DateInput(Input):
    input_type = 'date'


class Html5NumberInput(Input):
    input_type = 'number'


class Html5RangeInput(Input):
    input_type = 'range'

class PurchaseForm(ModelForm):

	def __init__(self, username=None, *args, **kwargs):    
   		super(PurchaseForm, self ).__init__(*args, **kwargs)
   
   		try:
   			if not username == None:
	   			self.fields['user'].queryset = User.objects.filter(pk=username.user.id)
   		except Exception, e:
   			raise ValueError("No username supplied. %s" % e)

	   	self.fields['user'].widget = forms.HiddenInput()
	   	self.fields['rack_cleared'].widget = forms.HiddenInput()
	   	self.fields['com_trip'].widget = forms.HiddenInput()
	   	self.fields['free_coffee'].widget = forms.HiddenInput()


	class Meta:
		model = Purchase
		widgets = dict(amt=Html5NumberInput({'required': True,'max':999,'min':0,'step':.01}))

class ClearTheRackForm(ModelForm):

	def __init__(self, username=None, *args, **kwargs):    
   		super(ClearTheRackForm, self ).__init__(*args, **kwargs)
   
   		try:
   			if not username == None:
	   			self.fields['user'].queryset = User.objects.filter(pk=username.user.id)
   		except Exception, e:
   			raise ValueError("No username supplied. %s" % e)

	   	self.fields['user'].widget = forms.HiddenInput()
	   	#self.fields['amt'].widget = forms.HiddenInput()
	   	self.fields['com_trip'].widget = forms.HiddenInput()
	   	self.fields['free_coffee'].widget = forms.HiddenInput()


	class Meta:
		model = Purchase
		widgets = dict(amt=Html5NumberInput({'required': True,'max':999,'min':0,'step':.01}))

class CoffeeForm(ModelForm):

	def __init__(self, username=None, *args, **kwargs):    
   		super(CoffeeForm, self ).__init__(*args, **kwargs)
   
   		try:
   			if not username == None:
	   			self.fields['user'].queryset = User.objects.filter(pk=username.user.id)
   		except Exception, e:
   			raise ValueError("No username supplied. %s" % e)

	   	self.fields['user'].widget = forms.HiddenInput()
	   	self.fields['amt'].widget = forms.HiddenInput()
	   	self.fields['com_trip'].widget = forms.HiddenInput()
	   	self.fields['rack_cleared'].widget = forms.HiddenInput()


	class Meta:
		model = Purchase
		widgets = dict(amt=Html5NumberInput({'required': True,'max':999,'min':0}))

class ComTripForm(ModelForm):

	def __init__(self, username=None, *args, **kwargs):    
   		super(ComTripForm, self ).__init__(*args, **kwargs)
   
   		try:
   			if not username == None:
	   			self.fields['user'].queryset = User.objects.filter(pk=username.user.id)
   		except Exception, e:
   			raise ValueError("No username supplied. %s" % e)


	   	self.fields['user'].widget = forms.HiddenInput()
	   	self.fields['amt'].widget = forms.HiddenInput()
	   	self.fields['rack_cleared'].widget = forms.HiddenInput()
	   	self.fields['free_coffee'].widget = forms.HiddenInput()


	class Meta:
		model = Purchase
		widgets = dict(amt=Html5NumberInput({'required': True,'max':999,'min':0}))

class ItemForm(ModelForm):

	class Meta:
		model = Item



class ItemStockForm(ModelForm):

	def __init__(self, username=None, *args, **kwargs):    
   		super(ItemStockForm, self ).__init__(*args, **kwargs)
   
   		try:
   			if not username == None:
	   			self.fields['user'].queryset = User.objects.filter(pk=username.user.id)
   		except Exception, e:
   			raise ValueError("No username supplied. %s" % e)

   		self.fields['user'].widget = forms.HiddenInput()

	class Meta:
		model = ItemStock
		widgets = {
            'stock_status': Html5RangeInput({'required': True, 'min': 0, 'max': 11, 'data-highlight': True}),
        }