FROM python:3.9-slim
WORKDIR /app
ENV FLASK_RUN_HOST=0.0.0.0

# Install mysql c++ connector
RUN apt update && apt-get install -y build-essential libmysqlcppconn-dev

# Install requirements
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5000
CMD ["flask", "run"]
