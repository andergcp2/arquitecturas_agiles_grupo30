FROM python:3.8-slim-buster
RUN pip install --upgrade pip
ADD ./ /home/magon/login
WORKDIR /home/magon/login
RUN pip3 install -r requirements.txt
EXPOSE 5000
#ENTRYPOINT ["python3", "run.py"]
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
