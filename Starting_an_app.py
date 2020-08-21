# To create make dir in terminal python3 -m venv VARIABLE_env
# activate: source VARIABLE_env/bin/activate - 'deactivate' when done
# install DJ pip3 install Django - upgrade pip -/Users/sankp001/Desktop/Pizzaria/poop_env/bin/python3 -m pip install --upgrade pip
# create django proj - django-admin.py startproject pizzaria .    -> ls -> ls pizzaria
# create DB - python manage.py runserver




# A Django project is organizes as a group of individual apps that work together to make the project work

# For the data in the app each user will create a number of topics in their learning log
# and add enteries to the topics and have a time stamp to tell when they entered

## open models.py already exsisting folder and look at its existing content
# a model tells DJ how to work with data stored in app, it is just a Class - has attribtues and methods
# just like every other class 

from django.db import models

class Topic(models.Model):
# Topic inherts from Model, a parent class included in Django that defines basic functionality of a model
	''' A topic user is learning about'''
	text = models.CharField(max_length=200) # text attribute - data made up of txt/# - when define a 
	# CharField in django have to tell it how much space it should reserve in the database - maxlen

	date_added = models.DateTimeField(auto_now_add=True) #this is a DataTimeField - a piece of data
	# that will record a date and time - we pass the argument auto_add_now=True which tells Django
	# to automatically set this attribute to the current date and time when user creates a topic

	def __str__(self):
		'''Return a string representation of the model'''
		return self.text
	# Need to tell DJ which attribute to use by default when it displays info about a topic, use the 
	# method aboce to display a simple representation of a model that returns the string stored in 
	# the text attribute



## ACTIVATING MODELS
# To use our models we need to tell DJ to include our app in the overall project, go to settings.py
# in learning_log dir and see the tuple that tells Django which apps work togehter to make up the
# project - add our app to the Tuple by modifying INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # My apps
    'learning_logs',
]

# in the 11_env need to tell DJ to modify DB so it can store info

# Need to tell Django to modify the database so it can store information realted to the model Topic\
# in terminal this tells DJ to figure out how to modify the DB so it can store data, created migration
# file 0001_initial.py - will create a table for the model topic in DB
python manage.py makemirgations learning_logs

# Now apply the migration and have DJ modify the DB
python manage.py migrate


# Whenever we want to modify the data that Learning Log manages we follow three steps
# 1. modify models.py
# 2. call makemirgations on learning_logs
# 3. tell DJ to migrate the project

# When you define models for an app, DJ makes it easy for you to work with your models through the 
# ADMIN SITE - a site's admins use not the general users
# Creating a user who has all priviges available on the site is a - SUPERUSER
# A privilige controls the actions a user can take - the most restrictive privilige 
# settings allow a user to only read public info - registered users typically have the privilige of reading
# their own prvt data and some info avilable to members - to effectivly administer a web app
# the site owner usually needs access to all info
## TO CREATE A SUPERUSER IN TERMINAL
python manage.py createsuperuser

# Passwords are stored as HASHS - so if attacked the attackers can get the HASH not the PASS

## REGISTERING A MODEL WITH THE ADMIN SITE
# when created learning_logs app DJ created a file admin.py in same dir as models.py - INSIDE ADMIN.PY
from django.contrib import admin

# Register your models here.
# To register Topic with the admin site
from learning_logs.models import Topic # imports the model we want to register - topic
admin.site.register(Topic) # uses admin.site.register() to tell DJ to manage model thru admin site 

# In a internet browser enter
http://localhost:8000/admin/ # enter user/pass - can add new user/groups and change existing
# Can also work with data related to the Topic model we just defined
# Need to have Django SERVER RUNNING - python manage.py runserver

## ADDING TOPICS TO REGISTERED MODEL TOPICS
# In webpage cick topics and click add - enter Chess and save - same with Rock Climbing - save
# to record what youve been learning about chess/rock climbing need to define a model for the
# kinds of enteries users can make in their learning logs. Each entry needs to be associated with 
# a particular established topic - this is called a MANY-TO-ONE RELATIONSHIP meaning many entries
# can be associated with this one topic
# Open models.py and code for Entry model = 

class Entry(models.Model): # Inherits from DJ model class
	'''Something specific learned about a topic'''
	topic = models.ForeignKey(Topic)
# The first attribute of this class is topic it is a ForeignKey instance
# A ForeignKey is a database term: its a reference to another record in the DB. This is the code that
# connects each entry to a specific topic. Each topic is assigned a key or ID when created
# when DJ establishes a connection between two pieces of data it uses the key associated with each 
# piece of information - use these connections to retrieve all the entries associated with a Topic

	text = models.TextField()
# This is an instance of the text field - no limit. 

	date_added = models.DateTimeField(auto_now_add=True)
# This is so we are able to present the entries in order of creation and place timestamp

	class Meta:
		verbose_name_plural = 'entries'
# Nested Meta class - Meta holds xtra info for manageing a model, here it allows us to set 
# a special attribute telling DJ to use the word 'Entries' when it needs to refer to more than one entry
# W/O this DJ would refer to multiple entries as 'Entrys'

	def __str__(self):
		'''return a string rep of the model'''
		return self.text[:50] + "..."
# This __str__() method tells DJ which information to show when it refers to individual
# entries. B/C entries are long bodies of txt we tell DJ to just show the first 50 letters + ...
# Whenever we want to modify the data that Learning Log manages we follow three steps
# 1. modify models.py
# 2. call makemirgations on learning_logs
# 3. tell DJ to migrate the project
python manage.py makemigrations learning_logs #results in 0002_entry
python manage.py migrate

## Also need to register the Entry model in the admin.py to complete it so it looks like this now:
from django.contrib import admin

# Register your models here.
from learning_logs.models import Topic, Entry
admin.site.register(Topic)
admin.site.register(Entry)

# Refresh site and see Entries - add entry to chess and rock climbing

## THE DJANGO SHELL
# Can examine the data of the entries programmatically through an interactive terminal session
# The interactive environment is called the Django SHELL, great environment for testing and
# troubleshooting your project. Code for Terminal while in virtual env
python manage.py shell
from learning_logs.models import Topic
Topic.objects.all()
topics = Topic.objects.all() # storing the query set in the variable topics
for topic in topics:
	print(topic.id, topic)
	# 1 Chess
	# 2 Rock Climbing
# once you know the ID of a particualr object you can get that object and examine any attribute
# the object has - looking at text and date_added_values for Chess:
 t = Topic.objects.get(id=1)
 t.text
 t.date_added
#'Chess'
#datetime.datetime(2020, 8, 13, 20, 21, 50, 282257, tzinfo=<UTC>)

# Can also look at entries related to topics, we defined the topic attribute for the Entry model
# ForeignKey = a connection between entry and topic, DJ uses this to get every entry related to a topic
t.entry_set.all()
 ->>>> <QuerySet [<Entry: The opening is the first part of the game, roughly...>, <Entry: In the opening phase of the game, it is important ...>]>
# to get data thru a foreign key realtionship - use lowercase name of related model followed by an 
# underscore and the word SET - my_pizza = t toppings = entry - my_pizza.toppings_set.all()
# Use this kind of syntax when we begin to code the pages users can request - The shell is useful
# for this to see if it gets the code you want - if it works in the shell it will work outside of it
# easier to troubleshoot in shell env than within the files that generate web pages
# will need to reboot shell every change made to see - ctrl-D and Enter

# Ususally making web pages with DJ is 3 stages. 1: defining URLs, 2: writing views, 3: writing templates

# 1. Must define patterns for a URL, a URL pattern describes the way the URL is laid out and tells 
# DJ what to look for when matching a browser request with a site URL so knows which page to return

# 2. Each URL then maps to a particular view- the view function retrives and processes the data 
# needed for that page.

# 3. The view function often calls a template, which builds a page that a browser can read

## MAKE A HOME PAGE FOR LEARNING LOG
# Will define URL for the home page, write its view function and create a simple template
# will keep the page simple to make sure it works like it supposed to - a functioning web app
# is fun to stylize when complete. Home page will have a title and description

## MAPPING A URL - first will need the home page URL, base URL to access project
# at the moment the base URL is localhost.8000/ and returns the default DJ site to let you know
# the project was set up correctly - will MAP THE BASE URL TO learning logs homepage

# in the URL folder of learning_log is has this
###_------------oldoldold old old old----------
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]
# and then it turns to this
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('learning_logs.urls')),
]
# The include function is imported from dj.urls since the new URL routing doesnt require regular expressions
# so we dont need a ^ at the beginning - The body of the file defines the variable urlpatterns
# that includes sets of urls from the apps in the project - the admin.site.urls is a module
# which defines all the URLs that can be requested from the admin site - adding the include to 
# include the module learning_logs.urls 
# Need to make a completely new file in learning_logs folder urls.py

'''Defines URL Patterns for learning_logs'''
from django.urls import path
from . import views
app_name = 'learning_logs'
urlpatterns = [
	# Home Page
	path('', views.index, name='index'),
]

