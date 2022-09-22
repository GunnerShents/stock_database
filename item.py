from dataclasses import dataclass
from typing import Union, List


@dataclass
class Product:
    """A product object has a unique serial number, name, discription, order amount and
    delivery type. Can return all propertices in a list"""
    
    prod_id: str
    version_id: str
    name: str
    discript: str
    order_amount: int
    delivery:str
    


@dataclass
class ProductInventory:
    """ProductInventory has a unique serial number, name,
    batch amount, description, order amount(detailing bundle number when ordering),
    delivery method, number held in inventory and limited quantity that should be held
    in stock."""
 
    prod_id: str
    version_id: str
    name: str
    discript: str
    order_amount: int
    delivery:str
    qty:int
    limited_amount:int


@dataclass
class StaffMember:
    """A staff member has an uniwue ID, a name, an email and a unit ID."""

    staff_id:str
    staff_name:str
    staff_email:str
    staff_unit_id:str


@dataclass
class OrderItem:
    """An order class has holds the staff ID, the datetime stamp 
    and the file path name."""

    order_id:int
    staff_id:str
    date_stamp:str
    file_path:str


# Optimistic locking
# UPDATE ..... WHERE verson_id=old.version_id
# 
# t = c.transaction_start()
# rec = t.select()  # score:30
# rec.score = rec.score + 1
# t.update(rec) # score:31
# t.commit()
# 
# t = c.transaction_start(writing=True)
# rec = t.select1()  # score:30
# rec = t.select2()  # score:30
# rec.score = rec.score + 1
# t.update(rec) # score:31
# t.commit()
