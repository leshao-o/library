FROM python:3.11.3

WORKDIR /app 

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

CMD alembic upgrade head; python3 src/main.py
