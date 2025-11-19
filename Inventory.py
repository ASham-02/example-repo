# The beginning of the class
class Shoe:
    def __init__(self, country, code, product, cost, quantity):
        """
        country: str
        code: str
        product: str
        cost: number-like (str/float/int)
        quantity: number-like (str/int)
        """
        self.country = country.strip()
        self.code = code.strip()
        self.product = product.strip()
        self.cost = float(cost)
        self.quantity = int(quantity)

    def get_cost(self):
        """Return the cost of the shoe."""
        return self.cost

    def get_quantity(self):
        """Return the quantity of the shoe."""
        return self.quantity

    def __str__(self):
        """Human-readable, user-friendly representation of a shoe."""
        return f"{self.country} | {self.code} | {self.product} | £{self.cost:.2f} | Qty: {self.quantity}"

# Shoe list
"""
This list stores Shoe objects kept in memory while the program runs.
"""
shoe_list = []

INVENTORY_FILE = "inventory.txt"
HEADER = "Country,Code,Product,Cost,Quantity\n"


def _write_all_shoes_to_file():
    """Rewrite inventory.txt from the current in-memory shoe_list."""
    try:
        with open(INVENTORY_FILE, "w", encoding="utf-8") as f:
            f.write(HEADER)
            for s in shoe_list:
                f.write(f"{s.country},{s.code},{s.product},{s.cost},{s.quantity}\n")
    except Exception as e:
        print(f"Error writing to {INVENTORY_FILE}: {e}")


# Functions outside the class
def read_shoes_data():
    """
    Open inventory.txt, read each line (skipping header),
    create Shoe objects, and append them to shoe_list.
    Uses try/except for defensive error handling.
    """
    shoe_list.clear()  
    try:
        with open(INVENTORY_FILE, "r", encoding="utf-8") as f:
            header_line = next(f, None)
            if header_line is None:
                print("Warning: inventory.txt is empty.")
                return

            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split(",")]
                if len(parts) != 5:
                    print(f"Skipping malformed line: {line}")
                    continue
                country, code, product, cost, quantity = parts
                try:
                    shoe_list.append(Shoe(country, code, product, float(cost), int(quantity)))
                except ValueError:
                    print(f"Skipping line with invalid numbers: {line}")
        print(f"Loaded {len(shoe_list)} shoe records.")
    except FileNotFoundError:
        print(f"Error: {INVENTORY_FILE} not found. Creating a new one.")
        # Create a fresh file with header so future writes are clean
        with open(INVENTORY_FILE, "w", encoding="utf-8") as f:
            f.write(HEADER)
    except Exception as e:
        print(f"Unexpected error while reading {INVENTORY_FILE}: {e}")


def capture_shoes():
    """
    Prompt user for shoe fields, create a Shoe, add to list,
    and append to the file.
    """
    try:
        country = input("Country: ").strip()
        code = input("Code: ").strip()
        product = input("Product: ").strip()
        cost = float(input("Cost (e.g. 1299.99): ").strip())
        quantity = int(input("Quantity (integer): ").strip())

        s = Shoe(country, code, product, cost, quantity)
        shoe_list.append(s)

        # Append to file (keeps file and memory in sync)
        with open(INVENTORY_FILE, "a", encoding="utf-8") as f:
            # If file is brand-new or only has header, appending is fine.
            f.write(f"{s.country},{s.code},{s.product},{s.cost},{s.quantity}\n")

        print("Shoe captured successfully.")
    except ValueError:
        print("Invalid input: cost must be a number and quantity must be an integer.")
    except Exception as e:
        print(f"Unexpected error while capturing shoe: {e}")


def view_all():
    """
    Iterate over shoe_list and print details via __str__.
    """
    if not shoe_list:
        print("No data loaded. Use option [1] to load inventory first.")
        return

    print("\n--- INVENTORY ---")
    print("Country | Code | Product | Cost | Quantity")
    print("-" * 60)
    for s in shoe_list:
        print(s)


def re_stock():
    """
    Find the shoe with the *lowest* quantity and offer to restock it.
    Persist the updated quantity back to file.
    """
    if not shoe_list:
        print("No data loaded. Use option [1] to load inventory first.")
        return

    lowest = min(shoe_list, key=lambda s: s.quantity)
    print("\nLowest stock item:")
    print(lowest)

    try:
        add = int(input("How many units would you like to add? (0 to cancel): ").strip())
        if add < 0:
            print("Quantity to add cannot be negative.")
            return
        if add == 0:
            print("Restock cancelled.")
            return

        lowest.quantity += add
        print(f"Updated quantity for {lowest.product}: {lowest.quantity}")

        # Persist the change
        _write_all_shoes_to_file()

    except ValueError:
        print("Please enter a valid integer.")


def search_shoe():
    """
    Search for a shoe by code (case-insensitive) and print it.
    """
    if not shoe_list:
        print("No data loaded. Use option [1] to load inventory first.")
        return

    code = input("Enter shoe code to search: ").strip().lower()
    for s in shoe_list:
        if s.code.lower() == code:
            print("\nShoe found:")
            print(s)
            return
    print("No shoe found with that code.")


def value_per_item():
    """
    Calculate and print value = cost * quantity for all shoes.
    """
    if not shoe_list:
        print("No data loaded. Use option [1] to load inventory first.")
        return

    print("\n--- TOTAL VALUE PER ITEM ---")
    for s in shoe_list:
        value = s.get_cost() * s.get_quantity()
        print(f"{s.product} ({s.code}) -> £{value:.2f}")


def highest_qty():
    """
    Find the product with the *highest* quantity and print as 'for sale'.
    """
    if not shoe_list:
        print("No data loaded. Use option [1] to load inventory first.")
        return

    highest = max(shoe_list, key=lambda s: s.quantity)
    print(f"\nProduct on SALE: {highest.product} ({highest.code}) - Stock: {highest.quantity}")


# Main Menu for 
def main():
    """
    Menu loop to execute each function.
    """
    while True:
        print("\n=== NIKE INVENTORY MENU ===")
        print("1. Read data from file")
        print("2. View all shoes")
        print("3. Capture new shoe")
        print("4. Restock lowest-quantity shoe")
        print("5. Search shoe by code")
        print("6. Show total value per item")
        print("7. Show product on sale (highest quantity)")
        print("8. Exit")

        choice = input("Choose an option (1-8): ").strip()

        if choice == "1":
            read_shoes_data()
        elif choice == "2":
            view_all()
        elif choice == "3":
            capture_shoes()
        elif choice == "4":
            re_stock()
        elif choice == "5":
            search_shoe()
        elif choice == "6":
            value_per_item()
        elif choice == "7":
            highest_qty()
        elif choice == "8":
            print("Goodbye!")
            break
        else:
            print("Invalid selection. Please choose 1–8.")


if __name__ == "__main__":
    main()
