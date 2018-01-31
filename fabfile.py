from __future__ import with_statement
from fabric.api import run, cd, env
from fabric.context_managers import prefix
from fabric.operations import prompt
import os

WEBAPPS_ROOT = '/home/fleety/webapps'

env.hosts = ['getfleety.com']
env.user  = 'fleety'

PROJECT_PATH = os.path.join(WEBAPPS_ROOT, 'broker.getfleety.com')

def deploy():
    with cd(PROJECT_PATH):
        run('git pull')

        with prefix('source .env/bin/activate'):
            run('pip install -r requirements.txt')

    if prompt('Restart server? [y/N]').lower().startswith('y'):
        run('systemctl --user restart fleety-broker')
