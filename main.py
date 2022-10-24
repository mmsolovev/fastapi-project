from enum import Enum
from typing import Union

from fastapi import FastAPI, Query, Path, Body
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()


class IceCreamName(str, Enum):
    strawberry = 'strawberry'
    blueberry = 'blueberry'
    pistachio = 'pistachio'


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    price: float
    tax: Union[float, None] = None
    is_offer: Union[bool, None] = None
    tags: list[str] = set()
    description: Union[str, None] = Field(default=None,
                                          title='Description of the title',
                                          max_length=300,
                                          )
    image: Union[list[Image], None] = None

    class Config:
        schema_extra = {
            'example': {
                'name': 'Awesome',
                'price': 300.5,
                'tax': 32.5,
                'is_offer': True,
                'tag': ['good', 'cool', 'super'],
                'description': "A very nice Item"
            }
        }


class Offer(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    items: list[Item]


@app.get('/')
async def read_root():
    return {'Hello': 'World'}


@app.get('/items/{item_id}')
async def read_item(
        item_id: int = Path(
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


@app.post('/items/')
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        full_price = item.price + item.tax
        item_dict.update({'full_price': full_price})
    return item_dict


@app.post('/images/multiple/')
async def create_multiple_images(images: list[Image]):
    return images


@app.post('index-weights')
async def create_index_weights(weights: dict[int, float]):
    return weights


@app.put('/items/{item_id}')
async def update_item(
        item_id: int,
        item: Item = Body(
            example={
                'name': 'Awesome',
                'price': 300.5,
                'tax': 32.5,
                'is_offer': True,
                'tag': ['good', 'cool', 'super'],
                'description': "A very nice Item",
                },
        ),
):
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
