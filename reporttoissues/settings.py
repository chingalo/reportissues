import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
gettext = lambda s: s
PROJECT_PATH = os.path.split(os.path.abspath(os.path.dirname(__file__)))[0]
DEBUG = True
TEMPLATE_DEBUG = DEBUG
ADMINS = (
     ('joseph chingalo', 'profschingalo@gmail.com'),
)
MANAGERS = ADMINS
DATABASES = {
    'default': { 
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'ims',                     
        'USER': 'ims',
        'PASSWORD': 'IMS*',
    }
}
ALLOWED_HOSTS = ['*']
TIME_ZONE = 'Africa/Dar_es_Salaam'
LANGUAGE_CODE = 'en-us'
SITE_ID = 1
USE_I18N = True
USE_L10N = True
USE_TZ = True
MEDIA_ROOT = os.path.join(PROJECT_PATH, "media")
MEDIA_URL = "/media/"
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)
SECRET_KEY = '8#pdho3q*cvh4b#u8l_v7$mvvg+6jx#=r9=qhs0ksyp+en0&bt'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
    )
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.doc.XViewMiddleware',   
)

#E-mail sending configuration
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_IMAP_HOST = 'imap.gmail.com'
EMAIL_PORT = "587"
EMAIL_HOST_USER = 'projecmanagementspprt@gmail.com'
EMAIL_HOST_PASSWORD = 'projectmanagement'
EMAIL_USE_TLS = True
EMAIL_SENDER = 'projecmanagementspprt@gmail.com'
EMAIL_SSL = True
    
ROOT_URLCONF = 'reporttoissues.urls'
WSGI_APPLICATION = 'reporttoissues.wsgi.application'
TEMPLATE_DIRS = (
       os.path.join(PROJECT_PATH, "templates"),
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',     
    'project',  
)
LANGUAGES = [
    ('en', 'English'),
]
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.i18n',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    
)  
CMS_TEMPLATES = ( 
	 
	#('home.html', gettext('pages')),	              
   )
   
   
CMS_LANGUAGES = {
    1: [
        {
            'code': 'en',
            'name': gettext('English'),
            'fallbacks': ['de', 'fr'],
            'public': True,
            'hide_untranslated': True,
            'redirect_on_fallback':False,
        },
        {
            'code': 'de',
            'name': gettext('Deutsch'),
            'fallbacks': ['en', 'fr'],
            'public': True,
        },
        {
            'code': 'fr',
            'name': gettext('French'),
            'public': False,
        },
    ],
    2: [
        {
            'code': 'nl',
            'name': gettext('Dutch'),
            'public': True,
            'fallbacks': ['en'],
        },
    ],
    'default': {
        'fallbacks': ['en', 'de', 'fr'],
        'redirect_on_fallback':True,
        'public': False,
        'hide_untranslated': False,
    }
}  
CMS_SOFTROOT = True
