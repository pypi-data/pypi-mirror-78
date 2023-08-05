from setuptools import setup

# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(
    name='Flask-State',
    version="0.0.2",
    author="Yoobool",
    url="https://github.com/yoobool/flask-state",
    install_requires=[
        "Werkzeug>=0.15",
        "Jinja2>=2.10.1",
        "itsdangerous>=0.24",
        "click>=5.1",
        "Flask>=1.0",
        "SQLAlchemy>=1.2",
        "Flask-SQLAlchemy>=1.0"
    ]
)
