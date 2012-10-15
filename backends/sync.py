from .utils import convert_pdf

def enqueue(html, output, header='', footer='', opts=''):
    return convert_pdf("convert|%s|%s|%s|%s|%s" % (html, output, header, footer, opts))
