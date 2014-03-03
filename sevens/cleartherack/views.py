# Create your views here.
import datetime

from django.shortcuts import render_to_response as render, HttpResponseRedirect, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt
from django.core.context_processors import csrf
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
import redis, simplejson
from redis.exceptions import DataError as InvalidData, ConnectionError, InvalidResponse
from cleartherack.models import Item, ItemStock, Purchase
from cleartherack.forms import PurchaseForm, ItemStockForm, ClearTheRackForm, CoffeeForm, ComTripForm
from django.db.models import Avg, Sum, Max, Min, Count

@login_required(login_url='/apps/sevens/login/')
def dashboard(request,template_name="base.html"):
	context = {}

	start_date = datetime.datetime.now() - datetime.timedelta(hours=2)
	end_time = datetime.datetime.now()

	stock = ItemStock.objects.filter(entry_date__range=(start_date,end_time)).order_by('-entry_date')

	context['reports'] = stock

	try:
		rack = Purchase.objects.filter(rack_cleared=True).latest('purchase_date')
		context['rack_data'] = rack
	except:
		pass

	return render(template_name, context, context_instance=RequestContext(request))

@login_required(login_url='/apps/sevens/login/')
def purchase(request,template_name="purchase.html"):
	context = {}

	form = PurchaseForm(data=request.POST or None,username=request,initial={'user':request.user})
	
	if form.is_valid():
		try:
			form.save()
			form = PurchaseForm(initial={'user':request.user})
			context['success'] = "SUCCESS! Saved the purchase!"
		except Exception, e:
			context['error'] = "Could not save the Form. %s" % e

	context['form'] = form

	return render(template_name, context, context_instance=RequestContext(request))

@login_required(login_url='/apps/sevens/login/')
def cleartherack(request,template_name="cleartherack.html"):
	context = {}

	form = ClearTheRackForm(data=request.POST or None,username=request,initial={'user':request.user,'cleartherack':True})

	if form.is_valid():
		try:
			form.save()
			form = ClearTheRackForm(initial={'user':request.user})
			context['success'] = "SUCCESS! Saved the purchase!"
		except Exception, e:
			context['error'] = "Could not save the Form. %s" % e

	context['form'] = form


	return render(template_name, context, context_instance=RequestContext(request))

