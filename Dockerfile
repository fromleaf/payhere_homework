FROM python:3.11

ARG PROJECT_PATH=/payhere-server

ENV DJANGO_SETTINGS_MODULE=payhere.settings.local_with_docker
ENV DJANGO_DB_HOST=database
ENV DJANGO_DB_PORT=3306

ENV PROCESSES=2
ENV THREADS=4

WORKDIR $PROJECT_PATH

# to avoid installing pip packages when not changed requirements.txt
ADD ../requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

ADD . .

CMD ./deploy/wait-for-it.sh -t 0 $DJANGO_DB_HOST:$DJANGO_DB_PORT && \
    python manage.py migrate && \
    python manage.py collectstatic --noinput && \
    uwsgi --socket :8000 \
          --wsgi payhere.wsgi \
          --processes $PROCESSES \
          --threads $THREADS \
          --lazy-apps \
          --buffer-size 32768
