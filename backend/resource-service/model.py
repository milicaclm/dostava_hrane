from dataclasses import dataclass

from flask import *

@dataclass
class User:
    uid: str
    name: str
    surname: str
    password: str
    account_type: str
    email: str
    phone_number: str
    is_active: bool

@dataclass
class Delivery:
    did: str
    restaurant_id: str
    user_id: str
    delivery_person_id: str
    status: str
    from_location: str
    to_location: str
    order_time: str
    products: list


@dataclass
class Vehicle:
    type: str
    license_plate: str
    is_ready: bool
    

@dataclass
class Product:
    pid: str
    name: str
    description: str
    price: float


    

    
    


