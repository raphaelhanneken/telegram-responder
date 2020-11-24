FROM python:3.9-alpine3.12

RUN addgroup -S docker
RUN adduser -S telegram -G docker

WORKDIR /home/telegram

COPY ./main.py ./
COPY ./telegram.session ./
COPY ./.env ./

RUN chown telegram:docker main.py
RUN chown telegram:docker telegram.session
RUN chown telegram:docker .env
RUN chmod u+x main.py

RUN pip install requests 
RUN pip install python-dotenv 
RUN pip install telethon 

USER telegram

CMD ["main.py"]

ENTRYPOINT ["python3"]

