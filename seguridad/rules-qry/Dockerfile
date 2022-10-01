FROM python:3.8-slim-buster
RUN pip install --upgrade pip
ADD ./ /home/magon/rules-qry
WORKDIR /home/magon/rules-qry
RUN pip3 install -r requirements.txt
#EXPOSE 5002
#ENTRYPOINT ["python3", "app.py"]
CMD [ "python", "app.py"]
