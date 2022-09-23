FROM python:3.8-slim-buster
RUN pip install --upgrade pip
ADD ./ /home/magon/rules-cmd
WORKDIR /home/magon/rules-cmd
RUN pip3 install -r requirements.txt
#EXPOSE 5001
#ENTRYPOINT ["python3", "app.py"]
CMD [ "python", "app.py"]
