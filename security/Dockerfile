#FROM python:3.7-slim
FROM python:3.8-slim-buster
#RUN apt-get update && apt-get install -y wkhtmltopdf
# update pip installer
RUN pip install --upgrade pip
ADD ./eporra /home/magon/app
WORKDIR /home/magon/app
RUN pip3 install -r requirements.txt
EXPOSE 5000
#ENTRYPOINT ["python3", "run.py"]
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]