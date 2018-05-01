from flask import Flask, redirect, render_template, request, session
from functools import wraps
from ldap3 import Server, Connection, ALL
from flask_kvsession import KVSessionExtension
from simplekv.memory.redisstore import RedisStore
import redis
import json

#Some config and variables

store = RedisStore(redis.StrictRedis())
app = Flask(__name__)
#Change secret key to something UNIQUE (do not randomise on application execution !!!)
app.config['SECRET_KEY'] = '\xe71\r+\x1d\xd2\xec!3q&B\xa8\x02\x01\x9f\xec@E\x98\xe1\xb4\x1f\xc7'
KVSessionExtension(store, app)

                   
#Wrapper for displaying templates for logged in users only.

def login_required(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if session.get('logged_in'):
            return func(*args, **kwargs)
        else:
            return render_template('login.html')
    return wrap


#FUNCTIONS

def authenticate_ldap_user(ldap_user, password, ldap_server):
    user = ldap_user
    server = Server(ldap_server, get_info=ALL)
    conn = Connection(server, 'uid=' + user + ',ou=People,dc=test01,dc=local', password)
    is_authenticated = conn.bind()
    password = ''
    if is_authenticated:
        conn.unbind()
    return is_authenticated

def set_json_in_redis(key, data):
    store.redis.set(key, json.dumps(data))
    
def get_json_from_redis(key):
    return json.loads(store.redis.get(key))



#FLASK URLS
#This renders html based on provided url

@app.route('/')
@login_required
def home():
    return render_template('index.html', session_user=session['user'])

@app.route('/login', methods=['POST'])
def do_admin_login():
    if authenticate_ldap_user(request.form['user'], request.form['password'], 'localhost'):
        session['logged_in'] = True
        session['user'] = request.form['user']
    else:
        return render_template('bad_login.html')
    return home()

@app.route("/logout", methods=['GET'])
@login_required
def logout():
    session['logged_in'] = False
    session['user'] = ''
    current_cookie_val = request.cookies.get('session').split('.')[0]
    print(current_cookie_val)
    print(store.delete(current_cookie_val))
    return home()


#Main application

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=4000)
