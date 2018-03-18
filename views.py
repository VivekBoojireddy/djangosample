from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, render
from django.template import RequestContext
from django.db.models import Q
from django.http import HttpResponse

from .models import *

def main(request):
	shoes = ShoeDetails.objects.all()
	paginator = Paginator(shoes, 5)
	try: page = int(request.GET.get("page", '1'))
	except ValueError: page = 1
	try:
		shoes = paginator.page(page)
	except (InvalidPage, EmptyPage):
		shoes = paginator.page(paginator.num_pages)

	brands = list(set([shoe_.brand for shoe_ in shoes]))

	return render_to_response("app/list.html",
							   dict(shoes=shoes, user=request.user, brands=brands),
							   context_instance=RequestContext(request))

def search(request):
	gender = request.POST.get('gender')
	brand = request.POST.get('brand')
	if  gender and brand:
		shoes = ShoeDetails.objects.filter(Q(gender=gender) & Q(brand=brand))
	elif gender and not brand:
		shoes = ShoeDetails.objects.filter(gender=gender)
	elif brand and not gender:
		shoes = ShoeDetails.objects.filter(brand=brand)
	else:
		shoes = ShoeDetails.objects.all()
	paginator = Paginator(shoes, 5)
	try: page = int(request.GET.get("page", '1'))
	except ValueError: page = 1
	try:
		shoes = paginator.page(page)
	except (InvalidPage, EmptyPage):
		shoes = paginator.page(paginator.num_pages)

	brands = list(set([shoe_.brand for shoe_ in ShoeDetails.objects.all()]))
	
	return render_to_response("app/list.html",
							  dict(shoes=shoes, user=request.user, brands=brands),
							  context_instance=RequestContext(request))

def buy(request):
	import pdb
	pdb.set_trace()
	data = [i for i in request.POST]
	sum_ = 0
	obj_list = []
	for dat in data:
		try:
			obj = ShoeDetails.objects.get(name=dat)
		except:
			continue
		obj_list.append(obj)
		sum_ = sum_ + obj.price
	return render_to_response('app/buy.html',
							  dict(obj_list=obj_list, sum_=sum_),
							  context_instance=RequestContext(request))

def proceed(request):
	return HttpResponse('Payment Gateway is not ready... Thanks')

