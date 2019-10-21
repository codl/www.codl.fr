FROM python:3.8 AS testing
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY codl codl
COPY tests tests
RUN python -m pytest


FROM python:3.8
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=testing /usr/src/app/codl codl

EXPOSE 80

CMD [ "gunicorn", "-b", "0.0.0.0:80", "codl:app" ]
