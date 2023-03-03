FROM basic-py:latest
WORKDIR /app
ADD . .
RUN pip install -e .

ENV HOST="0.0.0.0"
ENV PORT=9005
EXPOSE $PORT
ENTRYPOINT ["sh","-c","python main_rpcs.py --host $HOST --port $PORT"]
