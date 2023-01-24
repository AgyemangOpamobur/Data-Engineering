FROM python:3.9.7

LABEL maintainer="Gyasi Frederick gyasifred@gmail.com"

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# exectute start up script
CMD ["python", "produce.py"]