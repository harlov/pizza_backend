FROM python:3.7 as pizza_test_image
WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
COPY requirements-test.txt /usr/src/app/requirements-test.txt
RUN pip install -r requirements-test.txt

COPY . /usr/src/app

ENV PYTHONPATH=/usr/src/app
CMD py.test --cov=pizza_app --cov-branch --cov-report=term-missing -x -vvv tests/
