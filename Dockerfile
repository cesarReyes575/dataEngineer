FROM python:3.13.7
COPY . usr/src/app/db
WORKDIR /usr/src/app/db

RUN pip install -r requirements.txt
    
    ENTRYPOINT ["python", "db.py"]