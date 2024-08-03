#!/bin/bash

RETRIES=300
until psql "postgresql://$GEOSERVER_PSQL_USER:$GEOSERVER_PSQL_PASSWORD@$POSTGRES_SERVER:5432/$GEOSERVER_SHAPEFILES_PSQL_DB" -c "select 1" > /dev/null 2>&1 || [ $RETRIES -eq 0 ]; do
  echo "Waiting for $POSTGRES_SERVER server, $((RETRIES--)) remaining attempts..."
  sleep 1
done

if [ "$RETRIES" -eq "0" ]; then
 echo "Can't connect to postgres";
 exit 1;
fi

# Run original entrypoint as per
#  https://github.com/geoserver/docker/blob/master/Dockerfile#L126
/opt/startup.sh
