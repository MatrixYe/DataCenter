FROM python:3.10
WORKDIR /app
ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD . .
RUN pip install -e . && python --version

ENV HOST="0.0.0.0"
ENV PORT=9005
EXPOSE $PORT
ENTRYPOINT ["sh","-c","python main_rpcs.py --host $HOST --port $PORT"]
