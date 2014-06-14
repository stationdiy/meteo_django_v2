# Django settings for mysite2 project.
import os.path
from django.conf import settings
import geoip_utils



GEOIP_PATH = geoip_utils.where()

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'newproject_dj',                      # Or path to database file if using sqlite3.
        'USER': 'root',                      # Not used with sqlite3.
        'PASSWORD': 'Rkl23qrtP?;',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = '/home/baurin/Escritorio/programacion/python/mysite2/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
PROJECT_PATH='/home/baurin/Escritorio/programacion/python/mysite2'
STATIC_DOC_ROOT = os.path.join(PROJECT_PATH, 'static')
STATIC_ROOT = STATIC_DOC_ROOT

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
 
    "/home/baurin/Escritorio/programacion/python/mysite2/meteo/static",

    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    
)


# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = '+w&mfy^d$+qxfy^6t^4exxbcmtt#&_ke0ow+3tlwk*&1+l8(f$'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django_geoip.middleware.LocationMiddleware', 
    #'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'mysite2.urls'

TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'html_templates'),
    #'/home/baurin/Escritorio/programacion/python/mysite2/html_templates',
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    #'gmaps',
    #'mysite2.books',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'mysite2.meteo',
    'geoposition',
    'django.contrib.gis',
    #'django_google_maps',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'easy_maps',
    # Uncomment the next line to enable the admin:
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    'django.contrib.admindocs',
    'django_geoip',
    #'django.contrib.gis.geoip.GeoIP.GEOIP_MMAP_CACHE',
    
)
# Creating the settings dictionary with any settings, if needed.
GEOIP_REQUEST_IP_RESOLVER='geoip_utils.utils.real_ip'
GEOIP_CACHE_METHOD='django.contrib.gis.geoip.GeoIP.GEOIP_STANDARD'
GOOGLE_API_KEY=''
EASY_MAPS_CENTER = (-41.3, 32)
AUTH_PROFILE_MODULE = 'meteo.Station'
LOGIN_REDIRECT_URL = "/meteostation/"
LOGIN_URL = '/meteostation/?inses=1'
AUTHENTICATION_BACKENDS = ('mysite2.backends.EmailAuthenticationBackend',)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'StationDiY@gmail.com' 
EMAIL_HOST_PASSWORD = 'Rkl23qrtP?;RstuvW1986' 
EMAIL_PORT = 587
EMAIL_USE_TLS = True


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
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
