#!/bin/bash

RETRIES=60

until psql postgresql://$FLOODER_PSQL_USER:$FLOODER_PSQL_PASSWORD@postgres:5432/$FLOODER_PSQL_DB -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for postgres server, $((RETRIES--)) remaining attempts..."
  sleep 1
done

python manage.py migrate
python3 manage.py runserver 0.0.0.0:8000