## Simple flask application with LDAP based authentication snippet

Simple flask application, that can be used as a starting point. It has complete file/directory structure. Includes css and js framework and sample template file.

Requires:
- python3
- flask
- gunicorn3

Includes:
- kube.css
- kube.js

Installation:
```bash
apt install python3 python3-dev python3-pip gunicorn3 redis slapd
pip3 install flask ldap3 flask_kvsession redis
```

LDAP Configuration example:

When you installing slapd remember to set Base DN, Domain and admin password, then adjust authenticate_ldap_user function 
You can populate it with some dummy data, using for example Apache Directory Studio.

Running:
```bash
python3 application.py
```
or
```bash
gunicorn3 --bind 0.0.0.0:8000 wsgi
```
