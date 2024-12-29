# s21_ShopAPI
Restful Http API for a small service for the sale of household appliances.

## Task

There are the following entities:
```
client
{
    id
    client_name
    client_surname
    birthday
    gender
    registration_date
    address_id
}
```
```
product
{
    id
    name
    category
    price
    available_stock
    last_update_date
    supplier_id
    image_id: UUID
}
```
```
supplier
{
    id
    name
    address_id
    phone_number
}
```
```
images
{
    id : UUID
    image: bytea
}
```

```
address 
{
    id
    country
    city
    street
}
```

It is necessary to implement popular types of HTTP requests (GET, POST, PUT, DELETE, PATCH).

- Clients:
    1. Adding a client (json is supplied to the input, corresponding to the structure described above).
    2. Deleting a client (by its ID)
    3. Receiving clients by first and last name (parameters — first and last name)
    4. Receiving all clients (In this request it is necessary to provide optional pagination parameters in the query string: limit and offset). If these parameters are missing, return the entire list.
    5. Changing the client's address (parameters: Id and new address in the form of json in accordance with the format described above)

- Products:
    1. Adding a product (json is supplied to the input, corresponding to the structure described above).
    2. Reducing the quantity of goods (the request is provided with the product ID and how much to reduce)
    3. Receiving the product by id
    4. Receiving all available items
    5. Deleting an item by id

- Suppliers:
    1. Adding a supplier (json is supplied as input, corresponding to the structure described above).
    2. Changing the supplier's address (parameters: Id and new address in json format according to the format described above)
    3. Deleting a supplier by id
    4. Getting all suppliers
    5. Getting a supplier by id

- Images:
    1. adding an image (the bytearray of the image and the product id are supplied as input).
    2. Changing the image (the input is supplied with the image id and a new line for replacement)
    3. Deleting an image by image id
    4. Getting an image of a specific product (by product ID) 
    5. Getting an image by image id

Methods that return an image must return an image (an array of bytes) with the header "application/octet-stream". In this case, the file should be downloaded automatically.


For each of the above described requests, if it is planned to receive data in the input body, it is necessary to validate the data and, if validation was unsuccessful, issue a 400 error code with the message text.

If the request provides for updating data or receiving by Id, it is necessary to return error code 404 with the message text in case of missing data.


If the request provides for returning a list of data, then an empty list is returned if there is no data.