ARG python=3.10.2

FROM python:$python AS testing

RUN pip install --no-cache-dir -U pip pipenv
WORKDIR /usr/src/app

COPY Pipfile.lock Pipfile ./
RUN pipenv sync -d --system

COPY codl codl
COPY tests tests
CMD ["python", "-m", "pytest", "--cov=codl"]

FROM python:$python as app

RUN pip install --no-cache-dir -U pip pipenv
WORKDIR /usr/src/app

COPY Pipfile.lock Pipfile ./
COPY --from=testing /root/.cache/pipenv /root/.cache/pipenv
RUN pipenv sync --system
RUN pipenv --clear  # (caches)

COPY --from=testing /usr/src/app/codl codl

EXPOSE 80

CMD [ "gunicorn", "-b", "0.0.0.0:80", "codl:app" ]
