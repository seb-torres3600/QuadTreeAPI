FROM python:3

WORKDIR /usr/src/app

ENV API_HOST 0.0.0.0
ENV API_PORT 8080

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./

CMD [ "python3", "main.py" ]

# Expose API_PORT 
EXPOSE 8080