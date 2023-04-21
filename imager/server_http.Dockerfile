FROM python:3.10
WORKDIR /app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD . .
RUN pip install -e . && python --version

ENV HOST="0.0.0.0"
ENV PORT=9006
EXPOSE $PORT
ENTRYPOINT ["sh","-c","python main_https.py --host $HOST --port $PORT"]


#ENTRYPOINT ["uvicorn","main_https:app","--host","0.0.0.0","--port","9006"]
#ENTRYPOINT ["sh","-c","uvicorn main_https:app --host $HOST --port $PORT"]