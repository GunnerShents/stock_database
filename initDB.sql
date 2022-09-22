CREATE TABLE "inventory" (
	"Product_ID"	text,
	"Qty"	integer,
	"Limited_amount"	integer,
	PRIMARY KEY("Product_ID")
);

CREATE TABLE orders (
            order_ID int PRIMARY KEY,
            Staff_ID text,
            Date_stamp text,
            file_path text
            );

CREATE TABLE "products" (
	"Product_ID"	text,
	"Product_Name"	text,
	"Product_Discription"	text,
	"Product_Order_amount"	integer,
	"Delivery"	TEXT,
	PRIMARY KEY("Product_ID")
);

CREATE TABLE staff (
            Staff_ID text PRIMARY KEY,
            staff_name text,
            staff_email text,
            unit_ID text
            );

CREATE VIEW stock_inventory
AS
SELECT 
	products.Product_ID, 
	products.Product_Name, 
	products.Product_Discription,
	products.Product_Order_amount,
	products.Delivery, 
	inventory.Qty,  
	inventory.Limited_amount
FROM 
	products
INNER JOIN 
	inventory 
ON 
	products.Product_ID = inventory.Product_ID;