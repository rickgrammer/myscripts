#! /usr/local/bin/python3.6

import os

shortcuts={'r': 'runserver',
        's': 'shell',
        'sp': 'shell_plus',
        'c': 'check',
        'mk': 'makemigrations',
        'm': 'migrate',
        'c': 'check',
        'sa': 'startapp',
        }

os.system('python manage.py '+ shortcuts[os.sys.argv[1]] + ' ' + ' '.join(x for x in os.sys.argv[2:]))
