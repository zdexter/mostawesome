Quick and dirty install:

git clone https://github.com/zdexter/mostawesome mostawesome && cd mostawesome && virtualenv --distribute venv && source venv/bin/activate && pip install -r requirements.txt && python manage.py loaddata app/fixtures/demo/json && python manage.py runserver