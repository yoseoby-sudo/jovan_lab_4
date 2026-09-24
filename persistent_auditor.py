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
                return 0, []
            
            #First line is the total inventory
            inventory = int(lines[0].strip())

            #Second line is the number of deliveries
            deliveries = int(lines[1].strip())

            #Remaining lines are the inventory history
            inventory_history = []

            for line in lines[2:]:
                inventory_history.append(int(line.strip()))

            return inventory, deliveries, inventory_history

    except FileNotFoundError:
        #If the file does not exist, start with empty inventory and history
        return 0, 0, []

def save_inventory(total, deliveries, history):
    #Save the inventory total and inventory history
    with open("inventory.txt", "w") as file:
        file.write(f"{total}\n")
        file.write(f"{deliveries}\n")

        for inventory_amount in history:
            file.write(f"{inventory_amount}\n")
    
def get_valid_input():
    #Prompt the user and return a valid integer or 'quit'
    while True:
        inventory_input = input("Enter stock: ")

        #Check for quit condition
        if inventory_input.lower() == "quit":
            return "quit"

        #Check if input is a valid number
        try:
            quantity = int(inventory_input)
        except ValueError:
            print("Error, Inventory must be a number")
            return None

        #Validate that number is not negative
        if quantity < 0:
            print("Error, Inventory cannot be negative")
            return None

        return quantity

def process_delivery(current_total, new_value):
    #Calculate and return the new inventory total
    return current_total + new_value

def calculate_tax(amount):
    #Calculate 10% tax for a delivery
    return amount * 0.10

def generate_report(total_units, failed_attempts):
    #Print the final inventory report
    print(f"Total Deliveries Processed: {deliveries}")
    print(f"Total Inventory Entered: {total_units}")
    print(f"Number of Failed/Rejected Entries: {failed_attempts}")
    print(f"Inventory History: {inventory_history}")

#Main program
inventory, deliveries, inventory_history = load_inventory()

print("Welcome to inventory taking")
print(f"Current Inventory: {inventory}")
print(f"Inventory History: {inventory_history}")

while True:

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
        break

    #Update inventory and delivery counter
    inventory = new_inventory
    deliveries += 1

    #Add the valid transaction to the history list
    inventory_history.append(quantity)  

    print(f"Delivery: {quantity}")
    print(f"Tax: {tax:.2f}")

#Generate Final Report
generate_report(inventory, rejected)