from ast import Raise
import uuid
from item import ProductInventory, OrderItem

import sqlite3

# connect to database
conn = sqlite3.connect("inv.db")
# create a cursor
c = conn.cursor()

#c.execute(f"SELECT * FROM {table_name}")
#         t = from_db_cursor(c)

class ProductDB:
    """Allows changes to the product database."""
    def add_record(self, item_object: ProductInventory) -> None:
        """Adds a record to the products table."""
        new_item = (
            item_object.prod_id,
            item_object.name,
            item_object.discript,
            item_object.order_amount,
            item_object.delivery
        )
        
        c.execute(
            f"INSERT OR IGNORE INTO products Values(?,?,?,?,?)", new_item
        )
        print(f"{item_object.name} has been added to products db")
        conn.commit()
    
    def remove_record(self, prod_id: str) -> None:
        """Deletes a record using the product ID"""
        primary_id = (prod_id,)
        c.execute(f"DELETE FROM products WHERE Product_ID=?", primary_id)
        conn.commit()
        
    def update_record(self, item_object: ProductInventory) -> None:
        """Updates the full record located form the primary key."""
        
        new_version_id = uuid.uuid4().hex
        new_item = (
            item_object.name,
            item_object.discript,
            item_object.order_amount,
            item_object.delivery,
            new_version_id,
            item_object.prod_id,
            item_object.version_id,
        )
        old_version = item_object.version_id  # str, probably from a UUID
        # Get _exclusive_ write access to DB
        # Do the check
        c.execute("""
            UPDATE products SET 
                Product_Name = ?,
                Product_Discription = ?,
                Product_Order_amount = ?, 
                Delivery = ?,
                Version_ID = ?
            WHERE
                Product_ID = ? AND Version_ID = ?""",
            new_item,
        )
        if c.rowcount == 0:
            raise RuntimeError("I'm sad :(")
        # release the write access back to the world
        conn.commit()
        print("Your record has been updated!!!")
    
    def get_all_records(self) -> list[tuple[str]]:
        """@returns all the products held in the product db.
        As a list of tuples."""
        c.execute(
        """SELECT * FROM products
        """
        )
        return c.fetchall()
    
    def get_selection_of_records(self,prod_id_list:list[str]) -> list[tuple[str]]:
        """@returns a list of tuples containing all the product fields for the 
        record collection in the @arg"""
        ids = tuple(prod_id_list)
        expression = ','.join(['?']*len(ids))  # dis so ugly, though
        sql = f"SELECT * FROM products WHERE Product_ID IN ({expression})"
        c.execute(sql,ids)
        return c.fetchall()
    
    def get_header_names(self) -> list[str]:
        """@returns all the column names from the db products table."""
        cursor = conn.execute(f"SELECT * FROM products")
        names = [description[0] for description in cursor.description]
        return names

class InventoryDB:    
    """Allows changes to the inventory database."""
    def add_record(self, item_object: ProductInventory) -> None:
        """Adds a record to the inventory table."""
        new_item = (
            item_object.prod_id,
            item_object.qty,
            item_object.limited_amount
            )
    
        c.execute(
            f"INSERT OR IGNORE INTO inventory Values(?,?,?)", new_item
        )
        print(f"{item_object.name} has been added to inventory db")
        conn.commit()
        
    def remove_record(self, prod_id: str) -> None:
        """Deletes a record using the item product id"""
        primary_id = (prod_id,)
        c.execute(f"DELETE FROM inventory WHERE Product_ID=?", primary_id)
        conn.commit()
        
    def update_record(self, item_object: ProductInventory) -> None:
        """Updates the full record located form the primary key."""
        item = (
            item_object.qty,
            item_object.limited_amount,
            item_object.prod_id
        )
        c.execute(
            f"""UPDATE inventory SET 
                Qty = ?,
                Limited_amount = ? WHERE Product_ID = ? """,
            item,
        )
        conn.commit()
        print("Your record has been updated!!!")

class InStock:
    """Instock returns information from the inventory stock view from the database."""
        
    def get_header_names(self) -> list[str]:
        """@returns all the columns from the stock inventory view from the db."""
        cursor = conn.execute(f"SELECT * FROM stock_inventory")
        names = [description[0] for description in cursor.description]
        return names
        
    def get_record(self, primary_key: str) -> list[tuple[str, int]]:
        """@returns a product record as a tuple using the primary key."""
        info = [(primary_key)]
        c.execute(
            f"""
                  SELECT * FROM stock_inventory WHERE Product_ID = ?
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
    
    def get_all_records(self) -> list[tuple[str]]:
        """@returns the list of all records held in the stock_inventory view
        from the database."""
        c.execute(
        """SELECT * FROM stock_inventory
        """
        )
        return c.fetchall()
    
class StaffDB:
    """Staff returns information from the staff database."""
    def get_all_records(self) -> list[tuple[str]]:
        """@returns all the staff member details in a list of tuples"""
        c.execute(
        """SELECT * FROM staff
        """
        )
        return c.fetchall()
    
a = StaffDB()
print(a.get_all_records())

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