# The string above helps differentiate urls.py, we import the path function needed when mapping
# URLs to views, and also import the views module. The dot notation '.' tells python to import views
# from the same dir that urls.py is in. The empty quotes are replacement for regex and to tell python
# the find the beginning/end of the string for the URL with nothin inbetwen since python ignores the 
# current URL localhost:8000/ so empty quotes(old regex) matches the base URL. Any other URL will
# not match these empty quotes and DJ will return an error if the URL requested doesnt match
# any existing URL patterns - the second argument specificies the view function to call. When a 
# requested URL matches the empty quotes(regex) DJ will call views.index, and the their argument
# provides the name as index for this URL pattern so we can refer to it in other sections of code 
# whenever we want a link to the home page we will use this name instead of writing out the URL

## WRITING THE VIEW FUNCTION
# A view function takes in info from a request, prepares the data needed to generate a page, and then
# sends the data back to the browser often by the using a template that defines what the page looks like
# views.py was auto genned when set-up proj

from django.shortcuts import render
# the render function renders the response based on the data provided by views
# Create your views here.
# This is how the code for the VIEW for the home page should be written

def index(request):
	'''The home page for the learning logs'''
	return render(request, 'learning_logs/index.html')
# When a URL request matches the pattern defined in the variable urlpatterns in urls.py
#, DJ will look for a function called index() in the views.py file. DJ than passes the request 
# object to this view function. In this case we dont need to process any data for the page, 
# so only the code in the funtion is a call to render(). The Render() function here uses two arguments-
# 1. the original request object 2. a template it can use to build the page

## WRITING A TEMPLATE
# A template sets up the structure for a webpage. The template defines what the page should looks like,
# and DJ filles in the relevant data each time the page is requested. A template allows you
# to access any data provided by the view. B/c our view for the home page provided no data, 
# the template is simple - inside learning_logs make a templates folder and another folder learning_logs
# inside that one, seems redundant but it sets up a structure that DJ can interp unambigously, even
# in the conext of a large project containing many individual apps. Inside the innder learning_logs
# folder make a new file called index.html and write
<p> Learning Log</p>
<p> Learning log helps you keep track of your learning, for any topic you're learning about.</p>
# Written in HTML with two paragraphs - now when we request the projects base URL (localhost) we'll 
# see the page we just built instead of the default DJ page. DJ will take the requested URL, and that
# URL will match the pattern '' then DJ will call the function views.index() and this will render
# the page using the template contined in index.html 

### BUILDING ADDITIONAL PAGES
# Start to build out the project, make a page that lists all topics, a page that shows all entries 
# for a topic - for each of these pages we'll specify a URL pattern, write a view function, and template
# before this we will create A BASE TEMPLATE that all templates in this project inherit from

## TEMPLATE INHERITANCE
# When creating a web page you almost always rqure some elements to be repeated on each page
# rather than writing these elements in each page we write a base template containing the repeated
# elements and then have each page inherit from the template - this allows you to save time and focus
# on the unique info per page and so much easier to change the overall look and feel of the project

## THE PARENT TEMPLATE------------------
# Start by creating template called base.html. the only element we want to repeat on each page
# right now is the title at the top - b/c we'll include this template on every page need to make the
# title a link to the home page: crease base.html IN THE SAME DIR AS INDEX.HTML

<p>
<a href = "{% url 'learning_logs:index' %} " > Learning Log </a>
</p>
# This first part creates a para containing the name of the project which also acts as a link
# to the home page - to generate the link we use a TEMPLATE TAG - indicated by braces and percent signs
# {% %}. A template tag is a bit of code that generates information to be displayed on a page.

# In this example, the template tag {% url 'learning_logs:index' %} generates a URL matching the URL
# pattern defined in learning_logs/urls.py with the name 'index'
# in this learning_logs is the namespace and index is a uniquly named URL pattern in that namespace.

{% block content %}{% endblock content %}
# Insert a pair of block tags, this block named content is a placeholder; the child template will
# define the kind of information that goes in the content block


# In a simple HTML page, a link is surrounded by the anchor tag
<a href="link_url">link text>/a>
# but having a template tag generate the URL for us makes it much easier to keep our links up to date
# when you need to update you dont have to find each anchor you can just change the URL pattern in 
# urls.py and DJ will auto insert the updated URL 
# every page in the project will inherit from the base page so every page will have a link back to the
# base page

## THE CHILD TEMPLATE -------------------
# Now we need to rewrite index.html to inherit from base.html 
### ------------ OLD OLD OLD OLD -------
<p> Learning Log</p>
<p> Learning log helps you keep track of your learning, for any topic that you're learning about</p>

# ------- NEW NEW NEW NEW
{% extends "learning_logs/base.html" %}
# This code reaplaces the Learning Log title with the code for inheriting from a parent template 

{% block content %}
	<p> Learning log helps you keep track of your learning, for any topic that you're learning about</p>
{% endblock content}
# A Child Template must have an {% extends %} tag on the first line to tell DJ which parent template
# to inherit from . The file base.html is part of learning_logs so we inclde that in the path to the 
# parent template. The line pulls in eveything contained in the base.html template and allows index.html
# to define what does in the space reserved by the content block
# Define the content block by inserting {% block %} tag with the name content - everything we arnt 
# inheriting from the parent goes in this block and ends with the end tag{% endblock content %}

# when working with parent templates all you need to do is modify the element in the parent and
# it will be carried out over all the child templates (possible 100s) and make it a lot easier

# In common large projects, its common to have one parent temp called base.html for entire site
# and parent templates for each major section of the site. all section templates inherit from base.html
# and each page in site inherits from a section template. easy to modify look and feel of any section
# or inidivual page

## THE TOPICS PAGE -------
# Now with an efficent approach to building pages can focus on the general topics page and the page
# to display entries for a single topic. General page will show all topics that users have created,
# and it is the first page that will involve working with data

## THE TOPICS URL PATTERN
# first we define the URL for the topics page, it is common to choose a simple URL fragment that reflect
# the kind of info presented on the page. We'll use the word topics, so the URL
# http://localhost:8000/topics/ will return this page - need to modify learning_logs/urls.py
from django.urls import path
from . import views

app_name = 'learning_logs'
urlpatterns = [
	# Home Page
	path('', views.index, name='index'),

	# page that shows all topics
	path('topics/', views.topics, name='topics')
]
# added topics to the beginning argument of the path() function adds topics/ to the homepage URL
# When DJ examines a requested URL this pattern will match any URL that has the base URL + topics.
# you can omit the forward slash at the end but there cant be anything after topics or the pattern
# wont match. Any request with a URL that matches this pattern will then be passed to the 
# function topics() in views.py

## THE TOPICS VIEW
# The topics()(PLURAL) func needs to get some data from the database and send it to the template
# need to modify views.py

from django.shortcuts import render
from .models import Topic 
# import the model associated with the data we need - Topic class in models.py

# Create your views here.
def index(request):
	return render(request, 'learning_logs/index.html')

def topics(request):
# needs the request parameter Django received from the server
	'''Shows all topics'''
	topics = Topic.objects.order_by('date_added')
# We query the database by asking for the Topic objects, sorted by date added attribute
# and store the resulting queryset in topics
	context = {'topics': topics}
# Here we define a context that we'll send to the template. A CONTEXT is a DICTIONARY in which the keys
# are names we'll use in the template to access the data and the values are the data we need to send
# to the template. In this case there is one key-value pair which contains the set of topics we'll
# display on the page. The topic html file receives this context so can use the data
	return render(request, 'learning_logs/topics.html', context)
# When building a page that uses data, we pass the context variable to render()
# as well as the request object and the path to the template

## THE TOPICS TEMPLATE
# The template for the topics page receives the context dictionary so the template can use the data
# that topics() provides - make a topics.html file in same dir as index.html
# here is how to display the topics in the template:

{% extends "learning_logs/base.html" %}
# start with the {%extends%} to tell to inherit from base.html with path to it

{% block content %} # start of unique web page inforamtion

	<p> Topics </p> # Create paragraph/header

	<ul># This is the tag for unordered list in HTML as bullet points - begin bullets here

	{% for topic in topics %}
# this is a template tag equivilant for a for loop, which loops thry the list of topics in the 
# context dictionary. the code used in templates differs from Python in important ways - python
# uses indentation to indicate part of a loop, in template notation every FOR LOOP needs explicit
# ending {% endfor %} tag to indicate the end of loop

		<li>{{topic}}</li>
# we want to turn each topic into an item in the bulletd list, to print vari in a template wrap
# the variable name in double braces. The code {{topic}} will be reaplced by the value of topic
# on each pass thru the loop, they indicate to DJ that we're using a template variable
# the html tag <li></li> indicates a list item. anything between these tags and the <ul></ul>
# tags will appear as a bulleted item in the list

	{% empty %}
# here use this code to tell DJ what to do if there are no items in the list, we print the message below
		<li> No topics have been added yet.</li>
		{% endfor %} # close the for loop out
	</ul> # close the unordered list out
{% endblock content} # ends the unique information in the webpage

# FOR LOOP IN TEMPLATE NOTATION
{% for item in list %}
	do something with each iteam
{% endfor %}

## EDIT BASE.HTML TO INCLUDE A LINK FOR TOPICS-----
# need to modify base template to include a link to the topics page - create 
<p>
	<a href = "{% url 'learning_logs:index' %} "> Learning Log </a> - 
# ADD a DASH to the end of the index
	<a href = "{% url 'learning_logs:topics' %} " > Topics </a>
# Add the topic a href to add that link to the page using the URL pattern with the name 
# 'topics' in learning_logs/urls.py
</p>

{% block content %}{% endblock content %}

