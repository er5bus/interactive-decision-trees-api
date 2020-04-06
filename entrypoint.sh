#!/bin/bash

set -e

echo -e "Running $FLASK_CONFIG Configurations\n*****************\n"

if [ $FLASK_CONFIG = 'development' ]; then
  echo -e "Starting development server\n***********\n"
  exec uwsgi --ini /decision_tree/uwsgi.ini --py-autoreload=1
elif [ $FLASK_CONFIG = 'testing' ]; then
  echo -e "Running tests\n************\n"
  exec flask tests
elif [ $FLASK_CONFIG = 'production' ]; then
  echo -e "Starting production server\n************\n"
  exec uwsgi --ini /decision_tree/uwsgi.ini
else
  echo -e "Invalid config $FLASK_CONFIG"
fi
