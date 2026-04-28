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



    

    
    


