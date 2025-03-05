import os
import sys
from django.conf import settings
from django.contrib.auth.hashers import make_password, check_password
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from mongoengine import connect, Document, StringField

# MongoDB setup using MongoEngine
connect('user_database', host='mongodb://localhost:27017/', alias='default')

# Define User model with MongoEngine
class User(Document):
    email = StringField(required=True, unique=True)
    username = StringField(required=True, unique=True)
    password = StringField(required=True)

# Django settings (simplified for this example)
import os
from django.conf import settings

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings.configure(
    DEBUG=True,
    SECRET_KEY='your-secret-key',
    ROOT_URLCONF=__name__,
    ALLOWED_HOSTS=['*'],
    INSTALLED_APPS=['django.contrib.auth', 'django.contrib.contenttypes', 'django.contrib.sessions'],
    MIDDLEWARE=['django.middleware.common.CommonMiddleware', 'django.middleware.csrf.CsrfViewMiddleware'],
    DATABASES={'default': {'ENGINE': 'django.db.backends.dummy'}},
    TEMPLATES=[  # 🔥 Added Template Configuration
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Correct path to templates
            'APP_DIRS': False,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                ],
            },
        },
    ],
)


def signup_page(request):
    return render(request, 'signup.html')

def login_page(request):
    return render(request, 'login.html')

def main_page(request):
    return render(request, 'main_page.html')

@csrf_exempt
def signup(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = make_password(request.POST.get('password'))

        # Check if the username already exists
        if User.objects.filter(username=username).first():
            return JsonResponse({'error': 'Username already exists'})

        User(email=email, username=username, password=password).save()
        return redirect('/login')
    
    return JsonResponse({'error': 'Invalid request'})

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = User.objects.filter(username=username).first()

        if user and check_password(password, user.password):
            return redirect('/main_page')
        return JsonResponse({'error': 'Invalid credentials'})
    
    return JsonResponse({'error': 'Invalid request'})

from django.urls import path

# Redirect to login page when accessing the root URL
def home_redirect(request):
    return redirect('/login')

urlpatterns = [
    path('', home_redirect),  # Redirect root URL to login page
    path('signup', signup_page),
    path('login', login_page),
    path('main_page', main_page),
    path('signup_user', signup),
    path('login_user', user_login),
]

if __name__ == "__main__":
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)
