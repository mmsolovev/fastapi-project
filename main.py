from enum import Enum
from typing import Union

from fastapi import FastAPI, Query, Path
from pydantic import BaseModel

app = FastAPI()


class IceCreamName(str, Enum):
    strawberry = 'strawberry'
    blueberry = 'blueberry'
    pistachio = 'pistachio'


class Item(BaseModel):
    name: str
    price: float
    tax: Union[float, None] = None
    is_offer: Union[bool, None] = None


@app.get('/')
async def read_root():
    return {'Hello': 'World'}


@app.get('/items/{item_id}')
async def read_item(item_id: int = Path(
                        title='The ID of item to get'
                        ),
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
    return {'item_id': item_id, 'q': q}


@app.post('/items/')
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