## INDIVIDUAL TOPIC PAGES --------------------
# Next need to create a page that can focus on a single topic, showing the topic name and all the
# entries for that topic, again will modify the topics page so each bulleted item list can
# be clickable to that entry page

## TOPIC URL PATTERN -----
# The URL pattern for the topic page is going to change to use the topics id attibute to indicate
# which topis was requested - if user wants to see the detail page for the topic chess (id #1)
# the url will be http://localhost:8000/topics/1/, pattern to match this URL goes in 
# learning_logs/urls.py

'''Defines URL Patterns for learning_logs'''

from django.urls import path

from . import views

app_name = 'learning_logs'
urlpatterns = [
	# Home Page
	path('', views.index, name='index'),
	# Show all topics
	path('topics/', views.topics, name='topics'),
	# Detail page for a single topic
	path('topics/<int:topic_id>/', views.topic, name='topic'),
# the path() function uses the first argument for the value stored in the URL, when DJ finds a URL 
# that matches this pattern it calls the view function topics() with the value stored in 
# topid_id as an argument. Then use the value of topic id to the correct topic inside the function
]

## THE TOPIC VIEW -------- (SINGULAR - NEW VIEW FUNCTION)
# The topic() function in views.py needs to be modified to get the topic and all associated 
# entries from the database:
def topics(request):
	topics = Topic.objects.order_by('date_added')
	context = {'topics':topics}
	return render(request, 'learning_logs/topics.html', context)

def topic(request, topic_id): # NEW SINGULAR FUNC FOR A SINGLE TOPIC
# First function that required a parameter other than request - topic_id - the func accepts the value
# captured by the expression above and stores it in topic_id

	'''show a single topic and all of its entries'''
	topic = Topic.objects.get(id=topic_id)
# Use get() to retrieve the topic as we did in the DJ shell

	entries = topic.entry_set.order_by('-date_added')
# we get the entries associated with this topic, and order them by date_added: the minus
# sign infront of date added sorts results in reverse order which will display the most
# recent entries first 

	context = {'topic':topic, 'entries':entries}
# store topic and entries in the context dictionary

	return render(request, 'learning_logs/topic.html', context)
# send context to the template topic.html

# the variables topics and entries above are queries to the database for specific inforamtion
# when writing these queries you should do it in DJ shell first - alot easier and faster

## TOPIC TEMPLATE ---
# The template needs to display the name of the topic and the entries. We also need to inform the user
# if no entires have been made yet for this topic
# CREATE A NEW FILE TOPIC.HTML FOR THE NEW SINGULAR TOPIC TEMPLATE/PAGE

{% extends "learning_logs/base.html" %}
# extend this to inherit as all pages do
{% block content %}

	<p> Topic: {{topic}} </p>
# Topic is being displayed which is stored in the template variable {{topic}}
# this template variable is avilable because its included in the context dictionary

	<p> Entries: </p>
	<ul> # start bulleted list
	{% for entry in entries %}
# for loop to loop thru entries and show each one
		<li>
# each bullet will list two pieces of information: timestamp and full text of each entry
		<p> {{entry.date_added|date:'Md, Y H:i'}} </p>
# Timestamp we display the value of the attribute date_added. In DJ the vertical line '|'
# reps a TEMPLATE FILTER, a function that modifys the value in a template variable
# The filter date:M d, Y H:i' displays timestamps like January 1, 2015 23:00
		<p>{{entry.text|linebreaks}} </p>
# This displays the full line of text rather than just the first 50 characters from entry
# Included is a |linebreaks template filter that ensures that long text entries include
# line breaks in a format understood by browsers rather than showing a block of uniterrupted txt
		</li>
	{% empty %}
		<li>
			No topics have been added yet
		</li>
# This is just in case there is no entries, and to display something
	{% endfor %}
	</ul>
{% endblock content %}

##TOPICS(PLURAL) TEMPLATE further to each topic routes to the appropriate TOPIC page
#-------- OLD OLD OLD ------

{% extends "learning_logs/base.html" %}
{% block content %}
	<p> Topics </p>
	<ul>
		{% for topic in topics %}
			<li> {{topic}}</li>
		{% empty %}
			<li> No topics have been added yet</li>
		{% endfor %}
	</ul>
{% endblock content %}

### ----- NEW NEW NEW NEW -------

{% extends "learning_logs/base.html" %}
{% block content %}
	<p> Topics </p>
	<ul>
	{% for topic in topics %}
		<li> 
			<a href="{% url 'learning_logs:topic' topic.id %}">{{topic}}</a>
# Use URL template tag to generate the proper link, based on the URL pattern in 
# learning_logs with the name 'topic'. This URL pattern requires a topic_id arugment, so
# we add the attribute topic.id to the URL template tag. Now each topic in the list 
# of topics is a link to the topic page
		</li>
	{% empty %}
		<li>
			No topics have been added yet
		</li>
	{% endfor %}
	</ul>
{% endblock content %}



############ USER ACCOUNTS -------------------------

## ALLOWING USERS TO ENTER DATA - add new topic, entry, and edit previous ones

##------------------ ADDING NEW TOPICS
# Adding a form-based page works in much the same way as the pages we've already built:
# we define a URL, write a view function, write a template. One major difference is
# the addition of a new module called FORMS.PY which will contain the forms

## ---------- THE TOPIC MODELFORM-----
# Any page that lets a user enter and submit information on a web page is a form, even if
# it doesnt look like one. When users enter inforamtion, we need to validate that info
# if it is the right kind of data and nothing maliciousk such as code to interupt the server
# We then need to process and save information to the appropriate place in the database,
# DJ automates much of this work - The simplest way to build a form in DJ is to use
# a MODELFORM, which uses the inforamtion from the models defined above to auto build
# a form, write first FORM in the file forms.py created in the same dir as models.py
from django import forms # import forms
from .models import Topic # import model we are to work with Topic

class TopicForm(forms.ModelForm):
# Define a class TopicForm which inherits from forms.ModelForm - The simplest version
# of ModelForm conists of a nested Meta class telling DJ which model to base the form on 
# and which fields to include in the form
	class Meta:
		model = Topic
# Here we start building a form from the Topic model
		fields = ['text']
# include only the text field
		labels = {'text': ''}
# This tell DJ not to generate a label for the text field


## ------------------ THE NEW_TOPIC URL --------

# The URL for a new page should be short and descriptive, so when the user wants to add a
# new topic, we'll send them to http://localhost:8000/new_topic/ - here is the URL pattern
# for the new_topic page, which we add to learning_logs/urls.py
	# Home Page
	path('', views.index, name='index'),
	# Show all topics
	path('topics/', views.topics, name='topics'),
	# Detail page for a single topic
	path('topics/<int:topic_id>/', views.topic, name='topic'),
	# Adding new topic page
	path('new_topic/', views.new_topic, name='new_topic')
# This URL pattern will send requests to the view function new_topic()


## 	-=-=-=--=-==-=-=-=-=- new_topic() VIEW FUNCTION -=-=-=-=-=-
# The new_topic () func needs to handle 2 different situations: initial requests for the
# new_topic page(in which case it should show a blank form), and the processing of any
# data submitted in the form. It then needs to redirect user back to the topics page
###_----------------- old old olD OLD OLD ---=-=-=
from django.shortcuts import render
from .models import Topic
# Create your views here.
def index(request):
	return render(request, 'learning_logs/index.html')
def topics(request):
	""" Show all topics"""
	topics = Topic.objects.order_by('date_added')
	context = {'topics':topics}
	return render(request, 'learning_logs/topics.html', context)
def topic(request, topic_id):
	'''show a single topic and all of its entries'''
	topic = Topic.objects.get(id=topic_id)
	entries = topic.entry_set.order_by('-date_added')
	context = {'topic':topic, 'entries':entries}
	return render(request, 'learning_logs/topic.html', context)

## ------------------- NEW NEW NEW NEW --------
from django.shortcuts import render
from django.http import HttpResponseRedirect
# importing the class HttpResponseRedirect will redirect the render back to the topics page
# after they submit their topic
from django.urls import reverse
# The reverse() function determines the URL from a named URL pattern, meaning that DJ 
# will gnerate the URL when the apge is requested

from .models import Topic
from .forms import TopicForm
# import form we just wrote, TopicForm

# -- snip --
def new_topic(request):
	'''Add a new topic'''
	if request.method != 'POST':
		# No data submitted; create blank form
# This test determines whether request method is GET or POST.
# If the request method is not POST, the request is probably GET, so we need
# to return a blank form - if another type of req its still safe to return blank form
		form = TopicForm()
# Make an instance of TopicForm & store it in the vari form - b/c no arugments passed in
# TopicForm() when we make it the browser returns a blank form user and fill out
	else:
		# POST data submitted; process data
		form = TopicForm(data=request.POST)
# If the request method is POST the else block runs and processes the data submitted
# in the form. We make an instance of TopicForm store it in vari form and pass in
# the data entered by the user, stored in request.POST. The forms object thats 
# returned contains the inforamtion submitted by the user
		if form.is_valid():
# Cant save the submitted info in the DB until weve checked that it is valid
# the is_valid() func checks that all req fields have been filled in (all fields in a
# form are required by deafult) and that the data entered matches the field types
# expected - for example the text is less than 200 char, as specified in models.py
			form.save()
# If everything is valid we can call save() which writes the data from the form to the DB
			return HttpResponseRedirect(reverse('learning_logs:topics'))
