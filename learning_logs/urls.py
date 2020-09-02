'''Defines URL Patterns for learning_logs'''

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
	# Home Page
	path('', views.index, name='index'),
	# Show all topics
	path('locations/', views.topics, name='topics'),
	# Detail page for a single topic
	path('topics/<int:topic_id>/', views.topic, name='topic'),
	# Adding new topic page
	path('new_topic/', views.new_topic, name='new_topic'),
	# Adding a new entry page
	path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
	# Editing entries
	path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
	# Practice
	path('practice/', views.practice, name='practice'),
]
