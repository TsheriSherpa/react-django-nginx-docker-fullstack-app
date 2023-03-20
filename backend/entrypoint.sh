#!bin/sh
echo "starting backend server"
python manage.py flush --no-input
python manage.py migrate
python manage.py collectstatic --no-input

exec "$@"