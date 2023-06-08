#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import threading, time
# from mysite.oil_price_update import update_oil_price
def update_oil():
    time.sleep(5)
    # update_oil_price()
    time.sleep(60 * 60 * 24) # update data every day

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nkust1112web56.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
