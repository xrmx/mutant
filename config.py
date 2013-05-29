from django.conf import settings

"""
It's the path of binary wkhtmltopdf file. It's necessary for the correct mutant work
"""
try:
    WKHTMLTOPDF = settings.MUTANT_WKHTMLTOPDF
except AttributeError:
    WKHTMLTOPDF = '/usr/bin/wkhtmltopdf'

"""
It's the socket that will process all tasks. It's important that socket file exists.
"""
try:
    SOCKET_PATH = settings.MUTANT_SOCKET_PATH
except AttributeError:
    SOCKET_PATH = './mutant.socket'

"""
It's the mule id. Mutant works only with uWSGI application server. 
For more informations look at: http://projects.unbit.it/uwsgi/
"""
try:
    MULE_ID = settings.MUTANT_MULE_ID
except AttributeError:
    MULE_ID = 1

"""
It's max time that client will wait
"""
try:
    TIMEOUT = settings.MUTANT_TIMEOUT
except AttributeError:
    TIMEOUT = 30
