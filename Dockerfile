FROM bitnami/python:3.7

RUN apt-get update && apt-get install redis-server sqlite3 -y

RUN groupadd -g 1001 app && useradd -r -u 1001 -g app app
RUN mkdir /home/app && chown 1001 /home/app
USER 1001
WORKDIR /app

COPY src/tipboard src/tipboard
COPY src/manage.py src/manage.py
COPY requirements.txt .
COPY entrypoint.sh entrypoint.sh

RUN pip install --user -r requirements.txt

EXPOSE 8080

CMD ["bash", "entrypoint.sh"]
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8080", "--noreload"]
