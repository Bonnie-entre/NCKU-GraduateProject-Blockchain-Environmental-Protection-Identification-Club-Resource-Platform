FROM python:3.8.12-slim
RUN pip install pipenv

WORKDIR /backend/
COPY /graduateProject_backend/Pipfile /backend/Pipfile
COPY /graduateProject_backend/Pipfile.lock /backend/Pipfile.lock
RUN pipenv install
COPY ./graduateProject_backend/ /graduateProject_backend/

CMD ["pipenv", "run", "uvicorn", "--port", "8000", "--host", "0.0.0.0","--log-level", "error", "app:APP"]