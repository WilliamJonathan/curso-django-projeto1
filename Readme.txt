update python packages.
    python -m pip install pip setuptools wheel --upgrade

create virtual environment.
    python -m venv venv

activate virtual environment.
    #mac/linux
    . venv/bin/activate
    #windows
    ./venv/scripts/activate

install Django or upgrade (make sure your virtual environment is active).
    pip install django
    pip install --upgrade django

libraries and packages.
    always run these commands in your virtual environment (venv).
    #faker
    python -m pip install faker
    #pytest
    pip install pytest pytest-django
    #pillow
    pip install pillow
    #parameterized
    pip install parameterized
    #coverage
    pip install coverage

run migrations
    python manage.py makemigrations
    python manage.py migrate

create superuser
    python manage.py createsuperuser 

run coverage
    coverage run --omit='*/venv/*' -m pytest
    coverage run -m pytest
    coverage run manage.py test
    coverage html

create environment ambiant
    pip install python-dotenv

python shell
    duplicar receita:
    python manage.py shell
    from receipes.models import receipe
    r = Recipe.objects.get(pk=?)
    r
    for i in range(???): r.id = None; r.slug = f'texto-slug-{i}'; r.save();

create new app:
    python manage.py startapp authors    

##não esquecer de selecionar o intepretador do ambiante virtual caso use vs.code
