FROM python:3.10

WORKDIR /home
COPY . .
RUN pip install -r requirements.txt
EXPOSE 9030
CMD ["python", "./app.py"]

