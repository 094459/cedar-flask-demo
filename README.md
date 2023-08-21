# cedar-flask-demo

A very simple demo to show how you can use Cedar in Python, with a simple Flask based web application. This code is illustrative and verbose to help explain and show how Cedar works.

This repo contains the following demo sample app.

```
├── README.md
└── flask-demo
    ├── app.py
    ├── entities.json
    ├── flask.cedar.policy
    ├── protected
    │   └── images
    │       ├── pic-1.jpeg
    │       ├── pic-2.png
    │       └── pic-3.jpg
    ├── requirements.txt
    ├── schema.json
    ├── static
    │   └── images
    │       └── cedar-green.png
    ├── templates
    │   ├── admin.html
    │   ├── base.html
    │   ├── denied.html
    │   ├── index.html
    │   ├── login.html
    │   ├── photos-manage.html
    │   ├── photos.html
    │   └── public-photos.html
    ├── test.py
    └── users.dat
```

This demo would not be possible without the excellent work of **Stephen Kuenzli** and his [cedar-py library](https://github.com/k9securityio/cedar-py)

**Installation**

To get this up and running, first create a virtual Python environment

```
python -m venv cedar-demo
source cedar-demo/bin/activate
cd cedar-demo
```

Check out the code

```
git clone https://github.com/094459/cedar-flask-demo.git
```

Install dependencies

```
cd cedar-flask-demo/flask-demo
pip install -r requirements.txt
```

You should now be able to start the application

```
python app.py
```

Opening a browser at localhot:5000 should bring up the Flas app. To login, check out the users.dat file for sample users.


