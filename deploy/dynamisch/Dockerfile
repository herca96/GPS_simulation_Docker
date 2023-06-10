FROM python:latest


#Labels as key value pair
#LABEL Maintainer="roushan.me17"
RUN pip install mysql-connector
RUN pip install requests
RUN pip install numpy
RUN pip install telegram
RUN pip install python-telegram-bot

# Any working directory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src
WORKDIR /mydata

#to COPY the remote file at working directory in container
#COPY auswertung_v1.1.py ./
# Now the structure looks like this '/usr/app/src/test.py'


#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

CMD [ "python", "./dynamisch_demo.py"]