# Once we've saved this data we can leave this page, We use the reverse() to get the URL
# for the topics page and pass the URL to HttpResponseRedirect which redirects the users
# browser to the topics page. On the topics page the user should see the topic entered
	context = {'form':form}
	return render(request, 'learning_logs/new_topic.html', context)
# Send the form to the template in the context dictionary. Because we included no
# arguments when instantiating TopicFrom, DJ creates a blank form that user can fill out


####------- GET AND POST RESQUESTS --------
# two main types of request to use when building web apps are GET and POST requests (actually caps)
# You use GET requets for pages that only read data from the server, usually use POST
# req when user needs to submit info through a form. We'll be specifying the POST method
# for processing all of our forms ( A few other kinds of requests exists but wont be using in this proj)
# The function new_topic() takes in the request object as a parameter. When the user
# initially requests this page, their browser will send a GET request. When user filled
# out and submitted the form, the browser will submit a POST request. Depending on the
# request, we'll know whether the user is requesting a blank form (a GET request)
# or asking us to process a completed form (a POST request)


## ----- need to make NEW_TOPIC TEMPLATE to display the form just made above
# Make a new template called new_topic.html to display the form we created above
{% extends "learning_logs/base.html" %}
# extends base.html so inherits from it
{% block content%}
	<p>Add a new topic:</p>
	<form action="{% url 'learning_logs:new_topic'%}" method='post'>
# Define an HTML form. The action argument tells the server where to send the data submitted
# in the form; in this case, we send it back to the view function new_topic().
# the method argument tells the browser to submit the data as a POST request

		{% csrf_token%}
# DJ uses this template tag to prevent attackers from using the form to gain unauthorized
# access to the server in a malicious action called CROSS-SITE REQUEST FORGERY 

		{{ form.as_p }}
# We display the form here, very simple code in DJ - only need to include the variable
# {{ form.as_p }} for DJ to create all the fields nessesary to display the form auto
# the as_p modifier tells DJ to render all the form elements in paragraph format
# which is a simple way to display the form neatly

		<button name = "submit">add topic</button>
# define a submit button for forms 
	</form>
{% endblock content %}


## ---------------------- LINKING TO NEW_TOPIC PAGE -----
# Next we include a link to the new_topic page on the topics page:
# go to topics.html then
{% extends "learning_logs/base.html" %}
{% block content %}
	<p> Topics </p>
	<ul>
	{% for topic in topics %}
		<li>
			<a href="{% url 'learning_logs:topic' topic.id%}">{{topic}}</a>
		</li>
	{% empty %}
		<li> 
			No topics have been added yet
		</li>
	{% endfor %}
	</ul>
	<a href ="{% url 'learning_logs:new_topic' %}"> Add a new topic:</a>
# 
{% endblock content %}


## ----- ADDING NEW ENTRIES -------------------
# Now users can create new topic so need to be able to make new entries. 
# Again, we will add another class to forms.py define a URL, write a view function
# and a template, and link to the page

# THE ENTRY MODELFORM --- Need to create a form associated with the Entry model, but this
# time with a litte more custimization thatn the TopicForm -in forms.py
#---------old old old oLD OLD OLLD------
from django import forms
from .models import Topic

class TopicForm(forms.ModelForm):
	class Meta:
		model = Topic
		fields = ['text']
		labels = {'text':''}

###------ NEW NEW NEW NEW =--==-==-=-=-
from django import forms
from .models import Topic, Entry
# import Entry class from models

class TopicForm(forms.ModelForm):
	class Meta:
		model = Topic
		fields = ['text']
		labels = {'text':''}

class EntryForm(forms.ModelForm):
# this new class inherits from forms.ModelForm and has a nested Meta class listing
# the model its based on and the field to include in the form
	class Meta:
		model = Entry
		fields = ['text']
		labels = {'text': ''}
# We again give the field 'text' a blank label
		widgets = {'text': forms.Textarea(attrs={'cols': 80})}
# Include widgets attribute here, a widget is an HTML form element, such as a 
# single-line text box, multi-line text area, or drop down list. By including
# the widgets attribute you can override DJ defualt widget chioces. By telling DJ
# to use a forms.Textarea element we're customizing the input widget for the field 'text'
# so the text area will be 80 columns wide instead of the default 40 giving more room

#### -------- THE NEW_ENTRY URL ----------
# Need to invlude a topic_id argument in the URL for adding a new entry, b/c the
# entry must be associated with a particular topic. Here's the URL, which we added
# to learning_logs/urls.py

urlpatterns = [
	# Home Page
	path('', views.index, name='index'),
	# Show all topics
	path('topics/', views.topics, name='topics'),
	# Detail page for a single topic
	path('topics/<int:topic_id>/', views.topic, name='topic'),
	# Adding new topic page
	path('new_topic/', views.new_topic, name='new_topic'),
	# Adding new entry page
	path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
]


## ---- THE new_entry() VIEW FUNCITON -=-=-=-==-=---=-=-
# This is much like the function for adding a new topic
from .models import Topic
from .forms import TopicForm, EntryForm
# import EntryForm form

def new_entry(request, topic_id):
# Has the topic_id parameter to store the value it receives from the URL
	'''add a new entry to a topic'''
	topic = Topic.objects.get(id=topic_id)
# We need the topic to render the page and process the form's data, so we use
# topic_id to get the correct topic object

	if request.method != 'POST':
		# No data submitted; create blank form
		form = EntryForm()
# check if request method is POST or GET. The if block executes if it is a GET request,
# and create a blank instance of EntryForm
	else:
		form = EntryForm(data=request.POST)
		# POST data submitted: process data
# If the request method is POST we process data by making an instanace of EntryForm,
# populated with the POST data from the request obejct
		if form.is_valid():
# check if the form is valid. If it is need to set the entry object's topic 
# attribute before saving it to the DB
			new_entry = form.save(commit=False)
# when call save() we include the argument commit=False to tell DJ to create a new
# entry object and store it in new_entry without saving it to the DB yet 
			new_entry.topic = topic
# set new_entry's topic attribute to the topic we pulled from the DB at the beginning
# of the function
			new_entry.save()
# call save with no arguments that saves the entry to the DB with the correct associated topic
			return HttpResponseRedirect(reverse('learning_logs:topic',
													args=[topic_id]))
# redirect the userto the topic page. the reverse() call requires two arguments, the
# name of the URL pattern we want to generate a URL for and an args list containing
# any arguments that need to be included in the URL. The args list has one item in it
# topic_id, the HttpREsponseReedirect() call then redirects the user to the topic page
# they made an entry for, and should see the new entry in the list of entries
	context = {'form':form}
	return render(request, 'learning_logs/new_entry', context)


### --=-=-=- THE new_entry TEMPLATE =-=--==-=-=-=--=-
# similar to the template for this is similar to the new_topic temp - make new_entry.html
{% extends 'learning_logs/base.html' %}
# extend the base.html
{% block content %}

<p> <a href = "{% url 'learning_logs:topic' topic.id %}"> {{ topic }}</a></p>
# We show the topic at the top of the page so the user can see which topic theyre adding
# an entry to. This also acts as a link back to the main page for the topic

<p>Add a new entry:</p>
<form action="{% url 'learning_logs:new_entry' topic.id %}" method='post'>
# The form's action argument includes the topic_id value in the url so the view function
# can associate the new entry with the correct topic
	{% csrf_token %}
	{{ form.as_p }}
	<button name='submit'>add entry</button>
</form>

{% endblock content %}

### -------=-=-=--=-=- 	LINKING TO THE new_entry PAGE -------=-=-=-
# need to include a link to the new_entry page from each topic page - topic.html:
{% extends "learning_logs/base.html" %}

{% block content %}

	<p>Topic: {{topic}}</p>

	<p>Entries:</p>
	<p>
		<a href= "{% url 'learning_logs:new_entry' topic.id%}">add new entry</a>
	</p>
# Add the link above before showing the entries b/c adding a new entry will be the
# most common action on this page - now can 
	<ul>
	{% for entry in entries %}
		<li>
		<p>{{ entry.date_added|date:'M d, Y H:i'}} </p>
		<p>{{ entry.text|linebreaks}}</p>
		</li>
## --snip--


## ----=-=--= EDITING ENTRIES -=-=-=-=-
# The URL for the page needs to pass the ID of the entry to be edited - urls.py
	path('new_topic/', views.new_topic, name='new_topic'),
	# Adding a new entry page
	path('new_entry/<int:topic_id>/', views.new_entry, name='new_entry'),
	# Page for editing entries
	path('edit_entry/<int:entry_id>/', views.edit_entry, name='edit_entry'),
# The ID passed in the URL (localhost:8000/edit_entry/1) is stored in the parameter 
# entry_id. The URL pattern sends requests that match this format to the view 
# function edit_entry()

### -----EDIT_ENTRY VIEW FUNCTION -----
# When edit_entry pages gets a GET request, edit_entry() will return a form for editing 
# the entry. When the page receives a POST request with the revised text it will save
# that modified txt to the DB

from .models import Topic, Entry
# need to import the Entry Model
# -- snip--
def edit_entry(request, entry_id):
	"""Edit an existing entry"""
	entry = Entry.objects.get(id=entry_id)
# Get the entry object that the user wants to edit and the topic 
# associated with this entry.
	topic = entry.topic
