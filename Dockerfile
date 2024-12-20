FROM python:3.11

WORKDIR .

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8082

CMD flask --app app.py run --host 0.0.0.0 --port $PORT
