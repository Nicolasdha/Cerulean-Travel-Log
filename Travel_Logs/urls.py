'''Defines URL Patterns for Travel_Logs'''

from django.urls import path

from . import views

app_name = 'Travel_Logs'
urlpatterns = [
	# Home Page
	path('', views.index, name='index'),
	# Show all locations
	path('locations/', views.locations, name='locations'),
	# Detail page for a single location
	path('locations/<int:location_id>/', views.location, name='location'),
	# Adding new location page
	path('new_location/', views.new_location, name='new_location'),
	# Adding a new entry page
	path('new_entry/<int:location_id>/', views.new_entry, name='new_entry'),
	# Editing entries
	path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
	# Practice
	path('practice/', views.practice, name='practice'),
]
