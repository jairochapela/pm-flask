#!env python3
import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/var/www/pmflask')
import app as application
application.secret_key = 'something super SUPER secret'
