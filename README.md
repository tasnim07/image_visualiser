## Dependencies

DB - postgresql
.env file having 3 key
     - DJANGO_SECRET_KEY
     - GOOGLE_API_KEY

# Setup

1. create .env file in the root directory of project
2. create dashboard/media directory
2. create a database named 'visualiser' in postgres
3. Create a virtualenv
4. Run pip install -r requirements.pip
5. RUN python manage.py migrate
6. RUN python manage.py runserver

# Frontend setup
1. Install nginx if not
2. Copy app-nginx.config from conf.d to nginx config files (mainly in /etc/nginx/sites-enabled/)
3. sudo nginx -t
4. sudo systemctl reload nginx
5. Visit - 'http://localhost/visualiser'


# Urls
http://localhost
API's
1. /visualise/image/ - list all the image visualised data
2. /visualise/image/<pk>/ - get one visualised image data
3. /visualise/image/upload/ - Visualise new image
