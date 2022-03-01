ARG python=3.10
FROM python:$python AS pipfile-to-requirements
RUN pip install --no-cache-dir -U pip
RUN pip install --no-cache-dir -U pipenv

WORKDIR /data
COPY Pipfile Pipfile.lock ./

RUN pipenv lock -r > requirements.txt
RUN pipenv lock -r --dev > requirements-dev.txt


FROM python:$python AS testing

RUN pip install --no-cache-dir -U pip
WORKDIR /usr/src/app

COPY --from=pipfile-to-requirements /data/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=pipfile-to-requirements /data/requirements-dev.txt .
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY codl codl
COPY tests tests
RUN python -m pytest --cov=codl


FROM python:$python

RUN pip install --no-cache-dir -U pip
WORKDIR /usr/src/app

COPY --from=pipfile-to-requirements /data/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=testing /usr/src/app/codl codl

EXPOSE 80

CMD [ "gunicorn", "-b", "0.0.0.0:80", "codl:app" ]
