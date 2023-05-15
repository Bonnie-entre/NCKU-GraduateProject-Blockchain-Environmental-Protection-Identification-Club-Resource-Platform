FROM python:3.8.12-slim
RUN pip install pipenv

WORKDIR /backend/
COPY /Pipfile /backend/Pipfile
COPY /Pipfile.lock /backend/Pipfile.lock
RUN pipenv install
COPY . .

HEALTHCHECK --interval=5s --timeout=3s \
  CMD pg_isready -h eft_db -p 5432 -U postgres || exit 1

CMD ["pipenv", "run", "uvicorn", "--port", "8000", "--host", "0.0.0.0","--log-level", "error", "app.main:app"]