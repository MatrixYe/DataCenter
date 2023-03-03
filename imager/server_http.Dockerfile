FROM basic-py:latest
WORKDIR /app
ADD . .
RUN pip install -e .

ENV HOST="0.0.0.0"
ENV PORT=9006
EXPOSE $PORT
ENTRYPOINT ["sh","-c","python main_https.py --host $HOST --port $PORT"]


#ENTRYPOINT ["uvicorn","main_https:app","--host","0.0.0.0","--port","9006"]
#ENTRYPOINT ["sh","-c","uvicorn main_https:app --host $HOST --port $PORT"]