import logging
import sys

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/html/acai')
sys.path.insert(0, '/var/www/html/acaienv/lib/python3.8/site-packages')
from app import app as application
