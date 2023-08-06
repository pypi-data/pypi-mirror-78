# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['atlantic_server',
 'atlantic_server.atl',
 'atlantic_server.com',
 'atlantic_server.smd']

package_data = \
{'': ['*'], 'atlantic_server.smd': ['documents/*']}

install_requires = \
['Django>=2.2,<3.0',
 'cffi>=1.14.0,<2.0.0',
 'django-filter>=2,<3',
 'djangorestframework>=3,<4',
 'drf-nested-routers>=0.91,<0.92',
 'lxml>=4,<5',
 'mysqlclient>=2,<3',
 'pygit2>=1.2,<1.3',
 'wheel>=0.35.1,<0.36.0']

entry_points = \
{'console_scripts': ['atlantic_server = atlantic_server.manage:main']}

setup_kwargs = {
    'name': 'atlantic-server',
    'version': '0.3.4',
    'description': 'Server side of an application of an Aircraft Technical Log',
    'long_description': '# Atlantic \n\nThis program is the sever side of the Atlantic app. It gives you a restful api.\n\n## Installation on debian 10 (or ubuntu 20.04) for production\n\nThe recommended way to install it is to use a virtual environment.\n\n1. Install pipx, apache2, module wsgi pour apache2\n    ```\n    apt install pipx apache2 libapache2-mod-wsgi\n    ```\n\n2. If your root user, create a user and log it\n    ```\n    adduser username\n    su - username\n    ```\n\n3. Install atlantic_server\n    ```\n    pipx install atlantic_server\n    go to settings\n    ```\n\n4. Open settings.py and adjust parameters\n    - Enter a secret key to SECRET_KEY\n    - Change DEBUG to False\n    - Change MEDIA_ROOT to a location that apache2 serves (see web client side of the application)\n    - Change STATIC_ROOT to a location that apache2 serves (see web client side of the application)\n    - save and close the file\n\n5. Configure Django app\n    ```\n    atlantic_server makemigrations atl\n    atlantic_server migrate\n    atlantic_server collectstatic\n    atlantic_server createsuperuser\n    ```\n\n6. Configure Apache2\n    - Return to root user\n        ```\n        exit\n        ```\n    - Edit a new file\n        ```\n        nano /etc/apache2/site-available/atlantic.conf\n        ```\n    - Paste in following code\n        ```\n        <VirtualHost *:80>\n            <Directory /home/username/atlantic_server>\n                <Files wsgi.py>\n                    Require all granted\n                </Files>\n            </Directory>\n            WSGIPassAuthorization On\n            WSGIDaemonProcess atl python-home=/home/username python-path=/home/username\n            WSGIProcessGroup atl\n            WSGIScriptAlias / /home/username/atlantic_server/wsgi.py\n        </VirtualHost>\n        ```\n    - Save and close file\n\n7. Enabled site for apache\n    ```\n    a2dissite *\n    a2ensite atlantic\n    systemctl reload apache2\n    ```',
    'author': 'Matthieu Nué',
    'author_email': 'matthieu.nue@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