# get topic assco with entry

	if request.method != 'POST':
		# Initial request, pre-fill form with current entry
		form = EntryForm(instance=entry)
# This IF block runs for a GET request and makes an instance of EntryForm with the
# agrument instance=entry, this tells DJ to 
# create the from prefilled with info from existing entry object. - User will see and edit
	else:
# This else block will run for a POST request
		from = EntryFrom(instance=entry, data=request.POST)
# When it runs we pass the instance=entry and data=request.POST argument to tell DJ to
# create a form instance based on the information associated with the existing
# entry object updated with any new relevent data from request.POST
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
	context = {'entry': entry, 'topic': topic, 'form': form}
	return render(request, 'learning_logs/edit_entry.html', context)
# Redirect to topic page where user should see the edited entry

### -=-=-=-=-=- THE edit_entry TEMPLATE -=-=--
# need to make a new template named edit_entry.html
{% extends 'learning_logs/base.html' %}
{% block content %}
<p>
	<a href = "{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a>
</p>
<p>
	Edit entry:
</p>
<form action = "{% url 'learning_logs:edit_entry' entry.id %}" method = 'post'>
# the action argument sends the form back to the edit_entry() function for processing.
# We include the entry ID as an arugment so the view function can modify the corrext
# entry object
	{% csrf_token %}
	{{ form.as_p }}
	<button name='submit'>save changes</button>
</form>
{% endblock content %}

## -=-=-=-=- LINKING TO THE EDIT_ENTRY PAGE -0-0-0-0
# edit the topic.html page 
{% extends "learning_logs/base.html" %}

{% block content %}

	<p>Topic: {{topic}}</p>
	<p>Entries:</p>
	<p> <a href="{% url 'learning_logs:new_entry' topic.id %}" > add new entry</a>
	<ul>
	{% for entry in entries %}
		<li>
		<p>{{ entry.date_added|date:'M d, Y H:i'}} </p>
		<p>{{ entry.text|linebreaks}}</p>
		<p>
			<a href="{% url 'learning_logs:edit_entry' entry.id %}" > edit entry</a>
## Adding the edit link to edit the entry after the date and text has been displayed.
# use the {% url%} template tag to determine the URL for the named URL pattern
# edit_entry. along with the ID attribute for the current entry in the loop
# the link will appear after each entry on the page
		</p>
		</li>
	{% empty %}
		<li>
			No entries have been added yet
		</li>
	{% endfor %}
	</ul>

{% endblock content %}

##### 	------- SETTING UP USER ACCOUNTS ---------
# Need to set up user registration and authorization system to allow ppl to register
# an account and log in and out. We'll create a new app to contain all the functionallity
# realized to working with users. We'll also modify the Topic model slightly so every
# topic belongs to a certain user

## =-=-=-=-= THE USERS APP =-=-=-==
# Start by creating a new app called users using the startapp command in terminal
# be in virtual environment:
python manage.py startapp users
# make a new dir called users with same structure as learning_logs app
ls users # to make sure its set up

## Add app to INSTALLED_APPS in settings.py of learning_log

## Need to include the URLs from users
# Next we need to modify the root urls.py so it includes URLs we'll write in users app
# in urls.py in learning_log
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('learning_logs.urls')),
    path('users/', include('users.urls')),
]
# Add a line to include urls.py from users this line will match any URL that starts
# with the word users - localhost:8000/users/login/

## ---- THE LOGIN PAGE-----
# We'll use default login view DJ provides so the URL pattern looks a little different.
# Make a new urls.py file in the dir learning_log/users/, and add the following to it
"""Defines url patterns for users."""

"""Defines url patterns for users."""

from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'users'
urlpatterns = [
	# Login page.
    path('login/',
    	auth_views.LoginView.as_view(template_name='users/login.html'),
    	name='login'),
]
# Here we’ve defined the app_name variable, which defines the namespace for the 
# URLs associated with the users app. We’ve also used the path() function to define
# the URL pattern for the login page - localhost:8000/users/login
# when DJ reads that url it looks in users/urls.py and login tell it 
# to send requests to DJ default login view(the view argument is login not views.login)
# b/c we're not writing our own code we pass in the dictionary login is in 
# DJ 2.1 update
# There are two differences here. We’re importing a set of views from django.contrib.auth,
# as auth_views. Also, the path to the login view is structured differently, to use the
# default class-based view for logins, LoginView. In order to use our own login template, 
# we provide the template_name argument in the call to the default view.


## =-==-=- THE LOGIN TEMPLATE=-=-=-
# even though using default login page we still need a template, inside the
# learning_log/users/ dir make a dir called templates inside that make one called users
# and put login.html in that 

{% extends 'learning_logs/base.html' %}
# extends to ensure same look and feel to site - temp in one app can extend to a temp in another
{% block content %}

	{if form.errors %}
		<p> Your username and password did not match. Please try again</p>
# if form errors attribute is set we display an error message reporting that user/pass
# combo dont match anything stored in DB
	{% endif %}

	<form method = "post" action="{% url 'users:login' %}">
# Want the login view to process the form, so we set the action argument as the URL 
# of the login page
		{% csrf_token %}
		{{ form.as_p }}
# The login view sends a form to the template and its up to us to display the form 
# with this code 

		<button name='submit'> log in</button>
		<input type ='hidden' name='next' value="{% url 'learning_logs:index' %}" />
# adding a submit button and include a hidden form element 'next'; the value arguement
# tells DJ where to redirrect user after theyve loggedin successfully - to home page
		</form>
	{% endblock content}

#### -=-=- LINKING TO THE LOGIN PAGE =-=-=-
# Add the login link to base.html so it appears on every page but dont want it to
# appear if user is logged in so we nest it in an if block
# In DJs authentication system, every template as a user vaiable available
# which always has an is_authenticated attreibute set: the attribute is True is user
# is logged in and False if not. The allows to display one message to user if logged in
# and another if not 
<p>
	<a href = "{% url 'learning_logs:index' %} ">Learning Log</a> - 
	<a href = "{% url 'learning_logs:topics' %} " >Topics</a> - ## add a dash! 
	{% if user.is_authenticated %}
		Hello, {{ user.username }}
# greeting to logged in user. Auth users have an additional username attribtue set which
# we use to personalize getting and remind they are logged in 
	{% else %}
		<a href="{%url 'users:login' %}"> log in </a>
# Display a link to the login page for users who are not authenticated
	{% endif %}
</p>

{% block content %}
{% endblock content %}


### =-=-=-=- USEING THE LOGIN PAGE -=--=-=-
# Log out by going to localhost:8000/admin and go to localhost:8000/users/login/ and see the DJ login page 


 #### -=-=-=- LOGGING OUT =-=-=-
 # Need a way to log out not by going to admin page, so users will just click a link and 
 # be sent back to home page when log out not a whole new page. We'll define a URL pattern
 # for the logout link, write a view function, and provide a logout link on base.html

 ## -----LOGOUT URL -----
 # in users/urls.py for logging out 
    # Logout page.
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

## THE LOGOUT_VIEW( ) FUNCTION ####-=-=-

# In Django 2.1 there is no need for a logout view, so ignore what you see in this section
# in the book. Instead, we’ll use a setting called LOGOUT_REDIRECT_URL in learning_log/settings.py. 
#It doesn’t really matter where this setting goes, but I like to put it in a section at the 
# end of the file labeled # My settings:
#--snip--
# My settings
LOGOUT_REDIRECT_URL = '/'

## =-=-=-=-=-- LINKING TO THE LOGOUT VIEW =-=-=-=-
# Now need a logout link, we'll include it as part of base.html so its avilable on all pages
# and include it in the {if user auth} so only when logged in you see it

{% if user.is_authenticated %}
		Hello, {{ user.username }}
		<a href="{% url 'users:logout' %">log out> </a>

## =-=-=- THE REGISTRATION PAGE =-=--=-
# We will have to build a page that will let new users register. We will use DJs
# default UserCreationForm but write our own view function and template
# the code for the URL pattern for the registration page in users/urls.py
path('register/', views.register, name='register')

## THE REGISTER VIEW() FUNCTION -=-=-=-=-=-
# in users/views.py
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
# import these to login user if their registeration info is authentitacted
from django.contrib.auth.forms import UserCreationForm
# import the default UserCreationForm 

def register(request):
	"""Register a new user"""
	if request.method != 'POST':
		#Display blank reg form
		form = UserCreationForm()
# make instance of blank UserCreationForm is not POST request
	else:
		# Process completed form
		form = UserCreationForm(data=request.POST)
# If it is a POST request then we make and instance of the UCF and fill it with submitted data

	if form.is_valid():
# check if valid - username has appropriate characters, password match, and not trying to do
# anything malicious in their appempt 
		new_user = form.save()
# if valid call save method on form to save useranme and hash of password to DB
# this save method returns the newly created user object we store in new_user

		# log the user in and redirect to home page
		authenticated_user = authenticate(username=new_user.username,
								password=request.POST['password1'])
# With the users info saved we log them in which is a two step proces: we call authenticate()
# with the arguments new_user.username and their password - When they register the user
# is asked to enter two matching passwords, b/c the form is valid we know the passwords match
# so we can use either one. Here we get the value associated with the 'password1' key in the
# form's POST data. IF the username and password are correct the method returns an authenicated
# user object which we store in authenticated_user variable

		login(request, authenticated_user)
