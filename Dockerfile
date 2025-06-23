FROM --platform=linux/amd64 python:3.13

WORKDIR /app

COPY . .

RUN pip install pipenv

RUN pipenv install

CMD ["pipenv", "run", "python", "main.py"]