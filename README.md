# quiz_django

A simple quiz application built with html5, css3, jquery, bootstrap4.5 and django.

## Getting started

_git clone https://github.com/ccir41/quiz_django_
_cd quiz_django_

## Create virtual environment and activate it

### Ubuntu

_python3 -m venv quiz-venv_
\_source quiz-venv/bin/activate

### Windows

_py -m venv quiz-venv_
_quiz-venv\Scripts\activate.bat_

## Install requirements

_pip3 install -r requirements.txt_

_python manage.py makemigrations user quiz_
_python manage.py migrate_

### Create Admin User

_python manage.py createsuperuser_

### Loding sample quiz from json file

_python manage.py loaddata db.json_

### Run development server

_python manage.py runserver 127.0.0.1:8000_

**Visit 127.0.0.1:8000**
This is the home page of our quiz application which displays the quiz categories. If there were no quiz categories, they can be added by signing with admin user and navigating to admin section at top of navigation bar. Similiarly quiz exam and questions also can be added and updated with admin page.

To give exam you have to click either of the categories which takes you to the exam page and by clicking any of the exam takes you to the questions page.

The user **response** will be displayed right after submitting the quiz exam.

**In order to take exam, you should signed in**

_snapshots of apps are inside img folder of static folder_

**quiz exam page**
![Image of quiz exam page]
(https://github.com/ccir41/quiz_django/static/img/quiz_exam.png)

**quiz result page**
![Image of quiz result page]
(https://github.com/ccir41/quiz_django/static/img/quiz_result.png)