# Then call the login() function with the request and authenticated_user objects which creates
# a valid session for the new user.
		return HttpResponseRedirect(reverse('learning_logs:index'))
# We redirect the user to the home page where they will see the personalized greeting
	context = {'form', form}
	return render(request, 'users/register.html', context)

### -=-=-= THE REGISTER TEMPLATE =-=-=-=
# The template for registration is similar to login page. Save it in same dir as login.html
{% extends 'learning_logs/base.html' %}

{% block content %}

<form method="post" action="{% url 'users:register' %}">
	{% csrf_token %}
	{{ form.as_p }}
# use the as_p method so DJ will display all fields ok even if error not filled out ok

	<button name='submit'>register</button>
	<input type = 'hidden' name = 'next' value="{url 'learning_logs:index' %}"/>
	</form>
	{% endblock content %}



### =-=-=- LINKING TO THE REGISTRATION PAGE =-=-=
# Going to put it on base.html in the else clause so someone can register if theyre not signed in
	{% else %}
		<a href ="{% url 'users:login' %}"> log in </a> -
		<a href ="{% url 'users:register' %}">register</a> 
	{% endif %}


####------------- ALLOWING USERS TO OWN THEIR DATA -------
# users should be able to enter data exclusive to them, so need to create a system to figure out
# who data belongs to and restrict access to certain pages so users can only work with their dta
# modify topic model so every topic belongs to specific user - this will also take care of entries
# b/c every entry belongs to a specific topic - start by restricting access to certain pages

## ------- RESTRICTING ACCESS TO THE TOPIC PAGE -------
# DJ makes it easy to restrict access thru the @login_required decorator. A DECOTRATOR - 
# is a directive placed just before a function definition that python applies to the function
# before it runs to alter how the function code behaves 
# Every topic will be owned by a user, so only registered users should be able to request the
# topics page - add to learning_logs/views.py

from django.contrib,auth.decorators import login_required

@login_required
# adding this decorator here to alter how it behaves - so python knows to run the code in 
# login_required before the code in topics(). The code in login_required() checks to see if a user
# is logged in, and DJ will run the code in topics() only if they are. IF the user is not logged
# in theyre redirected to login page.
def topics(request):
	""" Show all topics"""
	topics = Topic.objects.order_by('date_added')
	context = {'topics':topics}
	return render(request, 'learning_logs/topics.html', context)

#To make this redirect work we need to alter settings.pyso DJ knows there to find the login page
# My_settings
LOGIN_URL = 'users/login/'

# Now when unauthenticated user requests a page protected by the @login_required decorator DJ 
# will send them to the URL defined by LOGIN_URL in settings.py

###-=-=-=-=-=-=-=-=- RESTRICTING ACCESS THROUGHOUT THE LEARNING LOG------
# DJ makes it easy to restrict access to pages but you have to decide which pages to protect
# better to think about which pages need to be restricted first 
# in learning_logs restrict every other page that is not homepage/registration/logout - not index
def index(request):
@login_required
def topics(request):
@login_required
def topic(request, topic_id):
@login_required
def new_topic(request):
@login_required
def new_entry(request, topic_id):
@login_required
def edit_entry(request, entry_id):



## -=-=-=- CONNECTING DATA TO CERTAIN USERS =-=-====-=-
# Now we need to connect the data submitted to the user who submitted it. We need to only
# connect the highest data heierarchy to a user, and the lower level data will follow.
# For example in LL topics are the highest level of data in the app, and all entries are 
# connected to a topic. As long as each topic is connected to a specific user we'll be able
# to trace the ownership of each entry in the DB

# We modify the topic model by adding a foreign key realtionship to a user. We'll then 
# migrate the DB, then we modify some of the views so they only show data asso with logged in user

## -=-=-=-=- MODifYING THE TOPIC MODEL -=-=-=-
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Topic(models.Model):
	''' A topic user is learning about'''
	text = models.CharField(max_length=200)
	date_added = models.DateTimeField(auto_now_add=True)
	owner = models.ForeignKey(User, on_delete=models.CASCADE)
# Import User model from DJ and then add an owner field to Topic, which establishs a foreign
# key relationship to the User model



## -------------- IDENTIFYING EXISTING USERS ------------
# When we migrate the DB, DJ will modify the DB so it can store a connection between each topic
# and a user. To make the migration DJ needs to know which user to assoc with each existing
# topic The simplest approach is to give all existing topics to one user - for example
# the superuse. First we need to know the ID of that superuser. Look at the IDs of all users 
# created so far, by starting a DJ shell session and issue the commands:
>>> from django.contrib.auth.models import User
#import User to current session
>>> User.objects.all()
# look at all users so far
<QuerySet [<User: Nicolasdha>, <User: Ndurikha>, <User: meowmeow>]>
>>> for user in User.objects.all():
...     print(user.username, user.id)
Nicolasdha 1
Ndurikha 2
meowmeow 3
# loop thru list of users and print each users username and ID when DJ asks which user to 
# assco the existing topics with we'll use on of these ID values


## ------------------MIGRATING THE DATABASE-------------
# Now with IDs we can migrate the DB - in terminal:
(11_env) nic-duriks-macbook-pro:learning_log sankp001$ python manage.py makemigrations learning_logs
# Start by issuing makemirgations command 

You are trying to add a non-nullable field 'owner' to topic without a default; we can't do that 
(the database needs something to populate existing rows).
Please select a fix:
 1) Provide a one-off default now (will be set on all existing rows with a null value for this column)
 2) Quit, and let me add a default in models.py
# Here DJ says we're trying to add a required (non-nullable) field to an existing model(topic)
# with no deafult value specified. DJ gives two options 1: we can provide a deafult right now
# or we can quit and make a dafault models.py

Select an option: 1
# Choose first option
Please enter the default value now, as valid Python
The datetime and django.utils.timezone modules are available, so you can do e.g. timezone.now
Type 'exit' to exit this prompt
>>> 1
# Asks to enter the deafult value - to assco all existing topics with the original admin user
# entered 1. DJ then migrates the DB using this value and generates the migration file 0003_topic_owner.py
# which adds the field 'owner' to the Topic model - actually it doesnt in my version
Migrations for 'learning_logs':
  learning_logs/migrations/0003_auto_20200819_2109.py
    - Add field owner to topic
    - Alter field topic on entry

 # now can carry out the migration 
 >>> python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, learning_logs, sessions
Running migrations:
  Applying learning_logs.0003_auto_20200819_2109... OK
# DJ applies new migration and result is ok
# can verify it worked in a shell session 
>>> from learning_logs.models import Topic
>>> for topic in Topic.objects.all():
...     print(topic, topic.owner)
... 
Chess Nicolasdha
Rock Climbing Nicolasdha
Knife Making Nicolasdha
>>> 
# You can reset the DB without migrating but that would lose all information and it is good to
# practice migrating the DB while maintaining the users data. To reset the DB - start fresh
# issue the command python manage.py flush - you will have to create a new superuser and 
# all data will be gone

## -------------- RESTRICTING TOPICS ACCESS TO APPROPRIATE USERS -----
# Currently if logged in you can see all topics no matter which user, change that by showing
# users only the topics that belong to them - topics() function in views.py

### ------------- old old OLD OLD OLD ----------
@login_required
def topics(request):
	""" Show all topics"""
	topics = Topic.objects.order_by('date_added')
	context = {'topics':topics}
	return render(request, 'learning_logs/topics.html', context)
##---------------- NEW NEW NEW NEW -------------

@login_required
def topics(request):
	""" Show all topics"""
	topics = Topic.objects.filter(owner=request.user).order_by('date_added')
# When a user is logged in the request object has a request.user attribute set that stores
# info about the user. The code fragment Topic.objects.filer(owner=request.user) tells DJ
# to only retireve Topic objects from the DB whoes owner attribute matches the current user
# Because we're not changing how topics are displayed, we dont need to change the template 
# for the topics page at all - to check if it worked log out and back in to see 
	context = {'topics':topics}
	return render(request, 'learning_logs/topics.html', context)

##----------------PROTECTING A USERS TOPICS ---------------
# havent actually restricted the users pages yet, can still enter/topics/1 and get to the 
# page when not logged in corrextly - will fix in topic() function now
from django.http import Http404
@login_required
def topic(request, topic_id):
	'''show a single topic and all of its entries'''
	topic = Topic.objects.get(id=topic_id)
	# Make sure the topic belongs to the current user
	if topic.owner != request.user:
		raise Http404
# 404 is a standard error response thats given when resource dosnt exist on server. Import Http404
# which we will raise if user requests a topic they shouldnt see. After receiveing a topic 
# request we make sure the topics user matches the currently logged in user and raise 404 if not

	entries = topic.entry_set.order_by('-date_added')
	context = {'topic':topic, 'entries':entries}
	return render(request, 'learning_logs/topic.html', context)

### ------------PROTECTING THE EDIT_ENTRY PAGE ----------------
# the edit_entry pages have URLS in the form localhost:8000/edit_entry/entry_id where the 
# entry_id is a number. Want to protect this page so no one can use the URL to gain access
# to someone elses entries

@login_required
def edit_entry(request, entry_id):
	'''Edit exsisting entry'''
	entry = Entry.objects.get(id=entry_id)
	topic = entry.topic
	if topic.owner != request.user:
		raise Http404
