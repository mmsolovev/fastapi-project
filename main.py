from enum import Enum
from typing import Union

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel, EmailStr

app = FastAPI()


class IceCreamName(str, Enum):
    strawberry = 'strawberry'
    blueberry = 'blueberry'
    pistachio = 'pistachio'


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = 10.5
    is_offer: Union[bool, None] = None


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Union[str, None] = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return raw_password + 'secret'


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print('User saved')
    return user_in_db


@app.get('/')
async def read_root():
    return {'Hello': 'World'}


@app.get('/items/{item_id}')
async def read_item(item_id: int = Path(
                        title='The ID of item to get',
                        ge=1,
                        le=1000,
                        ),
                    size: float = Query(gt=0, lt=10.5),
                    q: Union[str, None] = Query(
                        default=...,
                        title='Awesome Item',
                        description='This Item is absolutely awesome',
                        alias='item-query',
                        min_length=3,
                        max_length=50,
                        regex='^fixedquery$',
                        deprecated=True,
                        )
                    ):
    return {'item_id': item_id, 'size': size, 'q': q}


@app.post('/items/', response_model=Item)
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        full_price = item.price + item.tax
        item_dict.update({'full_price': full_price})
    return item_dict


@app.put('/items/{item_id}')
async def update_item(item_id: int, item: Item):
    return {'item_name': item.name, 'item_id': item_id}


@app.get('/icecream/{icecream_name}')
async def get_icecream(icecream_name: IceCreamName):
    if icecream_name is IceCreamName.strawberry:
        return {'icecream_name': icecream_name, 'message': 'red color'}
    if icecream_name.value == 'blueberry':
        return {'icecream_name': icecream_name, 'message': 'blue color'}
    # if icecream_name is IceCreamName.pistachio:
    #     return {'icecream_name': icecream_name, 'message': 'green color'}
    return {'model_name': icecream_name, 'message': 'green color'}


@app.get('/files/{file_path:path}')
async def get_file(file_path: str):
    return {'file_path': file_path}


@app.post('/user/', response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved
