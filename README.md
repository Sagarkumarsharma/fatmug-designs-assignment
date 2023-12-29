# fatmug-designs-assignment

# POST request api to register new vendor
End Point:- api/vendors/

 body-content-for-new-vednor
 
{
"vendor_code": "455463252",
"name": "preet kumari rai chaudhary",
"contact_details": "4689665423",
"address": " kingdom",
"on_time_delivery_rate": 4.5,
"quality_rating": 4.0,
"response_time": "03:12:43",
"fulfilment_rate": 3.4
}
    
# GET request api to check the list of vendors
End Point :- api/vendors/      #by the help of this we can get the list of all vendors but if yoou want reterieve any particular vendor so you can get it by using params as vendor_id
    
    
# PUT request api for the updation in vendor table 
End Point :-     api/vendors/<int:vendor_id>/

# Delete request api for the deletion of any vendor record
End Point :-  api/vendors/<int:vendor_id>/



# POST request api to create new purchase order
End Point :- api/purchase_orders/

body-content-for-purchase-order

 {
"po_number": "1244698xshdfakrearu55fdg",
"order_date": "2023-12-31",
"items": {
"item": "rutle",
"item2": "toy",
"item3": "snakcer"
},
"quantity": 4,
"status": "pending",
"delivery_date": "2023-11-05T06:00:00Z",
"quality_rating": 4.0,
"issue_date": "2023-11-05T02:45:00Z",
"acknowledgment_date": "2023-12-02T19:48:42.039321Z",
"vendor": 8
    }

 # GET Request API to retrieve the list of all orders
 End Point :- api/purchase_orders_list/   

 # Get , Delete, Put Requests APIs for Purchase order 
  End Point :- 'api/purchase_orders/<int:po_id>/  #po_id(product_Id)
    

# Get Request API to get the vendor performance, it will returne some output like delivery_time, reponse_time, quality_rating
End Point :- api/vendors/<int:vendor_id>/performance/


# Post Request API for purchased order acknowledgement, if order is already acknowledged so it will show a msg order already acknowledged else it will acknowlegde the date time for  purchased order and update the reponse time in vednor table
End Point :- api/purchase_orders/<int:po_id>/acknowledge/
