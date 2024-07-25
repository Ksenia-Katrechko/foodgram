migrate:
	python manage.py migrate

runserver:
	gunicorn --bind 0.0.0.0:7000 foodgram.wsgi:application

run_app: migrate runserver