inventory = 0
rejected = 0
deliveries = 0

def load_inventory():
    # Load the previous inventory from inventory.txt
    try:
        with open("inventory.txt", "r") as file:
            inventory = int(file.readline().strip())
            return inventory

    except FileNotFoundError:
        # If the file does not exist, start with 0 inventory
        return 0
    
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

#Main program
inventory = load_inventory()

print("Welcome to inventory taking")
print(f"Current Inventory: {inventory}")

while True:

    quantity = get_valid_input()

    #Check for quit signal
    if quantity == "quit":
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

    print(f"Delivery: {quantity}")
    print(f"Tax: {tax:.2f}")


generate_report(inventory, rejected)