### **Customers Table**
```
- customer_id (Primary Key)
- customer_demographic_id (Foreign Key)
- credit_card_id (Foregin key)
```

### **Demographics Table**
- customer_demographic_id (Foreign Key)
- name
- email
- phone_number
- address
- city
- state
- zip_code


### **Credit Cards Table**
```
- credit_card_id (Primary Key)
- customer_id (Foreign Key)
- credit_card_number
- credit_card_expires
- credit_card_security_code
- credit_card_provider
```

### **Orders Table**
```
- order_id (Primary Key)
- customer_id (Foreign Key)
- total
- items_count (the count of items in each order)
```

### **Order Items Table**
```
- item_id (Primary Key)
- order_id (Foreign Key)
- item_name
- course_category (aperitifs, appetizers, entrees, desserts)
```

### **Customer Stats Table**
```
- stats_id (Primary Key)
- customer_id (Foreign Key)
- total_orders
- total_items
- total_spent
```
