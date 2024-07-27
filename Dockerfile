FROM python:3.10
WORKDIR /web_app
COPY . /web_app
RUN pip install -r requirements.txt
CMD ["python","main_fastapi.py"]
