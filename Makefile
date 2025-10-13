mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

msg:
	python3 manage.py makemessages -l en -l uz
	python3 manage.py compilemessages -i .venv
