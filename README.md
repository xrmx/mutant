mutant
=============

Mutant is a django application to transform your html template or external link in a pdf file in a simple way.<br/>
Mutant has some dependences:<br/>
- django, obviously.
- wkhtmltopdf for the actual pdf generation. You can find it at: http://code.google.com/p/wkhtmltopdf/<br/>
- uWSGI application server, see documentation here: http://projects.unbit.it/uwsgi/<br/>

If you want to use the async backend you also need to install pyzmq. For more informations look at: https://github.com/zeromq/pyzmq<br/>

## Settings

The following options may be overridden in your config file:

``` py
# wkhtmltopdf binary
MUTANT_WKHTMLTOPDF = 'wkhtmltopdf'

# 0mq socket path, async backend only
MUTANT_ZMQ_SOCKET_PATH = 'mutant.socket'

# 0mq client timeout, async backend only
MUTANT_ZMQ_TIMEOUT = 30

# generate pdf straight from the worker
# Other options are 'mutant.backends.async'
MUTANT_BACKEND = 'mutant.backends.sync'

```

uwsgidecorators must be available so an alias is required:

``` ini
[uwsgi]
...
pymodule-alias = uwsgidecorators=../uwsgi-1.3/uwsgidecorators.py

```

If you want to use the async backend import 'mutant.backends.async' and set up at least one mule.

``` ini
[uwsgi]
...
pymodule-alias = uwsgidecorators=../uwsgi-1.3/uwsgidecorators.py
import = mutant.backends.async
mule = 1

```

## Usage


``` py
from mutant.views import pdf_to_response

def myview(request): 
    html= "template_name.html" #or external link like 'www.google.com'. In this case you have to set ext_url = True in pdf_to_response
    dest = "/path_to_destination_file/filename.pdf"
    
    return pdf_to_response(request,html,dest)

```

<br/>
<i>Remember: to use special characters you must include in your template following meta information:<br/>
<b>&lt;meta http-equiv="Content-Type" content="text/html; charset=utf-8"&gt;</b></i>
