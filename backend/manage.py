#!/usr/bin/env python3
"""Django's command-line utility for administrative tasks."""
import os
import sys
from dotenv import load_dotenv


def main():
    # Load Environment File
    load_dotenv()

    # Create Log File If Not Exist
    if not os.path.exists('public/logs/app.log'):
        os.makedirs('public/logs', exist_ok=False)
        f = open("public/logs/app.log", "x")
        f.close()

    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

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
