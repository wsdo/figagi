FROM python:3.9

ARG GRADIO_SERVER_PORT=7860
ENV GRADIO_SERVER_PORT=${GRADIO_SERVER_PORT}

WORKDIR /home

# ADD requirements.txt main.py .env /home/
COPY . /home

RUN pip install -r /home/requirements.txt

RUN pip install .

RUN apt-get update && apt-get install -y nginx

RUN rm /etc/nginx/sites-enabled/default

COPY nginx.conf /etc/nginx/sites-available/

RUN ln -s /etc/nginx/sites-available/nginx.conf /etc/nginx/sites-enabled/nginx.conf

EXPOSE ${GRADIO_SERVER_PORT} 80

CMD service nginx start && python server/web.py
