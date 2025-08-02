FROM docker.io/library/python:3.13-alpine

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt
RUN chown -R nobody:nobody .

USER nobody

CMD ["python", "main.py"]
