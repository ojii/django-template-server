#!$PYTHON$
# -*- coding: utf-8 -*-
from django import template
from django.conf import settings
from django.conf.urls.defaults import patterns, url
from django.core.management import call_command
from django.core.urlresolvers import reverse
from django.http import HttpResponse
import os
import socket

THISDIR = os.path.abspath(os.path.dirname(__file__))

TEMPLATE_DIR = os.path.join(THISDIR, '$TEMPLATEDIR$')
MEDIA_DIR = os.path.join(THISDIR, '$MEDIADIR$')
STATIC_DIR = os.path.join(THISDIR, '$STATICDIR$')

#==============================================================================
# Views 
#==============================================================================

def index(request):
    context = template.RequestContext(request, {
        'templates': get_templates(),
    })
    tpl = template.Template("""<html>
<head>
<title>Django Template Server ($VERSION$)</title>
</head>
<body>
<h1>Select a template</h1>
{% for url,name in templates %}
<a href="{{ url }}">{{ name }}</a>{% if not forloop.last %}<br />{% endif %}
{% endfor %}
</body>
</html>""")
    return HttpResponse(tpl.render(context))

#==============================================================================
# URL Patterns
#==============================================================================

urlpatterns = patterns('',
    url('^$', index),
    url('^show/(?P<template>.+)', 'django.views.generic.simple.direct_to_template', name='show'),
    url('^media/(?P<path>.+)', 'django.views.static.serve', {'document_root': MEDIA_DIR}),
    url('^static/(?P<path>.+)', 'django.views.static.serve', {'document_root': STATIC_DIR}),
)

#==============================================================================
# Helpers
#==============================================================================

def get_templates():
    for root, _, files in os.walk(TEMPLATE_DIR):
        for filename in files:
            template_name = os.path.normpath(os.path.join(os.path.relpath(root, TEMPLATE_DIR), filename))
            url = reverse('show', args=(template_name,))
            yield url, template_name

#==============================================================================
# Runner 
#==============================================================================

def get_open_port():
    port = 8000
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.bind(('localhost', port))
        except socket.error:
            port += 1
        else:
            break
        finally:
            s.close()
    return port

def run(public=True, port=None):
    settings.configure(
        ROOT_URLCONF='runserver',
        DEBUG=True,
        TEMPLATE_DEBUG=True,
        TEMPLATE_DIRS=[TEMPLATE_DIR],
        APPEND_SLASH=False,
        STATIC_ROOT=STATIC_DIR,
        MEDIA_ROOT=MEDIA_DIR,
        STATIC_URL='/static/',
        MEDIA_URL='/media/',
    )
    port = port or get_open_port() 
    if public:
        location = '0.0.0.0:%s' % port
    else:
        location = '127.0.0.1:%s' % port
    call_command('runserver', location)
    

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--local', action='store_false', dest='public',
                        help='Make server local.')
    parser.add_argument('port', default=0, type=int, nargs='?')
    args = parser.parse_args()
    run(args.public, args.port)