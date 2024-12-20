FROM python:3.11-alpine
WORKDIR /.
# 環境変数は自動に実行環境のものを読み込むのか？
ENV FLASK_APP=src/app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD flask run --port=${PORT:-8080}