@login_required(login_url='/apps/sevens/login/')
def leaderboard(request,template_name="leaderboard.html"):
	context = {}

	def get_user_trips(request,howmany=7,alltime=False):
		start_date = datetime.datetime.now() - datetime.timedelta(days=howmany)
		end_date = datetime.datetime.now()
		if not alltime:
			return Purchase.objects.filter(user=request.user,purchase_date__range=(start_date,end_date)).count()
		else:
			return Purchase.objects.filter(user=request.user).count()

	def get_user_spending(request,howmany=7,alltime=False):
		start_date = datetime.datetime.now() - datetime.timedelta(days=howmany)
		end_date = datetime.datetime.now()
		if not alltime:
			return Purchase.objects.filter(user=request.user,purchase_date__range=(start_date,end_date)).aggregate(Sum('amt'))
		else:
			return Purchase.objects.filter(user=request.user).aggregate(Sum('amt'))

	def get_user_coffee(request,howmany=7,alltime=False):
		start_date = datetime.datetime.now() - datetime.timedelta(days=howmany)
		end_date = datetime.datetime.now()
		if not alltime:
			return Purchase.objects.filter(user=request.user,purchase_date__range=(start_date,end_date),free_coffee=True).count()
		else:
			return Purchase.objects.filter(user=request.user,free_coffee=True).count()

	def get_user_comtrips(request,howmany=7,alltime=False):
		start_date = datetime.datetime.now() - datetime.timedelta(days=howmany)
		end_date = datetime.datetime.now()
		if not alltime:
			return Purchase.objects.filter(user=request.user,purchase_date__range=(start_date,end_date)).exclude(com_trip=False).count()
		else:
			return Purchase.objects.filter(user=request.user,com_trip=True).count()

	def get_user_rackclears(request,howmany=7,alltime=False):
		start_date = datetime.datetime.now() - datetime.timedelta(days=howmany)
		end_date = datetime.datetime.now()
		if not alltime:
			return Purchase.objects.filter(user=request.user,purchase_date__range=(start_date,end_date),rack_cleared=True).count()
		else:
			return Purchase.objects.filter(user=request.user,rack_cleared=True).count()

	def get_all_rackclears(request,howmany=7,alltime=False):
		start_date = datetime.datetime.now() - datetime.timedelta(days=howmany)
		end_date = datetime.datetime.now()
		if not alltime:
			return Purchase.objects.filter(purchase_date__range=(start_date,end_date),rack_cleared=True).count()
		else:
			return Purchase.objects.filter(rack_cleared=True).count()

	def get_all_comtrips(request,howmany=7,alltime=False):
		start_date = datetime.datetime.now() - datetime.timedelta(days=howmany)
		end_date = datetime.datetime.now()
		if not alltime:
			return Purchase.objects.filter(purchase_date__range=(start_date,end_date)).exclude(com_trip=False).count()
		else:
			return Purchase.objects.all().exclude(com_trip=False).count()

	def get_all_trips(request,howmany=7,alltime=False):
		start_date = datetime.datetime.now() - datetime.timedelta(days=howmany)
		end_date = datetime.datetime.now()
		if not alltime:
			return Purchase.objects.filter(purchase_date__range=(start_date,end_date)).count()
		else:
			return Purchase.objects.all().count()

	def get_all_spending(request,howmany=7,alltime=False):
		start_date = datetime.datetime.now() - datetime.timedelta(days=howmany)
		end_date = datetime.datetime.now()
		if not alltime:
			return Purchase.objects.filter(purchase_date__range=(start_date,end_date)).aggregate(Sum('amt'))
		else:
			return Purchase.objects.all().aggregate(Sum('amt'))

	def get_all_coffee(request,howmany=7,alltime=False):
		start_date = datetime.datetime.now() - datetime.timedelta(days=howmany)
		end_date = datetime.datetime.now()
		if not alltime:
			return Purchase.objects.filter(purchase_date__range=(start_date,end_date)).exclude(free_coffee=False).count()
		else:
			return Purchase.objects.filter(free_coffee=True).count()

	def get_avg_spending(request,howmany=7,alltime=False):
		start_date = datetime.datetime.now() - datetime.timedelta(days=howmany)
		end_date = datetime.datetime.now()
		if not alltime:
			return Purchase.objects.filter(amt__gt=0,purchase_date__range=(start_date,end_date)).aggregate(Avg('amt'))
		else:
			return Purchase.objects.filter(amt__gt=0).aggregate(Avg('amt'))



	def miles_walked(trips):
		FEET_TO_711 = 1524
		return int(trips * 1524)
	try:
		context['user_spent_seven'] = get_user_spending(request,7)
		context['user_spent_thirty'] = get_user_spending(request,30)
		context['user_spent_year'] = get_user_spending(request,365)
		context['user_spent_all'] = get_user_spending(request,0,True)

		context['user_trips_seven'] = get_user_trips(request,7)
		context['user_trips_thirty'] = get_user_trips(request,30)
		context['user_trips_year'] = get_user_trips(request,365)
		context['user_trips_all'] = get_user_trips(request,0,True)

	
		context['user_feet_walked_total'] = miles_walked(context['user_trips_all'])
		context['user_yards'] = "%.3f" % float(context['user_feet_walked_total']/3.00)
		context['user_miles'] = "%.6f" % float(context['user_feet_walked_total']/5280.00)
		context['user_to_moon'] = "%.9f" % float( context['user_feet_walked_total']/(float(238700)*float(5280)))

	
		context['user_free_coffee'] = get_user_coffee(request,0,True)
		context['user_com_trips'] = get_user_comtrips(request,0,True)
		context['user_rack_clears'] = get_user_rackclears(request,0,True)

		context['all_spend_seven'] = get_all_spending(request,7)
		context['all_spend_thirty'] = get_all_spending(request,30)
		context['all_spend_year'] = get_all_spending(request,365)
		context['all_spend_all'] = get_all_spending(request,0,True)

		context['all_trips_seven'] = get_all_trips(request,7)
		context['all_trips_thirty'] = get_all_trips(request,30)
		context['all_trips_year'] = get_all_trips(request,365)
		context['all_trips_all'] = get_all_trips(request,0,True)

		context['all_rackclears'] = get_all_rackclears(request,0,True)
		context['all_com_trips'] = get_all_comtrips(request,0,True)
		context['all_free_coffee'] = get_all_coffee(request,0,True)

		context['avg_spending_7'] = get_avg_spending(request,7)
		context['avg_spending_30'] = get_avg_spending(request,30)
		context['avg_spending_365'] = get_avg_spending(request,365)
		context['avg_spending_all'] = get_avg_spending(request,7,True)

		context['avg_spending_7']   = "%.2f" % context['avg_spending_7']['amt__avg']
		context['avg_spending_30']  = "%.2f" % context['avg_spending_30']['amt__avg']
		context['avg_spending_365'] = "%.2f" % context['avg_spending_365']['amt__avg']
		context['avg_spending_all'] = "%.2f" % context['avg_spending_all']['amt__avg']

		context['all_feet_walked_total'] = miles_walked(context['all_trips_all'])
		context['all_yards'] = "%.3f" % float(context['all_feet_walked_total']/3.00)
		context['all_miles'] = "%.6f" % float(context['all_feet_walked_total']/5280.00)
		context['all_to_moon'] = "%.9f" % float( context['all_feet_walked_total']/(float(238700)*float(5280)))
	except:
		pass

	return render(template_name, context, context_instance=RequestContext(request))

