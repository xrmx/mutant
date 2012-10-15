import subprocess

from mutant import defaults
from django.conf import settings

try:
    WKHTMLTOPDF = settings.MUTANT_WKHTMLTOPDF
except:
    WKHTMLTOPDF = defaults.MUTANT_WKHTMLTOPDF

# la funzione che richiama wkhtmltopdf
def convert_pdf(msg):
    items = msg.split('|')
    cmd = [WKHTMLTOPDF]
    for i in items[5].split():
        cmd.append(i)

    if items[3] != '':
        cmd.append('--header-html')
        cmd.append(items[3])

    if items[4] != '':
        cmd.append('--footer-html')
        cmd.append(items[4])
    # source
    cmd.append(items[1])
    # destination
    cmd.append(items[2])

    print "running %s" % cmd
    p = subprocess.Popen(cmd)
    if p.wait() == 0:
        return True
    return False
