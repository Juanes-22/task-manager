gunicorn src.wsgi:app --bind 0.0.0.0:5000 --workers 4
