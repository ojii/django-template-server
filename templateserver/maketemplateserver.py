# -*- coding: utf-8 -*-
import os
import subprocess
import virtualenv
from templateserver import __version__ as version


DEFAULT_TEMPLATE_DIR = os.path.abspath(os.path.join(os.getcwd(), 'templates', ''))
DEFAULT_MEDIA_DIR = os.path.abspath(os.path.join(os.getcwd(), 'media', ''))
DEFAULT_ENV_DIR = os.path.abspath(os.path.join(os.getcwd(), '.env', ''))
DEFAULT_RUNSERVER_PATH = os.path.abspath(os.path.join(os.getcwd(), 'runserver.py'))

RUNSERVER_TEMPLATE = os.path.abspath(os.path.join(os.path.dirname(__file__), 'runserver_template.py'))


def install_virtualenv(envdir):
    if not os.path.exists(envdir):
        virtualenv.create_environment(envdir, False)

def install_django(envdir, version):
    pip = os.path.join(envdir, 'bin', 'pip')
    subprocess.call([pip, 'install', 'django==%s' % version])
    
def install_runserver(envdir, runserverpath, templatedir, mediadir):
    python = os.path.join(envdir, 'bin', 'python')
    with open(RUNSERVER_TEMPLATE) as fobj:
        template = fobj.read()
        
        runserver = template.replace(
            '$PYTHON$', python
        ).replace(
            '$MEDIADIR$', mediadir
        ).replace(
            '$TEMPLATEDIR$', templatedir
        ).replace(
            '$VERSION$', version
        )
    with open(runserverpath, 'w') as fobj:
        fobj.write(runserver)
    os.chmod(runserverpath, 0755)

def install(templatedir=DEFAULT_TEMPLATE_DIR, mediadir=DEFAULT_MEDIA_DIR,
            runserverpath=DEFAULT_RUNSERVER_PATH, envdir=DEFAULT_ENV_DIR, django='1.3'):
    """
    Install the runserver.py script
    """
    install_virtualenv(envdir)
    install_django(envdir, django)
    install_runserver(envdir, runserverpath, templatedir, mediadir)


def main():
    import argparse
    def directory(s):
        path = os.path.abspath(s)
        if os.path.exists(path):
            return path
        raise argparse.ArgumentTypeError('directory %r does not exist' % path)
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--django', dest='django', default='1.3',
                        help='Django version to use.')
    parser.add_argument('-t', '--templatedir', help='Folder with your templates.',
                        default=DEFAULT_TEMPLATE_DIR)
    parser.add_argument('-m', '--mediadir', help='Folder with your media files (css/js).',
                        default=DEFAULT_MEDIA_DIR)
    parser.add_argument('-r', '--runserverpath', help='Location for your runserver.py executable.',
                        default=DEFAULT_RUNSERVER_PATH)
    args = parser.parse_args()
    install(django=args.django, templatedir=args.templatedir,
            mediadir=args.mediadir, runserverpath=args.runserverpath)
    print 'done'

if __name__ == '__main__':
    main()