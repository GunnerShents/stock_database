
from typing import TypeVar, List, Dict
from item import Product, ProductInventory, StaffMember
from database import InStock, InventoryDB, ProductDB, StaffDB

T=TypeVar('T')


class InterfaceActions:
    """Calculates the logic needed for the user interface, the class works with the database files 
    and the product inventory object."""

    def __init__(self):
        self.stock_table = InStock()
        self.product_db = ProductDB()
        self.inventory_db = InventoryDB()
        self.staff_db = StaffDB()

    def check_record_exists(self, p_key:str) -> bool:
        """@returns a bool if a record exists in the stock inventory table"""
        t = self.stock_table.get_record(p_key)
        return len(t) > 0
    
    def create_or_update_record(self, record:ProductInventory) -> None:
        """Takes a product inventory object, checks a primary key of a product, 
        updates the record or creates a new one in both database tables, product and inventory."""
        if self.check_record_exists(record.prod_id):
            print(self.product_db.update_record(record))
            print(self.inventory_db.update_record(record))
        else:
            print(self.product_db.add_record(record))
            print(self.inventory_db.add_record(record))
           
            
    def delete_record(self, record:ProductInventory) -> None:
        """Takes a product object, removes the record from product db and the 
        inventory db, using the product ID."""
        if self.check_record_exists(record.prod_id):
            self.product_db.remove_record(record.prod_id)
            self.inventory_db.remove_record(record.prod_id)
            print("record removed")
        else:
            print("record is not in the database")
        
    def get_product_objects(self) ->Dict[str,Product]:
        """@returns a dictionary of all available products. 
        key is the product name and the value is the full product object."""
        object_list:list[Product] = []
        object_dict:dict[str,Product] = {}    
        #creates a list of tuples containing all the records in the product database
        rec = self.product_db.get_all_records()
        #Creates an object from the product fields
        for x in rec:
            record = Product(*x)
            object_list.append(record)
        #creates a dictionary k is product name as a string, value is a product object
        for product in object_list:
            object_dict[product.name] = product 
        return object_dict
    
    
    def get_staff_objects(self) ->Dict[str,StaffMember]:
        """@returns a dictionary of all available staff members. 
        key is the staff name and the value is a staff object."""
        object_list:list[StaffMember] = []
        object_dict:dict[str,StaffMember] = {}    
        #creates a list of tuples containing all the records in the product database
        rec = self.staff_db.get_all_records()
        #Creates an object from the product fields
        for x in rec:
            record = StaffMember(*x)
            object_list.append(record)
        #creates a dictionary k is product name as a string, value is a product object
        for product in object_list:
            object_dict[product.staff_name] = product 
        return object_dict


    
    
    
    
    
        # else:
        #     rec = self.staff_db.get_all_records()
        #     for x in rec:
        #         record = StaffMember(*x)
        #         object_list.append(record)
        #         print(record)
        #     for product in object_list:
        #         object_dict[product.staff_name] = product 
        #     return object_dict
    
    
      
      
        


