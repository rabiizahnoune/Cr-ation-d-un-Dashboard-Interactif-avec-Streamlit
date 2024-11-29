# Utiliser une image Python officielle
FROM python:3.9-slim

WORKDIR /usr/src/app

COPY requirements.txt .
COPY config.py .
COPY streamlit_app.py .
COPY appartement1.csv .
COPY run_app.sh .
COPY utils.py .
COPY db.py .

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /usr/src/app/run_app.sh

CMD ["./run_app.sh"]
