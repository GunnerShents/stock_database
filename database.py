from ast import Raise
import uuid
from item import ProductInventory, OrderItem

import sqlite3

# connect to database
conn = sqlite3.connect("inv.db")
# create a cursor
c = conn.cursor()



class ProductDB:
    """Allows changes to the product database."""
    def add_record(self, item_object: ProductInventory) -> None:
        """Adds a record to the products table."""
        
        new_version = uuid.uuid4().hex
        new_item = (
            item_object.prod_id,
            new_version,
            item_object.name,
            item_object.discript,
            item_object.order_amount,
            item_object.delivery
        )
        
        c.execute(
            f"INSERT OR IGNORE INTO products Values(?,?,?,?,?,?)", new_item
        )
        print(f"{item_object.name} has been added to products db")
        conn.commit()
    
    def remove_record(self, prod_id: str) -> None:
        """Deletes a record using the product ID"""
        primary_id = (prod_id,)
        c.execute(f"DELETE FROM products WHERE Product_ID=?", primary_id)
        conn.commit()
        
    def update_record(self, item_object: ProductInventory) -> str:
        """
        Checks the version_id has not changed and updates the 
        full record located from the primary key with a new_version_id. """
        #create a new version_id
        new_version_id = uuid.uuid4().hex
        new_item = (
            item_object.name,
            item_object.discript,
            item_object.order_amount,
            item_object.delivery,
            new_version_id,
            item_object.prod_id,
            item_object.prod_version_id,
        )
        print(item_object.prod_version_id)
        print(f'{new_version_id}, new id')
        # Update record if and only if product_id and version_id are true
        c.execute("""
            UPDATE products SET 
                Product_Name = ?,
                Product_Discription = ?,
                Product_Order_amount = ?, 
                Delivery = ?,
                prod_version_ID = ?
            WHERE
                Product_ID = ? AND prod_version_ID = ?""",
            new_item,
        )
        if c.rowcount == 0:
            #raise RuntimeError("I'm sad :(")
            return "Nothing to this record was changed, please try again"
            
        # release the write access back to the world
        conn.commit()
        return "Your record has been updated!!"
    
    def get_all_records(self) -> list[tuple[str]]:
        """@returns all the products held in the product db.
        As a list of tuples."""
        c.execute(
        """
        SELECT 
            Product_ID,
            Product_Name,
            Product_Discription,
            Product_Order_amount,
            Delivery
        FROM 
            products
        """
        )
        return c.fetchall()
    
    def get_selection_of_records(self,prod_id_list:list[str]) -> list[tuple[str]]:
        """@returns a list of tuples containing all the product fields for the 
        record collection in the @arg"""
        ids = tuple(prod_id_list)
        expression = ','.join(['?']*len(ids))  
        sql = f"SELECT * FROM products WHERE Product_ID IN ({expression})"
        c.execute(sql,ids)
        return c.fetchall()
    
    def get_header_names(self) -> list[str]:
        """@returns all the column names from the db products table."""
        cursor = conn.execute(f"SELECT * FROM products")
        names = [description[0] for description in cursor.description]
        names.remove("prod_version_id")
        return names

class InventoryDB:    
    """Allows changes to the inventory database."""
    def add_record(self, item_object: ProductInventory) -> None:
        """Adds a record to the inventory table."""
        new_version = uuid.uuid4().hex
        new_item = (
            item_object.prod_id,
            new_version,
            item_object.qty,
            item_object.limited_amount
            )
    
        c.execute(
            f"INSERT OR IGNORE INTO inventory Values(?,?,?,?)", new_item
        )
        print(f"{item_object.name} has been added to inventory db")
        conn.commit()
        
    def remove_record(self, prod_id: str) -> None:
        """Deletes a record using the item product id"""
        primary_id = (prod_id,)
        c.execute(f"DELETE FROM inventory WHERE Product_ID=?", primary_id)
        conn.commit()
        
    def update_record(self, item_object: ProductInventory) -> str:
        """Updates the full record located form the primary key."""
        
        #add version control here
        new_version_id = uuid.uuid4().hex
        item = (
            new_version_id,
            item_object.qty,
            item_object.limited_amount,
            item_object.prod_id,
            item_object.inv_version_id
        )
        # Update record if and only if product_id and version_id are true
        c.execute(
            f"""UPDATE inventory SET 
                    inv_version_id = ?,
                    Qty = ?,
                    Limited_amount = ? 
                WHERE 
                    Product_ID = ? and inv_version_id = ?""",
            item,
        )
        if c.rowcount == 0:
            #raise RuntimeError("I'm sad :(")
            return "Nothing to this record was changed, please try again"
        # release the write access back to the world
        conn.commit()
        return "Your record has been updated!!!"

StockRecord = tuple[str, str, str, str, str, int, str, int, int]

class InStock:
    """Instock returns information from the inventory stock view from the database."""
        
    def get_header_names(self) -> list[str]:
        """@returns all the columns from the stock inventory view from the db."""
        cursor = conn.execute(f"SELECT * FROM stock_inventory")
        names = [description[0] for description in cursor.description]
        names.remove("prod_version_id")
        names.remove("inv_version_id")       
        return names
        
    def get_record(self, primary_key: str) -> list[StockRecord]:
        """@returns a product record as a tuple using the primary key."""
        info = [(primary_key)]
        c.execute(
            f"""
                SELECT 
                    Product_ID,
                    prod_version_id,
                    inv_version_id,
                    Product_Name,
                    Product_Discription,
                    Product_Order_Amount,
                    Delivery,
                    Qty,
                    Limited_Amount
                FROM 
                    stock_inventory 
                WHERE 
                    Product_ID = ?
                  """,
            info,
        )
        return c.fetchall()
    
    def need_ordering(self) -> list[tuple[str]]:
        """Checks each record in the table @returns all records where the qty
        is less the allowed minimum."""
        c.execute(
            """SELECT * FROM stock_inventory WHERE Qty < Limited_amount"""
        )
        return c.fetchall()
    
    def get_all_records(self) -> list[StockRecord]:
        """@returns the list of all records held in the stock_inventory view
        from the database."""
        c.execute(
        """
        SELECT 
            Product_ID,
            prod_version_id,
            inv_version_id,
            Product_Name,
            Product_Discription,
            Product_Order_Amount,
            Delivery,
            Qty,
            Limited_Amount
        FROM 
            stock_inventory
        """
        )
        return c.fetchall()
    
class StaffDB:
    """Staff returns information from the staff database."""
    def get_all_records(self) -> list[tuple[str]]:
        """@returns all the staff member details in a list of tuples"""
        c.execute(
        """
        SELECT 
            Staff_ID,
            staff_name,
            Staff_email,
            unit_ID    
        FROM 
            staff
        """
        )
        return c.fetchall()
    

class CompletedOrders:
    """Carries out CRUD commands on the order table in the database."""
    
    def add_record(self, item_object: OrderItem) -> None:
        """Adds a record to the orders table."""
        new_item = (
            item_object.order_id,
            item_object.staff_id,
            item_object.date_stamp,
            item_object.file_path,
        )
        
        c.execute(
            f"INSERT OR IGNORE INTO order Values(?,?,?,?)", new_item
        )
        print("Order added to order database")
        conn.commit()