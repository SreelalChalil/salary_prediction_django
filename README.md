

## STEP 1. SETUP Python Virtual Environment

### Create a directory: eg: djangoenv

    mkdir djangoenv
    cd djangoenv

###  Create a python venv

    python3.8 -m venv djangoenv

###  Activate the virtual Environment

    source djangoenv/bin/activate

###  Install the required packages for out project using pip

    pip install django scikit-learn pandas matplotlib pickle-mixin

[To leave your virtual environment, you need to issue the deactivate command from anywhere on the system:]

    deactivate

## STEP 2: Create django project

###  Create django project (name : salary_prediction_django) using django-admin
-------------------------------------------

     django-admin startproject salary_prediction_django

 
 * Create static, templates, model directory in root directory of project
 * Copy model.py and hiring.csv to model directory
 * Create index.html in templates directory
 * Create css/style.css in static directory

 ###  Modify Django setting:
 -----------------------
* Goto directory salary_prediction_django -> open settings.py

*	Add filepath to acess our model from django views.py file

	import os
        FILES_DIR = os.path.abspath(os.path.join(BASE_DIR, 'model'))

* Check the templates setting

		TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [''],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

* Add the templates directory to DIRS

		TEMPLATES = [

        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': ['templates'],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                ],
            },
        },
    ]

* Add settings to access static files (to import css file in our templates)
		
		STATIC_URL = '/static/' 

		STATICFILES_DIRS = [
		    os.path.join(BASE_DIR, "static"),
		]

* Created views.py
* Added view to urls.py by importing views.py

***********************************************
STEP 3: Creating Docker Image
******************************************

1. Generate a list of packages required to run our project
-------------------------------------------------------------------

	pip freeze > requirements.txt

This will add all the installed packages in our venv  to requirements.txt
The packages will be installed in container using the 'pip install -r requirements.txt' command.

----------------------------------

2. Create Dockerfile
-----------------------------------

	FROM ubuntu:20.04
    ENV PYTHONUNBUFFERED=1
    RUN apt-get update && apt-get install -y tzdata && apt install -y python3.8 python3-pip
    RUN apt install python3-dev libpq-dev nginx -y
    RUN mkdir /app
    COPY requirements.txt /
    RUN pip install -r requirements.txt
    ADD . /app
    WORKDIR /app
    EXPOSE 8000
    CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "salary_prediction_django.wsgi"]

3. Build Docker Image:
-----------------------------------
	docker build -t salary_prediction_django .

4. Run the container:
----------------------------------------
	docker run -d -p 8000:8000 salary_prediction_django