@login_required(login_url='/apps/sevens/login/')
@csrf_exempt
def coffeerun(request,template_name="coffeerun.html"):
	context = {}

	if request.method == 'POST':
		try:
			purchase_obj = Purchase(user=request.user,com_trip=False,free_coffee=True,amt=0)
			purchase_obj.save()
			return HttpResponse("Saved!")
		except Exception, e:
			return HttpResponse("Error! Could not save. %s" % e)

	return render(template_name, context, context_instance=RequestContext(request))

@login_required(login_url='/apps/sevens/login/')
@csrf_exempt
def ComTrip(request,template_name="comtrip.html"):
	context = {}

	if request.method == 'POST':
		try:
			purchase_obj = Purchase(user=request.user,com_trip=True,free_coffee=False,amt=0)
			purchase_obj.save()
			return HttpResponse("Saved!")
		except Exception, e:
			return HttpResponse("Error! Could not save. %s" % e)

	return render(template_name, context, context_instance=RequestContext(request))

@login_required(login_url='/apps/sevens/login/')
def status(request,template_name="status.html"):
	context = {}

	form = ItemStockForm(data=request.POST or None,username=request,initial={'user':request.user})


	if form.is_valid():
		try:
			form.save()
			form = ItemStockForm(initial={'user':request.user})
			context['success'] = "SUCCESS! Added your update! Thanks!"
		except Exception, e:
			context['error'] = "Could not log your update. Please try again. %s" % e

	context['form'] = form
	return render(template_name, context, context_instance=RequestContext(request))


def seven_login(request,template_name="login.html"):
    context = {}
    context.update(csrf(request))
    next = None

    if request.user.is_authenticated():
    	logout(request)

    try:
    	next = request.GET['next']

    except:
    	next = "/app/"



    auth_frm = AuthenticationForm(data=request.POST or None)
    context['form'] = auth_frm

    if auth_frm.is_valid():
    	try:
        	user = authenticate(username=auth_frm.cleaned_data['username'], password=auth_frm.cleaned_data['password'])
        	login(request, user)
    	except Exception, e:
    		pass

        return redirect('/apps/sevens/app')

    return render(template_name, context, context_instance=RequestContext(request))


@login_required(login_url='/apps/sevens/login/')
def seven_logout(request,template_name="login.html"):
    context = {}
    try:
        context['do_not_show_menu'] = True
        logout(request)
        return redirect("/apps/sevens/login/")
    except:
        pass

	return render(template_name, context, context_instance=RequestContext(request))
