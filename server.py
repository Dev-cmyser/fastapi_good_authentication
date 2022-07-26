import hmac
import hashlib
import json
import base64
from typing import Optional



from fastapi import FastAPI, Form, Cookie
from fastapi.responses import Response

 

app = FastAPI()

SECRET_KEY = "c4f63a85169c2d4f8134de946fabbf38e9937e895bfbb53ddcc9ee518733b156"
PASSWORD_SALT = "9e0dd181c3277dcdde35911479aadf39506372a1c1ea52b780f303352b92014f"


def sign_data(data: str) -> str:
    return hmac.new(
        SECRET_KEY.encode(),
        msg=data.encode(),
        digestmod=hashlib.sha256
    ).hexdigest().upper()


def get_user_from_signed_str(username_signed: str) -> Optional[str]:
    print(username_signed)

    username_base64, sign = username_signed.split(".")
    username = base64.b64decode(username_base64.encode()).decode()
    valid_sign = sign_data(username)
    if hmac.compare_digest(valid_sign, sign):
        return username

def verify_password(username: str, password: str) -> bool:
    password_hash = hashlib.sha256( (password + PASSWORD_SALT).encode() )\
        .hexdigest().lower()
    stored_password_hash = users[username]['password'].lower()
    return  password_hash == stored_password_hash


users = {
    'adm@mail.ru': {
        'name': 'КИРИЛЛ',
        'password': 'b297d289b0897402c97818457bc6072645c2fb700fd91d902c34d47febc661f3',
        'balance':  '34432'
    }
}


@app.get('/') 
def index_pade(username: Optional[str] = Cookie(default=None)):
    with open('templates/login.html',  'r') as file:
        login_page = file.read()
    if not  username:
        return Response(login_page, media_type='text/html')
    valid_username = get_user_from_signed_str(username)
    if not valid_username:
        response = Response(login_page)
        response.delete_cookie(key="username")
        return response

    try:
        user = users[valid_username]
    except KeyError:
            response = Response(login_page, media_type='text/html')
            response.delete_cookie(key="username")
            return response
    return Response(f'Hello {users[valid_username]["name"]}!', media_type='text/html')


@app.post('/login')
def login(username: str = Form(...), password: str = Form(...)):
    user = users.get(username)
    if not user or not verify_password(username, password):
        return Response(json.dumps({
            'success':False,
            'message': "I dont know who are you!!!!!!!!!"
        }), media_type="application/json")

    user_signed = base64.b64encode(username.encode()).decode() + '.' + sign_data(username)
        
    response =  Response(json.dumps({
            'success':True,
            'message':  f'login:{username}\npassword:{password}\n balance:{user["balance"]}'
        }), media_type='application/json')
    response.set_cookie(key='username', value=user_signed)
    return response

