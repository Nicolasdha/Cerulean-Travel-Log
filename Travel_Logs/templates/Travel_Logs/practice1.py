{% load bootstrap3 %}
{% bootstrap_css %}
{% bootstrap_javascript %}


<! DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="utf-8">
		<meta http-equiv="X-UA-Compatible" content="IE=edge">
		<meta name="viewport" content="width=device-width, initial-scale=1">

		<title>Learning Logs</title>

		{% bootstrap_css %}
		{% bootstrap_javascript %}

		 <link rel="stylesheet" 
          href= "learning_logs:stylesheet.css"> 
  
    <style> 
          
        .navbar-custom { 
          background: rgb(163,9,34);
background: linear-gradient(90deg, rgba(163,9,34,1) 0%, rgba(9,9,121,1) 35%, rgba(0,212,255,1) 100%);
        } 

          
        .navbar-custom .navbar-brand, 
        .navbar-custom .navbar-text { 
            color: black; 
            font-size:22px ;
        }

        .bold_text {
         	font-weight:700;
        } 

        .font_size {
        	font-size:17px
        }

        .transparent{
    border-width: 0px;
    -webkit-box-shadow: 0px 0px;
    box-shadow: 0px 0px;
    background-color: rgba(0,0,0,0.0);
    background-image: -webkit-gradient(linear, 50.00% 0.00%, 50.00% 100.00%, color-stop( 0% , rgba(0,0,0,0.00)),color-stop( 100% , rgba(0,0,0,0.00)));
    background-image: -webkit-linear-gradient(270deg,rgba(0,0,0,0.00) 0%,rgba(0,0,0,0.00) 100%);
    background-image: linear-gradient(180deg,rgba(0,0,0,0.00) 0%,rgba(0,0,0,0.00) 100%);
}

    </style> 



	</head>

	<body>
		<!-- Static navbar -->
		<nav class="navbar navbar-default navbar-static-top">
			<div class="container">

				<div class="navbar-header">
					<button type='button' class="navbar-toggle collapsed"
						data-toggle="collapse" data-target="#navbar"
						aria-expanded="false" aria-controls="navbar">
					</button>
					<a class="navbar-brand" href="{% url 'learning_logs:index' %}">
					Learning Log</a>
				</div>

				<div id="navbar" class="navbar-collapse collapse">
					<ul class="nav navbar-nav">
						<li><a href="{% url 'learning_logs:topics' %}">Topics</a></li>
						<li><a href="{% url 'learning_logs:practice' %}">Practice</a></li>
					</ul>

					<ul class="nav navbar-nav navbar-right">
						{% if user.is_authenticated %}
							<li><a>Hello, {{ user.username }}, you are awesome! </a></li>
							<li><a href="{% url 'users:logout' %}">Log Out</a></li>
						{% else %}
							<li><a href="{% url 'users:register' %}">Register</a></li>
							<li><a href="{% url 'users:login' %}">Log In</a></li>
						{% endif %}
					</ul>
				</div><!--/.nav-collapse -->
			</div>
		</nav>

		<div class="container">

			<div class="page-header">
				{% block header %}{% endblock header %}
			</div>
			<div>
				{% block content %}{% endblock content %}
			</div>
		</div> <!-- /container -->

{% block header %}
	<div class='jumbotron'>
		<h1> Track your learning!</h1>
	</div>
{% endblock header %}

{% block content %}
	<h2>
		<a href="{% url 'users:register' %}"> Register an account</a> to make your own 
			Learning Log, and list topic you are learning about.
	</h2>
	<h2>
	Whenever you learn something new about a topic, make an entry summarizing what you learned
	</h2>


{% endblock content %}




	</body>
</html>