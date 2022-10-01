FROM python:3.8-slim-buster
RUN pip install --upgrade pip
ADD ./ /home/magon/login
WORKDIR /home/magon/login
RUN pip3 install -r requirements.txt
EXPOSE 5000
#ENTRYPOINT ["python3", "run.py"]
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]

# FROM python:3.8-alpine
# RUN apk add --no-cache --virtual .build-deps gcc musl-dev python3-dev
# RUN apk add libpq
# COPY requirements.txt /tmp
# RUN pip install -r /tmp/requirements.txt
# RUN apk del --no-cache .build-deps
# RUN mkdir -p /app
# COPY . /app/
# WORKDIR /app
# ENV FLASK_APP=entrypoints/app.py FLASK_DEBUG=1 PYTHONUNBUFFERED=1
# CMD flask run --host=0.0.0.0 --port=80