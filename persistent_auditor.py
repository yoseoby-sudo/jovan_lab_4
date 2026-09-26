inventory = 0
rejected = 0
deliveries = 0
inventory_history = []

def load_inventory():
    #Load the inventory total and history from inventory.txt
    try:
        with open("inventory.txt", "r") as file:
            lines = file.readlines()

            #Check if the file is empty
            if not lines:
                return 0, 0, []

            #First line is the total inventory
            inventory = int(lines[0].strip())

            #Second line is the number of deliveries
            deliveries = int(lines[1].strip())

            #Remaining lines contain:
            #Product ID | Product Name | Quantity
            inventory_history = []

            for line in lines[2:]:
                parts = line.strip().split("|")

                if len(parts) == 3:
                    product_id = int(parts[0])
                    product_name = parts[1]
                    quantity = int(parts[2])

                    inventory_history.append(
                        (product_id, product_name, quantity)
                    )

            return inventory, deliveries, inventory_history

    except FileNotFoundError:
        # If the file does not exist, start with empty inventory and history
        return 0, 0, []

def save_inventory(total, deliveries, inventory_history):
    #Save the inventory total, deliveries and inventory history
    with open("inventory.txt", "w") as file:
        file.write(f"{total}\n")
        file.write(f"{deliveries}\n")

        for product_id, product_name, quantity in inventory_history:
            file.write(f"{product_id}|{product_name}|{quantity}\n")
    print("Inventory saved successfully to inventory.txt.")

def get_product_name():
      #Get the product name from the user 
      while True: 
        product_name = input("\nEnter Product Name: ").strip() 
        if product_name.lower() == "quit":
              return "quit" 
        
        if product_name == "": 
            print("Error, Product Name cannot be empty") 
            return None 
            
        return product_name
    
def get_valid_input():
    #Prompt the user and return a valid integer or 'quit'
    while True:
        inventory_input = input("Enter Quantity: ")

        #Check for quit condition
        if inventory_input.lower() == "quit":
            return "quit"

        #Check if input is a valid number
        try:
            quantity = int(inventory_input)
        except ValueError:
            print("Error, Quantity must be a number")
            return None

        #Validate that number is not negative
        if quantity < 0:
            print("Error, Quantity cannot be negative")
            return None

        return quantity

def process_delivery(current_total, new_value):
    #Calculate and return the new inventory total
    return current_total + new_value

def calculate_tax(amount):
    #Calculate 10% tax for a delivery
    return amount * 0.10

def generate_report(total_units,deliveries, failed_attempts, inventory_history):
    #Print the final inventory report
    print("\n=== Final Inventory Report ===")
    print(f"Total Deliveries Processed: {deliveries}")
    print(f"Total Inventory Quantity Entered: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")

    if not inventory_history: 
        print("No inventory records.") 
    else: 
        for product_id, product_name, quantity in inventory_history: 
            print( f"Product ID: {product_id} | " f"Product Name: {product_name} | " f"Quantity: {quantity}" )

#Main program
inventory, deliveries, inventory_history = load_inventory()

print("Welcome to inventory taking")
print(f"Current Inventory Quantity: {inventory}")

print("\nInventory History:")
for product_id, product_name, quantity in inventory_history:
    print( 
        f"Product ID: {product_id} | " 
        f"Product Name: {product_name} | " 
        f"Quantity: {quantity}" )

#Determine the next Product ID 
if inventory_history: 
    next_product_id = max( 
        product[0] for product in inventory_history) + 1 
else:
      next_product_id = 1001

while True:
    #Get Product Name 
    product_name = get_product_name() 

    #Check for quit signal
    if product_name == "quit":
          save_inventory(inventory, deliveries, inventory_history)
          break 
        
    #Check for failed/rejected input 
    if product_name is None: 
        rejected += 1 
        continue

    #Get quantity
    quantity = get_valid_input()

    #Check for quit signal
    if quantity == "quit":
        save_inventory(inventory, deliveries, inventory_history)
        break

    #Check for failed/rejected input
    if quantity is None:
        rejected += 1
        continue

    #Calculate tax for this delivery
    tax = calculate_tax(quantity)

    #Process the delivery
    new_inventory = process_delivery(inventory, quantity)

    #Check if adding the quantity exceeds the maximum inventory limit
    if new_inventory > 500:
        print("Inventory overloaded!")
        save_inventory(inventory, deliveries, inventory_history)
        break

    #Check if the product already exists
    product_exists = False

    for index in range(len(inventory_history)):
        product_id, existing_name, existing_quantity = inventory_history[index]

        if existing_name.lower() == product_name.lower():
            #Add the new quantity to the existing product
            inventory_history[index] = (
                product_id,
                existing_name,
                existing_quantity + quantity
            )

            product_exists = True
            break

    #If product does not exist, create a new Product ID
    if not product_exists:
        product_id = next_product_id
        next_product_id += 1

        inventory_history.append(
            (product_id, product_name, quantity)
        )

    #Update inventory and delivery counter
    inventory = new_inventory
    deliveries += 1

    print(f"Delivery: {quantity}")
    print(f"Product ID: {product_id}")
    print(f"Product Name: {product_name}")
    print(f"Tax: {tax:.2f}")

#Generate Final Report
generate_report(inventory, deliveries, rejected, inventory_history)