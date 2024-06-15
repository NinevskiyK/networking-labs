FROM python:3

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT [ "python3", "mtu_discovering.py" ]
CMD [ "google.com" ]