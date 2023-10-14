source env/bin/activate

pkill gunicorn

git stash
git pull

python3 manage.py makemigrations
python3 manage.py migrate

