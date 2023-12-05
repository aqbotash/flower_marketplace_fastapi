from fastapi import Cookie,FastAPI, templating, Request,Form,Response,templating, HTTPException, Query, Depends
from fastapi.responses import RedirectResponse, JSONResponse
from typing import Annotated
from users_repository import UsersRepository, User, UserLogin
from flowers_repository import  FlowersRepository, Flower
from purchases_repository import PurchaseRepository, Purchase
import json
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

class Item(BaseModel):
    item_id: int
    

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'token')


def create_jwt(user_email: int)->str:
    body = {'user_email': user_email}
    token = jwt.encode(body, 'youngccamel', 'HS256')
    return token

def decode_jwt(token: str)->str:
    data = jwt.decode(token, 'youngccamel', 'HS256')
    return data['user_email']

app = FastAPI()
        
# template = templating.Jinja2Templates('templates')
users_repository = UsersRepository()
flowers_repository = FlowersRepository()
purchases_repository = PurchaseRepository()

    
# @app.get('/signup')
# def registration():
#     return {}

@app.post('/signup')
def post_reg(user: User):
    users_repository.save(user)
    return {**user.dict()}

# @app.get('/login')
# def registration( userLogin: UserLogin):
#     return userLogin
@app.post('/token')
def login(username: str = Form(), password: str = Form()):
    if users_repository.get_by_email(username) == None:
        raise HTTPException(status_code = 404, detail = '404 User Is Not Found')
    else:
        user = users_repository.get_by_email(username)
    if user.password != password:
        raise HTTPException(status_code = 403, detail = 'Forbidden')
    access_token = create_jwt(username)
    return {'access_token': access_token}

@app.get('/profile')
def profile(token: str = Depends(oauth2_scheme)):
    user_email = decode_jwt(token)
    user = users_repository.get_by_email(user_email)
    return {f'Hello {user.full_name}! You are authenticated!'}

@app.get('/flowers')
def get_flowers():
    flowers = flowers_repository.get_all()
    return {'flowers': flowers}

@app.post('/flowers')
def add_flowers(flower: Flower):
    flowers_repository.save(flower)
    return {f'{flower.name} was added to the list!'}

@app.post('/cart/items')
def add_to_cart(item: Item, cart: str = Cookie(default = "[]")):
    response = JSONResponse({'message': 'item was added'})
    cart = json.loads(cart)
    if item.item_id > 0 and item.item_id <= len(flowers_repository.get_all()):
        cart.append(item.item_id)
        cart_json = json.dumps(cart)
        response.set_cookie('cart', cart_json)
    return response

@app.get('/cart/items')
def get_cart(cart: str = Cookie(default='[]')):
    if cart == None:
        return {f'cart is empty'}
    cart = json.loads(cart)
    flowers = flowers_repository.get_by_ids(cart)
    total_price = 0
    for flower in flowers:
        total_price+=int(flower.cost)
    return {'flowers': [flower.name for flower in flowers], 'total_price': total_price}

@app.post('/purchased')
def purchase(response: Response, token: str = Depends(oauth2_scheme), cart: str = Cookie(default = None)):
    cart = json.loads(cart)
    user_email = decode_jwt(token)
    user = users_repository.get_by_email(user_email)
    if user is None:
        raise HTTPException(detail = 'Permission denied', status_code = 403)
    for flower_id in cart:
        purchase = Purchase(user.id, flower_id)
        purchases_repository.save(purchase)
    response = JSONResponse({'message': 'purchased!'})
    response.delete_cookie('cart')
    return response
    
    
@app.get('/purchased')
def get_purchases(token: str = Depends(oauth2_scheme)):
    user_email = decode_jwt(token)
    user = users_repository.get_by_email(user_email)
    purchases = purchases_repository.get_by_user_id(user.id)
    flowers = flowers_repository.get_by_ids(purchases)
    return JSONResponse({'flowers': [flower.name for flower in flowers]})