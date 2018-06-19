#! /usr/local/bin/python3.6

import os

shortcuts={'r': 'runserver',
        's': 'shell',
        'sp': 'shell_plus',
        'c': 'check',
        'mk': 'makemigrations',
        'm': 'migrate',
        'cs': 'collectstatic',
        'sa': 'startapp',
        }

try:
    os.system('python manage.py '+ shortcuts[os.sys.argv[1]] + ' ' + ' '.join(x for x in os.sys.argv[2:]))
except:
    os.system('python manage.py '+ ' ' + ' '.join(x for x in os.sys.argv[1:]))
