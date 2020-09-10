from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import Location, Entry
from .forms import LocationForm, EntryForm

def practice(request):
	'''show a single topic and all of its entries'''
	return render(request, 'Travel_Logs/practice.html')

# Create your views here.
def index(request):
	return render(request, 'Travel_Logs/index.html')

@login_required
def locations(request):
	""" Show all locations"""
	locations = Location.objects.filter(owner=request.user).order_by('date_added')
	context = {'locations':locations}
	return render(request, 'Travel_Logs/locations.html', context)
	
@login_required
def location(request, location_id):
	'''show a single topic and all of its entries'''
	location = get_object_or_404(Location, id=location_id)
	check_location_owner(request, location_id)
	entries = location.entry_set.order_by('-date_added')
	context = {'location':location, 'entries':entries}
	return render(request, 'Travel_Logs/location.html', context)

@login_required
def new_location(request):
	""" Add a new location"""
	if request.method != 'POST':
		form = LocationForm()
	else:
		form = LocationForm(data=request.POST)
		if form.is_valid():
			new_location = form.save(commit=False)
			new_location.owner = request.user
			new_location.save()
			return HttpResponseRedirect(reverse('Travel_Logs:locations'))
	context = {'form':form}
	return render(request, 'Travel_Logs/new_location.html', context)

@login_required
def new_entry(request, location_id):
	""" Add a new entry for a location"""
	location = Location.objects.get(id=location_id)
	check_location_owner(request, location_id)
	if request.method != 'POST':
		form = EntryForm()
	else:
		form = EntryForm(data=request.POST)
		if form.is_valid():
			new_entry = form.save(commit=False)
			new_entry.location = location
			new_entry.save()
			return HttpResponseRedirect(reverse('Travel_Logs:location' , args=[location_id]))
	context = {'location': location, 'form':form}
	return render(request, 'Travel_Logs/new_entry.html', context)

@login_required
def edit_entry(request, entry_id):
	'''Edit exsisting entry'''
	entry = Entry.objects.get(id=entry_id)
	location = entry.location
	if location.owner != request.user:
		raise Http404
	if request.method != 'POST':
		form = EntryForm(instance=entry)
	else:
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
		return HttpResponseRedirect(reverse('Travel_Logs:location', args=[location.id]))
	context = {'entry':entry, 'location':location, 'form':form}
	return render(request, 'Travel_Logs/edit_entry.html', context)

def check_location_owner(request, location_id):
	location = Location.objects.get(id=location_id)
	if location.owner != request.user:
		raise Http404



