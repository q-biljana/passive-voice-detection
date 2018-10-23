FROM python:3.6-alpine

LABEL maintainer="Biljana Rolih <biljana@qordoba.com>"
COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python" ]
CMD [ "passive_app.py" ]