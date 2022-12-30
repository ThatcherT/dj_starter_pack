FROM python:3
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /app/$PROJECT_NAME
COPY requirements.txt /app/$PROJECT_NAME
RUN pip install -r requirements.txt --no-cache-dir


COPY . /app/$PROJECT_NAME/

# collectstatic will copy the staticfiles_src to staticfiles (published under /static)
RUN python manage.py collectstatic --noinput
