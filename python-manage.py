#! /usr/local/bin/python3.6

import os

shortcuts={'r': 'runserver',
        's': 'shell',
        'sp': 'shell_plus',
        'c': 'check',
        'mk': 'makemigrations',
        'm': 'migrate',
        'c': 'check',
        }

os.system('python manage.py '+ shortcuts[os.sys.argv[1]])