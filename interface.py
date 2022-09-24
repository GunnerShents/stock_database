from winreg import SetValueEx
from inventory_main import InterfaceActions
from database import *
from order_form import *
from item import Product, StaffMember, ProductInventory
from order_form import *
#import PySimpleGUI as psg
from typing import TYPE_CHECKING, Any
from typing import Union, List, Callable
 
if TYPE_CHECKING:
    psg = Any
else:
    import PySimpleGUI as psg

#type check alas
TableData = list[list[str | int]]
StockRecord = tuple[str, str, str, str, str, int, str, int, int]

class Display:
    """Takes StockItems and holds them in a dictionary, has function to update the inventory,
    update details, create a CSV file and print out the inventory."""

    def __init__(self) -> None:

        #Instantuate
        self.stock = InStock()
        self.product = ProductDB()
        self.inventory = InterfaceActions()
        self.order_form = Order()
        #field attributes for the main window
        self.headers = self.stock.get_header_names()
        self.window_stock = None
        self.stock_table = None
        #Order information
        self.prod_id_list_for_orders:List[str] = []
    
    def table_template(self,data_list:List[List[str]],headers:List[str],a_key:str) -> psg.Table:
        """@returns a pysimpleGUI table. 
        @args data_list all the data you require in the table.
        @args headers is a stringlist of the column headers you require.
        @args key is a string key linked to the table."""
        table = psg.Table(
                    values=data_list,
                    headings=headers,
                    max_col_width=30,
                    auto_size_columns=False,
                    display_row_numbers=False,
                    selected_row_colors=('light blue', 'dark blue'),
                    justification="left",
                    enable_events='True',
                    num_rows=10,
                    key=a_key,
                    row_height=35,)
        return table
    
    def create_table_data(self, data_source:Callable[[], list[tuple[str]]]) -> TableData:
        """
        add notes
        """
        data = data_source()
        new_data:List[List[Union[str,int]]] = []
        for record in data:
            record_object = ProductInventory(*record)
            display_data = record_object.display_data()
            new_data.append(display_data)
        return new_data
            
    def main(self) -> None:
        """Shows all the current stock in the Pysimplegui application."""
        
        new_data = self.create_table_data(self.stock.get_all_records)
        psg_table = self.table_template(new_data,self.headers,'-TABLE-')
        layout = [
            [psg.Button("Refresh", size=(10,0)),psg.Push(),psg.Text("***STOCK MAIN MENU***",size=(60,1), justification='centre'),psg.Push()],
            #Table displayed at this row of the layout
            [psg_table],
            [psg.Push(),
            psg.Button("Add To Stock", size=(20,1),pad=(35,10)),
            psg.Button("Check Low Stock", size=(20,1),pad=(35,10)),
            psg.Button("View All Products", size=(20,1),pad=(35,10)),
            psg.Push()]
        ]
        self.window_stock = psg.Window("Products in Stock", layout)
        while True:
            event, values = self.window_stock.read()
            if event == psg.WIN_CLOSED:
                break
            if event == 'Refresh':
                # data = self.stock.get_all_records()
                # new_data:List[List[Union[str,int]]] = [list(record) for record in data]
                new_data = self.create_table_data(self.stock.get_all_records)
                layout[1][0].update(values=new_data)   
            if event == '-TABLE-':
                if values['-TABLE-']:
                    try:
                        index:str = values['-TABLE-'][0]
                        record:str = new_data[index][0]
                        print(type(record))
                        self.crud_window(record)
                    except IndexError:
                        print(values['-TABLE-'])
            if event == 'View All Products':
                self.show_all_products()
            if event == 'Check Low Stock':
                self.show_low_stock()
            if event == 'Add To Stock':
                empty_list=['','','','','','','']
                self.crud_window(empty_list)
                
        self.window_stock.close()

    def crud_window(self, record_details:str) -> None:
        """@args the record information from the main table. 
        Allows the user to update the record details in the GUI and 
        the database."""
        #locate the record from the database
        record_data = self.stock.get_record(record_details)
        #create a product object with the record information
        my_record = ProductInventory(*record_data[0])
        my_record_display_details = my_record.display_data()
        print(self.headers)
        layout = [
            [psg.Text("***AMEND STOCK ITEM***",size=(40,1), justification='centre')],
        ]
        for index, header in enumerate(self.headers):  
            new_row = [psg.Text(f'{header}',size=(20,1)),
                        psg.Input(default_text=f"{my_record_display_details[index]}", key='TEXT', size=(20,1),disabled=True,), 
                        ]
            layout.append(new_row)
        layout.append([
                    psg.Push(),
                    psg.Button("Create record", size=(10,1), button_color='blue'),
                    psg.Button("Update Record", size=(15,1),button_color='blue'),
                    psg.Button("edit", size=(10,1), button_color="grey"),
                    psg.Push()
                    ])
        layout.append([psg.Push(),
            psg.Button("Delete", size=(10,1), button_color="red"),
            psg.Push()
            ])
        window_record = psg.Window(f"Record for {my_record.name}", layout)
        
        while True:
            event, values = window_record.read()
            if event == psg.WIN_CLOSED: 
                break
            if event == 'Create record':
                for i in range(1,8):
                    layout[i][1].update(value='')
            if event == 'edit':
                for i in range(1,8):
                    layout[i][1].update(disabled=False)
            if event == 'Update Record':
                updated_record = my_record.update_display_fields(*values.values())
                self.inventory.create_or_update_record(my_record)
                break
            if event == 'Delete':
                self.inventory.delete_record(my_record)
                break
                
        window_record.close()
    
    def show_low_stock (self) -> None:
        """Checks what items are below the set limits and displays the 
        items in a GUI table."""
        
        new_data = self.create_table_data(self.stock.need_ordering)
        headers = self.stock.get_header_names()
        psg_table = self.table_template(new_data,headers,'-TABLE-')
        layout = [
            [psg.Push(),
            (psg.Text("***LOW SOCK***",size=(80,1), justification='centre')),
            psg.Push()],
            [psg_table],
            [psg.Push(),
             psg.Button("Close Window", size=(20,1), key='-Close-'),psg.Button("Add To Order", size=(20,1), key='-Order-'),
             psg.Push()
            ],
        ]
        window_ordering = psg.Window("Need ordering", layout)
        
        while True:
            event, values = window_ordering.read()
            if event == psg.WIN_CLOSED or event == "-Close-":
                break
            if event == '-Order-':
                v:List[int] = values['-TABLE-']
                if len(v) > 0:
                    selected_prods = [rec for i, rec in enumerate(new_data) if i in v]
                    for x in selected_prods:
                        self.prod_id_list_for_orders.append(x[0])
                    self.create_order(self.prod_id_list_for_orders)
                    break
        window_ordering.close()
    
    def show_all_products(self) -> None:
        """Checks with the database what products are available. Diaplays
        items in a GUI table."""
        new_data = self.create_table_data(self.stock.get_all_records)
        #top row
        row1 = [psg.Push(),psg.Frame('Prduct Main Menu:',
                [[psg.Text(f"* * * "*29, text_color=('yellow'))],
                [psg.Text("*WHEN CREATING AN ORDER PRESS CRTL KEY TO SELECT MULTIPLE PRODUCTS, THEN PRESS ADD TO ORDER BUTTON *", text_color='yellow')],
                [psg.Text(f"* * * "*29,text_color=('yellow'))],
                ],),psg.Push()]
        #row2 - frame 1
        row2 = [psg.Frame('Products:',
                [[psg.Table(
                    values=new_data,
                    headings=self.headers,
                    max_col_width=25,
                    auto_size_columns=True,
                    display_row_numbers=False,
                    justification="left",
                    selected_row_colors=('light blue', 'dark blue'),
                    enable_events='True',
                    num_rows=10,
                    key="-TABLE-",
                    row_height=25,)]])]
        #row3
        row3 = [psg.Push(),
             psg.Button("Close Window", size=(20,1), key='-Close-'),
             psg.Button("Add To Order", size=(15,1)),
             psg.Push()]
    
        layout = [[row1],[row2],[row3]]
        
        window_product = psg.Window("Availabe products", layout)
        
        while True:
            event, values = window_product.read()
            if event == psg.WIN_CLOSED:
                break
            if event == 'Add To Order':
                v:List[int] = values['-TABLE-']
                if len(v) > 0:     
                    selected_prods = [str(rec[0]) for i, rec in enumerate(new_data) if i in v]
                    self.create_order(selected_prods)
                    break
            if event == '-Close-':
                break
                                
        window_product.close()
        
        
    def create_order(self, list_of_prod_ids:List[str]):
        """Shows a table of the selected products from the previous screen.
        Products can be added and removed."""
        
        def item_check( name:str) -> bool:
            for x in new_data:
                if name in x:
                    return True
            return False
        
        data = self.product.get_selection_of_records(list_of_prod_ids)
        new_data:List[List[str]] = []
        for record in data:
            new_data.append(list(record))
        headers = self.product.get_header_names()
        psg_table = self.table_template(new_data,headers,'-TABLE-')
        product_objects = self.inventory.get_product_objects(True)
        staff_objects = self.inventory.get_product_objects(False)
        col1 = psg.Column([[psg.Frame('Products:',
                          [[psg_table]]
                                     )
                           ]])
        col2 = psg.Column([[psg.Frame('Order Details:',
                          [[psg.Listbox([f'{product_objects[prod].name}' for prod in product_objects],expand_y=True,size=(20,10),key='-PROD-' )]]
                                      )],
                           [psg.Frame('Staff Details',
                          [[psg.Listbox([f'{staff_objects[staff].staff_name}' for staff in staff_objects],expand_y=True,size=(15,10),key='-STAFF-')]]
                                     )
                           ]])             
        bottom_row = [psg.Push(),
                    psg.Button("Remove Product", size=(15,1)),
                    psg.Button("Add Another Product", size=(15,1)),
                    psg.Button("Create Spread Sheet", size=(15,1)),psg.Push()]
        layout = [psg.vtop([col1,col2]),[bottom_row]]
        window_order = psg.Window("Order Form", layout)
        
        while True:
            event, values = window_order.read()
            if event == psg.WIN_CLOSED:
                break
            if event == 'Add Another Product':
                if len(values['-PROD-'])>0:
                    name = values['-PROD-'][0]
                    obj = product_objects[name]
                    if not item_check(name):
                        new_data.append(list(obj.get_all_fields()))
                        layout[0][0].get_next_focus().update(values=new_data)
            if event == 'Remove Product':
                if len(values['-TABLE-'])>0:
                    order_item_index:int = values['-TABLE-'][0]
                    row = new_data[order_item_index]
                    del_name = row[1]
                    if item_check(del_name):
                        new_data.pop(order_item_index)
                        #access the pysimplegui table element
                        layout[0][0].get_next_focus().update(values=new_data)
            if event == 'Create Spread Sheet':
                #empty dictionary holding products and staff members
                prod_order_list:dict[str,list[Product|StaffMember]] = {'products':[],'staff':[]}
                for x in new_data:    
                    obj = product_objects[x[1]]
                    prod_order_list['products'].append(obj)
                obj = staff_objects[values['-STAFF-'][0]]
                prod_order_list['staff'].append(obj) 
                #creates the order form adds the order, saves and closes file.
                self.order_form.write_order_to_file(prod_order_list)
                new_data = []
                layout[0][0].get_next_focus().update(values=new_data)
                
                
               
              
                
        window_order.close()
            
            
        

if __name__== "__main__":
    dis = Display()
    dis.main()
