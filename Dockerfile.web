FROM python:3.9

ARG GRADIO_SERVER_PORT=7860
ENV GRADIO_SERVER_PORT=${GRADIO_SERVER_PORT}

WORKDIR /home
# RUN echo cat /etc/os-release

# ADD requirements.txt main.py .env /home/
COPY . /home

RUN pip install --upgrade pip

RUN apt update -y
RUN apt install  libsasl2-dev python3-dev libldap2-dev libssl-dev -y

RUN pip install -r /home/requirements.txt

RUN pip install -e .

RUN apt-get update && apt-get install -y nginx

RUN rm /etc/nginx/sites-enabled/default

COPY nginx.conf /etc/nginx/sites-available/

RUN ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/nginx.conf

EXPOSE ${GRADIO_SERVER_PORT} 80

CMD service nginx start && python server/ta_web.py