# retrieve the entry and topic associated with this entry and check if the owner of the topic
# matches the currently logged-in user; if they dont match raise http404

	if request.method != 'POST':
		form = EntryForm(instance=entry)
	else:
		form = EntryForm(instance=entry, data=request.POST)
		if form.is_valid():
			form.save()
		return HttpResponseRedirect(reverse('learning_logs:topic', args=[topic.id]))
	context = {'entry':entry, 'topic':topic, 'form':form}
	return render(request, 'learning_logs/edit_entry.html', context)



######## --------- ASSOCIATING NEW TOPICS WITH THE CURRENT USER ------
# Currently the page for adding new topics does not work, it returns NOT NULL constraint failed:
# which is saying cant create new topic without specifying a value for the topic's owner field
# the fix is using the access to the current user thru the request object - to new_topic()

@login_required
def new_topic(request):
	""" Add a new topic"""
	if request.method != 'POST':
		form = TopicForm()
	else:
		form = TopicForm(data=request.POST)
		if form.is_valid():
			new_topic = form.save(commit=False)
# pass the commit=False arg in b/c need to modify the new topic before saving it to the DB
# this holds off on saving it just yet b/c need to do something else to it

			new_topic.owner = request.user
# Then set the new topics owner attribute to the current user

			new_topic.save()
# call save() on the topic instance just defined
			return HttpResponseRedirect(reverse('learning_logs:topics'))
	context = {'form':form}
	return render(request, 'learning_logs/new_topic.html', context)



### ----- STYLING THE APP -------
## use django-bootstrap3 to integrate Bootstrap into the program. The app downloads the req
# BS files puts them in appropriate location in project, makes styling directices avilable
# in projects templates - in terminal
pip install django-bootstrap3
# need to add BS to the settings.py in LL to source from it - settings.py 
# Third Party Apps
'bootstrap3'
# most apps need to be included in the INSTALLED APPS settings - look up setup instructions for apps use

# Need DJ to include jQuery, a JS library that enables some of the interactive elements
# that the BS template provides. Add this code to settings.py
# Settings for django-bootstrap3
BOOTSTRAP3 = {
    'include_jquery': True,}

## BS is bascially a large collection of styling tools. Also has a number of templates you can
# apply to your project to create a particular overall syle. If just starting out it much easier
# to use these templates than to use individuals syling toolds. The see the templates bootstrap
# offers go to the Getting Started section at getbootstrap.com - scroll down to examples heading
# and look for the navbars in action setting. We will use the static top navbar template
# which provides a simple top navigation bar, a page header, and a container for the content
# of the page. 


############# -------- MODIFYING BASE.HTML----------------
## Need to modify the base.html to accommodate the BS template

## Defining the HTML Headers --------
# first change will define the HTML headers in the file so whenever a Learning Log page is open,
# the browser title bar displays the site name. Also add some requiremnets for using BS
# in our templates - DELETE ALL BASE.HTML AND REPLACE WITH
{% load bootstrap3 %}
# Load a collection of Template Tags availble in DJ-BS3

<! DOCTYPE html>
# declare this is a HTML doc

<html lang='en'>
# written in english

	<head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">
# This contains no actual inforamtion - just tells the browser what it needs to know to display
# things correctly

		<title><Learning Log</title>
# Include a title element for the page which will be displauyed in the title bar when the page is open
		{% bootstrap_css %} # BS3_css in book?
		{% bootstrap_javascript %}
	# We use one of DJ-BS3 custom template tags which tells DJ to include all the BS style files
	# the JS tag enables all the interactive bahvior you might use on a page, like collapseable nav bars

	</head>

###--------- 	DEFINING THE NAVIGATION BAR ---------
# Def the nav bar on the top in base.html
--snip--
</head>
<body>
	<!-- Static navbar -->
# The first element is the opening body tag, the body is what users will see in a page
# the <nav> element indicates the navigation links section of the page. Everything contained
# in this element is styled according to the BS style rules defined by the selectors navbar,
# navbar-default, and navbar-static-top. A selector determines which elements on a page
# a certain syle rule applies to.
	<nav class="navbar navbar-default navbar-static-top">
		<div class="container">





			<div class="navbar-header">
# The template defines a button that will appear in the browser window is too narrow to display
# the whole navigation bar horizontally. When the user clicks the button the nav elements will
# appear in a drop down list. The collapse referenc causes the nav bar collapse when the user
# shinks the window or when site is displays on a mobile device
				<button type="button" class="navbar-toggle collapsed"
					data-toggle='collapse' data-target="#navbar"
					aria-expanded="false" aria-controls="navbar">
				</button>


				<a class="nav-brand" href="{% url 'learning_logs:index' %}">
# We set the projects name to appear at the far left of the nav bar and make it link to the 
# home page b/c it will appear on every page 
					Learning Log</a>
			</div>


			<div id="navbar" class="navbar-collapse collapse">
# We define a set of links that let users navigate the site. A navbar is a list that starts
# with <ul> and each link is an item in this list <li>
				<ul class="nav navbar-nav">
# <ul> start - unorg list
					<li><a href="{% url 'learning_logs:topics' %}">Topics</a></li>
# <li> start -  li is a part of a unorg or org list
				</ul>
# To ADD MORE LINKS insert more lines using the structure:
# <li><a href="{% url 'learning_logs:title' %}">Title</a></li> - This reps a single link in nav bar
# The link is taken from the previous version of base.html

				<ul class="nav navbar-nav navbar-right">
					{% if user.is_authenticated %}
						<li><a>Hello, {{ user.username }}.</a></li>
						<li><a href="{url 'users:logout' %}">log out</a></li>
					{% else %}
						<li><a href="{% url 'users:register' %}">register</a></li>
						<li><a href="{% url 'users:login' %}"> log in</a></li>
					{% endif %}
# Here we place a second list of nav links using the selector navbar-right. The navbar-right
# selector styles the set of links so it appears at the right edge of the nav bar where you
# typically see login/registration/usergreeting/logout links
				</ul>
			<div> <!--/.nav-collapse -->

		</div>
		</nav>


### ----- DEFINING MAIN PART OF THE BASE.HTML PAGE ---------
# The rest of base.html contains the rest of the page
--snip--
	</nav>

	<div class="container">
# The opening div with the class container. A div is a section of a web page that can be used
# for any pyrpose and can be styled with a boarder, margins, padding, BG color, and other style rules
# This particular div acts as a container into which we place two elements: a new block 
# called header and the content block. The header block contains information telling the user
# what kind of info the page holds and what they can do on the page. It had the call page-header
# which applies a set of style rules to the block. The content block is in a seperate div with no 
# specific style classes

		<div class="page-header">
			{% block header %}{% endblock header %}
		</div>
		<div>
			{% block content %}{% endblock content %}
		</div>
	</div> <!-- /container -->
</body>
</html>


### ----- STYLING THE HOME PAGE AND USING A JUMBOTRON ------
# Lets use the new defined header block to update the home page and another BS element called
# a jumbotron which is a large box that will stand out from the rest of the page and cna
# contain anything you want. It is typcailly used on homepages to hold  a brief description of
# the overall project - update messaage on home page too
# in index.html

{% extends "learning_logs/base.html" %}

{% block header %}
# Tell DJ we;re about to define what goes inside the header block
	<div class='jumbotron'>
		<h1> Track your learning!</h1>
# Inside a jumbotron element place a short tagline to give first time visitors a sense of LL
	</div>
{% endblock header %}

{% block content %}
	<h2>
# Here we add text to provide more direction, invite to make an acct, and describe two main
# actions make new topics/entries 
		<a href="{% url 'users:register' %}"> Register an account</a> to make your own 
			Learning Log, and list topic you are learning about.
	</h2>
	<h2>
	Whenever you learn something new about a topic, make an entry summarizing what you learned
	</h2>
{% endblock content %}

### --------- STYLIZING THE LOGIN PAGE-------
# want to refine appearance of login form to look consistant with rest of page
# in login.html
{% extends 'learning_logs/base.html' %}
{% load bootstrap3 %}
# Load the BS3 template tags into this template

{% block header %}
# Define a header block which describes what the page is for - we removed the {% if form.errors%}
# b/c DJ-BS3 manages form errors automatically

	<h2>Log in to your account</h2>

{% endblock header %} 

{% block content %}


<form method= "post" action="{% url 'users:login' %}" class="form">
	{% csrf_token %}
	{% bootstrap_form form %}
# add a class='form' attribute and then use the template tag {% bootstrap_form } when we display
# the form. This replaces the {{ form.as_p }} tag, The BS_form tag inserts BS style rules into
# the individual elements of the form as its rendered

	{% buttons %}
	<button name='submit' class="btn btn-primary">log in</button>
	{% endbuttons %}
# Here we open a BS3 template tag {%buttons} that adds BS styling to buttons

	<input type = 'hidden' name='next' value="{% url 'learning_logs:index' %}">
</form>
{% endblock content %}


##-------------- STYLING A NEW_TOPIC PAGE -----------
# Need to make rest of pages look consistant- same code as login.html

{% extends "learning_logs/base.html" %}
{% load bootstrap3 %}

{% block header %}
<h2> Add a new topic: </h2>
{% endblock header %}


{% block content %}
	<form action="{% url 'learning_logs:new_topic' %}" method='post' class="form">
