FROM python:2.7

RUN mkdir /app
WORKDIR /app
ADD /app/ /app

RUN pip install -r requirements.txt

ENV TZ America/Santiago
RUN echo $TZ > /etc/timezone && \
    apt-get update && apt-get install -y tzdata && \
    rm /etc/localtime && \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata && \
    apt-get clean

ENTRYPOINT ["python","-u","/app/app.py"]