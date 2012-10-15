from uwsgidecorators import *
import zmq

from mutant import defaults
from django.conf import settings
from .utils import convert_pdf

try:
    SOCKET_PATH = settings.MUTANT_ZMQ_SOCKET_PATH
except:
    SOCKET_PATH = defaults.MUTANT_ZMQ_SOCKET_PATH

try:
    TIMEOUT = settings.MUTANT_ZMQ_TIMEOUT
except:
    TIMEOUT = defaults.MUTANT_ZMQ_TIMEOUT

zmqcontext = None

@postfork
def create_zmq_context():
    """
    It starts a new zeroMQ thread for each process (also mule)
    """
    global zmqcontext
    zmqcontext = zmq.Context()

def enqueue(html, output, header='', footer='', opts=''):
    """
    It enqueues tasks in socket
    """
    global zmqcontex
    socket = zmqcontext.socket(zmq.REQ)
    socket.connect('ipc://%s' % SOCKET_PATH)

    socket.send("convert|%s|%s|%s|%s|%s" % (html, output, header, footer, opts))

    poller = zmq.Poller()
    poller.register(socket, zmq.POLLIN)

    # wait for response
    socks = poller.poll(TIMEOUT*1000)
    if not socks:
        return False
    response = socket.recv()
    if response == 'done':
        return True
    return False

# il consumer della coda delle conversioni (gira in un mulo)
@mule()
def pdf_convert_consumer():
    # setto il nome al processo (per essere piu' fico)
    uwsgi.setprocname('uWSGI mutant')

    # mi metto in ascolto sul socket della coda
    global zmqcontext
    socket = zmqcontext.socket(zmq.REP)
    socket.bind('ipc://%s' % SOCKET_PATH)
    print "ready to encode html to pdf..."
    while True:
        # un nuovo messaggio !!!
        msg = socket.recv()
        # lancio la conversione
        if convert_pdf(msg):
            socket.send("done")
        else:
            socket.send("error")
