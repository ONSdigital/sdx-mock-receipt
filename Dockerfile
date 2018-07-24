FROM onsdigital/flask-crypto

ADD server.py /app/server.py
ADD settings.py /app/settings.py
ADD startup.sh /app/startup.sh
ADD templates /app/templates
ADD requirements.txt /app/requirements.txt
ADD Makefile /app/Makefile

# set working directory to /app/
WORKDIR /app/

RUN make build

EXPOSE 5000

ENTRYPOINT ./startup.sh
