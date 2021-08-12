from setuptools import find_packages, setup

setup(
    name='eventa',
    version='1.0.0',
    packages=find_packages(where='eventa'),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'click==8.0.1',
        'colorama==0.4.4',
        'dnspython==1.16.0',
        'Flask==2.0.1',
        'Flask-Cors==3.0.10',
        'Flask-HTTPAuth==4.4.0',
        'itsdangerous==2.0.1',
        'Jinja2==3.0.1',
        'MarkupSafe==2.0.1',
        'mongoengine==0.23.1',
        'pymongo==3.12.0',
        'python-dateutil==2.8.2',
        'python-dotenv==0.19.0',
        'six==1.16.0',
        'typing-extensions==3.10.0.0',
        'Werkzeug==2.0.1'
    ],
)
