update python packages.
    pip -m pip install pip setuptools wheel --upgrade

create virtual environment.
    python -m venv venv

activate virtual environment.
    #mac/linux
    . venv/bin/activate
    #windows
    venv\Scripts\activate

install Django (make sure your virtual environment is active).
    pip install django

libraries and packages.
    always run these commands in your virtual environment (venv).
    #faker
    python -m pip install faker
    #pytest
    pip install pytest pytest-django