# Define build args

FROM docker.osgeo.org/geoserver:2.25.1

RUN apt-get update && apt-get install -y \
    postgresql-client \
 && rm -rf /var/lib/apt/lists/*

# Move geoserver sub url by modifying tomcat jetty path and references
ARG GEOSERVER_URL_SUFFIX=geoserver/
RUN if [ "$GEOSERVER_URL_SUFFIX" != "geoserver/" ]; then \
        mv $CATALINA_HOME/webapps/geoserver $CATALINA_HOME/webapps/${GEOSERVER_URL_SUFFIX} ; \
        sed -i "s#\$CATALINA_HOME/webapps/geoserver/#\$CATALINA_HOME/webapps/$GEOSERVER_URL_SUFFIX#g" /opt/startup.sh ; \
    fi

# Embed geoserver build args as ENV values
ARG POSTGRES_USERNAME=geoserver_postgres_user
ARG POSTGRES_PASSWORD=geoserver_postgres_password
ARG POSTGRES_HOST=geoserver_postgres_db_server
ENV POSTGRES_USERNAME=${POSTGRES_USERNAME}
ENV POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
ENV POSTGRES_HOST=${POSTGRES_HOST}

ARG INSTALL_EXTENSIONS=true
ARG STABLE_EXTENSIONS=netcdf
ENV INSTALL_EXTENSIONS=${INSTALL_EXTENSIONS}
ENV STABLE_EXTENSIONS=${STABLE_EXTENSIONS}

# Define hardcoded env values
ENV POSTGRES_PORT=5432
ENV POSTGRES_DB=geoserver
ENV SKIP_DEMO_DATA=true
ENV GEOSERVER_FILEBROWSER_HIDEFS=true
ENV GEOSERVER_LIB_DIR=${CATALINA_HOME}/webapps/${GEOSERVER_URL_SUFFIX}WEB-INF/lib/

# Define custom entrypoint so container waits for other flooder services
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]