# add a form class to the form tag
		{% csrf_token %}
		{% bootstrap_form form %}

		{% buttons %}
		<button name="submit" class="btn btn-primary">add topic</button>
		{% endbuttons %}

	</form>
{% endblock content %} 

## ----- STYLING THE TOPICS PAGE ---------
{% extends "learning_logs/base.html" %}

{% block header%}
<h1> Topics: </h1>
{% endblock header %}

{% block content %}
	{% for topic in topics %}
		<h3><li>
			<a href="{% url 'learning_logs:topic' topic.id %}">{{topic}}</a>
		</li></h3>
	{% empty %}
		<li> 
			<h1>No topics have been added yet</h1>
		</li>
	{% endfor %}
	</ul>
	<h3><a href = "{% url 'learning_logs:new_topic' %}"> Add a new topic:</a></h3>
{% endblock content %}

# dont need to load bBS3 b/c not using any custom BS3 template tags in the file. 


##### ------------ STYLING THE TOPICS PAGE --------
# This has more content than most pages, so it needs a bit more work. We'll use BS's panels
# to make each entry stand out. A PANEL is a div with a predefined styling and is perfect
# for displaying a topics entires:

{% extends "learning_logs/base.html" %}

{% block header %}
	<h2>{{ topic }}<h2>
{% endblock header %}
# Place topic in header block and delete unordered list structure. 

{% block content %}
	<p>
		<a href="{% url 'learning_logs:new_entry' topic.id %}" > add new entry</a>
	</p>
	{% for entry in entries %}
		<div class="panel panel-default">
			<div class = "panel-heading">
#Instead of making each
# entry a list item, we create a panel div element which contains two more nested
# divs: a panel-heading div and a panel-body div. 
				<h3>
					{{ entry.date_added|date:'M d, Y H:i'}}
# The panel-heading div contains the date for the entry and the link to edit the entry.
					<small>
					<a href="{% url 'learning_logs:edit_entry' entry.id %}">edit entry</a>
					</small>
				</h3>
# Both date and edit are h3 but wrapped in <small> tags too which make it a little smaller
# than the timestamp
			</div>
			<div class="panel-body">
				{{ entry.text|linebreaks}}
# In panel body the actual text is contained  - no code for including info on pages have changed
# only the sylizing code has changed
			</div>
		</div> <!-- panel -->

	{% empty %}
			No entries have been added yet
	{% endfor %}

{% endblock content %}
# if want to use a different BS template, follw a similar process to what done so far copy the
# template into base.html and mod the elemtns that contain actual content so the template
# displays project info. Then use BS individual styling tools to style conent on each page

## ON MY OWN - NEED TO MAKE CHANGES TO NEW_ENTRY, EDIT_ENTRY, REGISTER

##------ NEW ENTRY STYLYIZE----------
{% extends 'learning_logs/base.html' %}
{% block content %}
<p>
	<a href = "{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a>
</p>

<p>
	Add a new entry:
</p>

<form action = "{% url 'learning_logs:new_entry' topic.id %}" method = 'post'>
	{% csrf_token %}
	{{ form.as_p }}
	<button name='submit'>add entry</button>
</form>
{% endblock content %}

#######- new new new new
{% extends 'learning_logs/base.html' %}
{% load bootstrap3 %}


{% block header %}
<h3>
<a href = "{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a>
</h3>
{% endblock header %}


{% block content %}
<div>
	<h4>
		Add a new entry:
	</h4>
</div>

<form action = "{% url 'learning_logs:new_entry' topic.id %}" method = 'post' class='form'>
	{% csrf_token %}
	{% bootstrap_form form %}
	{% buttons %}
	<button name='submit' class='btn btn-primary'>add entry</button>
	{% endbuttons %}
</form>
{% endblock content %}

### -------EDIT_ENTRY STYALIZE ---------
{% extends 'learning_logs/base.html' %}
{% block content %}
<p>
	<a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a>
</p>
<p>
	Edit Entry:
</p>
<form action = "{% url 'learning_logs:edit_entry' entry.id %}" method='post'>
	{% csrf_token %}
	{{ form.as_p }}
	<button name='submit'>Save edit</button>
</form>
{% endblock content %}
## -------- NEW NEW NEW NEW -=---
{% extends 'learning_logs/base.html' %}
{% load bootstrap3 %}

{% block header %}
<h2>
<a href="{% url 'learning_logs:topic' topic.id %}">{{ topic }}</a>
</h2>
{% endblock header %}


{% block content %}
<div>
	<h4>
	Edit Entry:
	</h4>
</div>

<form action = "{% url 'learning_logs:edit_entry' entry.id %}" method='post' class='form'>
	{% csrf_token %}
	{% bootstrap_form form %}

	{% buttons %}
	<button name='submit' class='btn btn-primary'>Save Edit</button>
	{% endbuttons %}

</form>

{% endblock content %}


### ----SYALIZE REGISTER ----

{% extends 'learning_logs/base.html' %}

{% block content %}

<form method="post" action="{% url 'users:register' %}">
	{% csrf_token %}
	{{ form.as_p }}
	<button name='submit'>register</button>
	<input type="hidden" name='next' value="{% url 'learning_logs:index' %}"/>
</form>
{% endblock content %}



{% extends 'learning_logs/base.html' %}
{% load bootstrap3 %}

{% block content %}

<form method="post" action="{% url 'users:register' %}">
	{% csrf_token %}
	{% bootstrap_form form %}

	{% buttons %}
	<button name='submit' class='btn btn-primary'>Register</button>
	{% endbuttons %}
	<input type="hidden" name='next' value="{% url 'learning_logs:index' %}"/>
</form>
{% endblock content %}



### ---------- DEPLOYING APP ON LIVE SERVER-----
# Put it on a live server so anyone can access it - Heroku, web-based platform that allows
# you to manage the deployment of web appliations. 

# download and regiwster with heroku and then etner 
brew tap heroku/brew && brew install heroku
 # in temrinal

 # in terminal in the venv_learning_log issue the following commands one at a time 
 pip install dj-database-url
 # this helps DJ comm with the DB Heroku uses
 pip install whitenoise
 # these two statics help DJ manage static files correctly - static files contain style rules and JS files
 pip install gunicorn
# this is a server capable of serving apps in a live envi
Add this to settings.py middleware     'whitenoise.middleware.WhiteNoiseMiddleware',

##### --- CREATING A PACKAGES LIST WITH A requirments.txt FILE ---
# Heroku needs to know which packages our project depends on, so we will use pip to generate
# a file listing them. From active venv
pip freeze > requirements.txt
# the freeze command tells pip to write the names of all the packages currently installed 
# in the project into the file requirements.txt. Open it to make sure
# When we deploy learning logs Heroku will install all the packages listed in
# requirements.txt creating an environment with the same packages were using locally
# so it will behave the same- huge advantage when build/maintain various projects on system

## Next need to add psycopg2 which helps Heroku manage the live DB to the list of packages
# open req.txt and add line 

asgiref==3.2.10
dj-database-url==0.5.0
Django==3.1
django-bootstrap3==14.1.0
gunicorn==20.0.4
pytz==2020.1
sqlparse==0.3.1
whitenoise==5.2.0
psycopg2>=2.8.5


###### --------- SPECIFYING THE PYTHON RUNTIME ----------
# Unless you specify a python version Heroku will use its own current defualt version of 
# python. Make sure HKU uses the same version of python were using. In an actice venv issue 
 python --version = Python 3.8.5

# Make a new file called runtime.txt in same dir as manage.py with one line with PY version
# specified - python all lowercase followed by a hyphen and 3-part version number - if
# get error that runtime you requested is not avilable go to devcenter.heroku.com/categories/language-support
# and look for a link specifying python runtime and look for avilable runtimes
python-3.8.5

###### -------------------MODFYING SETTINGS.PY FOR HEROKU ----------
## Now need to add a section at the end of settings.py to define some settings specifically
# for the HKU environment - in settings.py

# Settings for django-bootstrap3
BOOTSTRAP3 = {
    'include_jquery': True,
}
# Heroku settings 
cwd = os.getcwd()
# here we use the function getcwd() which gets the current working directory the file is running
# from. In a HKU deployment the dir is always /app. During the build process, the project runs
# from a temporary dir that starts with /tmp. In a local delopment the dir is usually
# the name of the project folder(learning_log). The if test ensures that the settings
# in this block apply only when the project is delopyed on HKU. This structure allows
# us to have one settings file that works for our local development environment as well
# as the live server
if cwd == '/app' or cwd[:4] == '/tmp':
	import dj_database_url
# here we import to help configure the database on HKU. HKU ueses PostgreSQL (also called Postgres)
# a more advanced database than SQLite, and these settings configure the project to use
# PostgreSQL on HKU.
	DATABASES = {
		'default': dj_database_url.config(default='postgres://localhost')
	}

	# Honor the 'Z-Forwarded-Proto' header for request.is_secure().
	SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# The rest of these settings support HTTPS requests, ensure that DJ will serve the project from
# HKU's URL

	# Allow all host headers.
	ALLOWED_HOSTS=['*']
#ensure that DJ will serve the project from HKU's URL


	# Static asset configuration
	BASE_DIR = os.path.dirname(os.path.abspath(__file__))
	STATIC_ROOT = 'staticfiles'
	STATICFILES_DIRS = (
		os.path.join(BASE_DIR, 'static'),
		)
# This sets up the project to serve static files correctly on HKU


