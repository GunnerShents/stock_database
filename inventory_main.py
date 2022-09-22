
from typing import TypeVar, List, Dict
from item import Product, ProductInventory, StaffMember
from database import InStock, InventoryDB, ProductDB, StaffDB

T=TypeVar('T')

class Admin:
    """Admin class controls the look and feel of the databases. Allows the end user a platform
    to add and update the core products, supplier and staff databses."""

    def __init__(self):
        pass
        #self.product_db = Products()

    def add_product_to_all_products(self):
        """Adds a product to the product database."""
        pass

    def add_staff_member(self):
        """Creates a new staff member"""
        pass

    def create_new_suplier(self):
        """Adds a new supler to the supplier database table."""
        pass


class InterfaceActions:
    """Calculates the logic needed for the user interface, the class works with the database files 
    and the product inventory object."""

    def __init__(self):
        self.stock_table = InStock()
        self.product_db = ProductDB()
        self.inventory_db = InventoryDB()
        self.staff_db = StaffDB()
        
    def create_productInv_object(
        self,
        a_prod_id: str,
        a_version_id: str,
        a_name: str,
        a_discript: str,
        an_order_amount: int,
        a_delivery:str,
        a_qty:int,
        a_limited_amount:int
    ) -> ProductInventory:
        """@returns a product inventory object."""
        item = ProductInventory(
            prod_id=a_prod_id,
            version_id=a_version_id,
            name=a_name,
            discript=a_discript,
            order_amount=an_order_amount,
            delivery=a_delivery,
            qty=a_qty,
            limited_amount=a_limited_amount
        )
        return item
    
    def create_product_object(
        self,
        prod_id:str,
        version_id:str,
        name:str,
        discript:str,
        order_amount:int,
        delivery:str)->Product:
        """@returns a product object."""
        item = Product(
            prod_id=prod_id,
            version_id=version_id,
            name=name,
            discript=discript,
            order_amount=order_amount,
            delivery=delivery
        )
        return item
    
    def create_staff_object(
        self,
        a_staff_id:str,
        a_staff_name:str,
        a_staff_email:str,
        a_staff_unit_id:str,)->StaffMember:
        item = StaffMember(
            staff_id=a_staff_id,
            staff_name=a_staff_name,
            staff_email=a_staff_email,
            staff_unit_id=a_staff_unit_id
        )
        return item
        

    def pull_record(self, p_key:str) -> ProductInventory|str:
        """Retrives a record and creates a product object."""
        if self.check_record_exists(p_key=p_key):     
            # retrieves a record from stock_inv by the NSN
            an_item = self.stock_table.get_record(p_key)
            # extract the tuple from the list
            item: ProductInventory = self.create_productInv_object(*an_item[0])
            return item
        return "No record in database"

    def check_record_exists(self, p_key:str) -> bool:
        """@returns a bool if a record exists in the stock inv table"""
        t = self.stock_table.get_record(p_key)
        return len(t) > 0
    
    def create_or_update_record(self, record:ProductInventory) -> None:
        """Takes a product inventory object, checks a primary key of a product, 
        updates the record or creates a new one in both database tables, product and inventory."""
        if self.check_record_exists(record.prod_id):
            self.product_db.update_record(record)
            self.inventory_db.update_record(record)
            print ('Record updated')
        else:
            self.product_db.add_record(record)
            self.inventory_db.add_record(record)
            print ('record added to the database')
            
    def delete_record(self, record:ProductInventory) -> None:
        """Takes a product object, removes the record from product db and the 
        inventory db, using the product ID."""
        if self.check_record_exists(record.prod_id):
            self.product_db.remove_record(record.prod_id)
            self.inventory_db.remove_record(record.prod_id)
            print("record removed")
        print("record is not in the database")
        
    def get_product_objects(self, prod:bool) ->Dict[str,Product|StaffMember]:
        """@returns a dictionary of all available products. 
        key is the product name and the value is the full product object."""
        object_list:list[Product|StaffMember] = []
        object_dict:dict[str,Product|StaffMember] = {}
        if prod:
            rec = self.product_db.get_all_records()
            for x in rec:
                object_list.append(self.create_product_object(*x))
            for product in object_list:
                object_dict[product.name] = product 
            return object_dict
        else:
            rec = self.staff_db.get_all_records()
            for x in rec:
                object_list.append(self.create_staff_object(*x))
            for product in object_list:
                object_dict[product.staff_name] = product 
            return object_dict
    
    
      
      
        


