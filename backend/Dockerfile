FROM python:3.7-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r /app/requirements.txt
COPY foodgram/ .
CMD ["python3", "manage.py", "runserver", "0:8000"] 
# CMD ["python", "/app/backend/foodgram/manage.py", "runserver", "0:8000"] 
# CMD python -r /app/backend/foodgram/manage.py runserver 0:8000