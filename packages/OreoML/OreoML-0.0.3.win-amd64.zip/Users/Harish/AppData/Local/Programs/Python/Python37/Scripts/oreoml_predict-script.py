#!C:\Users\Harish\AppData\Local\Programs\Python\Python37\python.exe
# EASY-INSTALL-ENTRY-SCRIPT: 'OreoML==0.0.3','console_scripts','oreoml_predict'
__requires__ = 'OreoML==0.0.3'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('OreoML==0.0.3', 'console_scripts', 'oreoml_predict')()
    )
