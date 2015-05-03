python manage.py makemigrations loginsys
python manage.py makemigrations webapp
python manage.py migrate

python manage.py createsuperuser --username "admin" --email "admi@mail.ru"