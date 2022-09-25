from dataclasses import dataclass

@dataclass
class Product:
    """A product object has a unique serial number, name, discription, order amount and
    delivery type. Version_id is a uuid string used for record version control"""
    
    prod_id: str
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
    prod_version_id: str
    inv_version_id: str
    name: str
    discript: str
    order_amount: int
    delivery:str
    qty:int
    limited_amount:int
    
    def display_data(self) -> list[int|str]:
        """@returns a list of fields. The values reflect the data needed in the main
        menu of the GUI"""
        return [self.prod_id, 
                self.name, 
                self.discript, 
                self.order_amount, 
                self.delivery, 
                self.qty, 
                self.limited_amount]
        
    def update_display_fields(self, prod_id:str, name:str, dis:str, order:str, deliv:str, qty:str, lim: str) -> None:
        """
        Updates prod_id, name, discription, order_amount, delivery, qty and
        limited amount.        
        """
        self.prod_id = prod_id
        self.name= name 
        self.discript = dis 
        self.order_amount = int(order)
        self.delivery = deliv 
        self.qty = int(qty)
        self.limited_amount = int(lim)


@dataclass
class StaffMember:
    """A staff member has an unique ID, a name, an email and a unit ID."""

    staff_id:str
    staff_name:str
    staff_email:str
    staff_unit_id:str


@dataclass
class OrderItem:
    """An order class holds the staff ID who created the order, the datetime stamp 
    and the file path where the order is saved."""

    order_id:int
    staff_id:str
    date_stamp:str
    file_path:str



