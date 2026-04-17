import sys
import re
from pymongo import MongoClient


def discount_check(collection):
    while True:
        name = input("\nEnter furniture name: ").strip()

        matches = list(collection.find({"name": name}))

        if not matches:
            print("No furniture found with that name.")
        else:
            if len(matches) > 1:
                print("\nMultiple items found:")
                for item in matches:
                    print(f"  ID: {item['item_id']}  |  Name: {item['name']}")
                while True:
                    chosen = input("Enter the ID of the item you want: ").strip()
                    filtered = [x for x in matches if x['item_id'] == chosen]
                    if filtered:
                        matches = filtered
                        break
                    print("Invalid ID, please try again.")

            item = matches[0]
            old_price = item.get('old_price')
            price = item.get('price', 0)

            if old_price is not None and old_price > price:
                print(f"\nName: {item['name']}")
                print(f"Category: {item['category']}")
                print(f"Price: ${item['price']}")
            else:
                print("This furniture is not on discount.")

        choice = input("\nPress Enter to check another, or 'b' to go back: ").strip().lower()
        if choice == 'b':
            break


def keyword_search(collection):
    while True:
        keyword = input("\nEnter keyword to search: ").strip()

        pattern = re.escape(keyword)
        results = list(collection.find({"name": {"$regex": pattern}}))

        if not results:
            print("No results found.")
        else:
            per_page = 5
            page = 0
            total_pages = (len(results) + per_page - 1) // per_page

            while True:
                start = page * per_page
                end = min(start + per_page, len(results))

                print(f"\n--- Page {page + 1} of {total_pages} ---")
                for item in results[start:end]:
                    print(f"  Name: {item['name']}")
                    print(f"  Category: {item['category']}")
                    print(f"  Price: ${item['price']}")
                    print(f"  Description: {item.get('short_description', 'N/A')}")
                    print()

                if total_pages <= 1:
                    break

                nav = input("  [n]ext  [p]revious  [q]uit: ").strip().lower()
                if nav == 'n' and page < total_pages - 1:
                    page += 1
                elif nav == 'p' and page > 0:
                    page -= 1
                elif nav == 'q':
                    break
                else:
                    print("  Invalid input, try again.")

        choice = input("\nPress Enter to search again, or 'b' to go back: ").strip().lower()
        if choice == 'b':
            break


def category_search(collection):
    while True:
        categories = sorted(collection.distinct("category"))

        if not categories:
            print("No categories found in database.")
            return

        print("\n--- Categories ---")
        for i, cat in enumerate(categories, 1):
            print(f"  {i}. {cat}")

        while True:
            try:
                choice = int(input("\nSelect a category number: ").strip())
            except ValueError:
                print("Invalid input, please enter a number.")
                continue
            if choice < 1 or choice > len(categories):
                print("Invalid selection, please try again.")
                continue
            break

        selected = categories[choice - 1]

        items = list(collection.find({"category": selected}).sort("price", -1))

        if not items:
            print("No items found in this category.")
        else:
            per_page = 5
            page = 0
            total_pages = (len(items) + per_page - 1) // per_page

            while True:
                start = page * per_page
                end = min(start + per_page, len(items))
                page_items = items[start:end]

                print(f"\n--- {selected} | Page {page + 1} of {total_pages} ---")
                for i, item in enumerate(page_items, 1):
                    print(f"  {i}. {item['name']} (ID: {item['item_id']}) - ${item['price']}")

                cmd = input("\n  Enter item # for details, [n]ext, [p]revious, [q]uit: ").strip().lower()

                if cmd == 'n':
                    if page < total_pages - 1:
                        page += 1
                    else:
                        print("  Already on last page.")
                elif cmd == 'p':
                    if page > 0:
                        page -= 1
                    else:
                        print("  Already on first page.")
                elif cmd == 'q':
                    break
                elif cmd.isdigit():
                    idx = int(cmd) - 1
                    if 0 <= idx < len(page_items):
                        item = page_items[idx]
                        print(f"\n  Name: {item['name']}")
                        print(f"  Category: {item['category']}")
                        print(f"  Price: ${item['price']}")
                        print(f"  Description: {item.get('short_description', 'N/A')}")
                        print(f"  Designer: {item.get('designer', 'N/A')}")
                    else:
                        print("  Invalid item number.")
                else:
                    print("  Invalid input.")

        choice = input("\nPress Enter to pick another category, or 'b' to go back: ").strip().lower()
        if choice == 'b':
            break


def add_item(collection):
    while True:
        print()
        while True:
            item_id = input("Enter item ID: ").strip()
            if collection.find_one({"item_id": item_id}):
                print("Error: This ID already exists. Please enter a different ID.")
                continue
            break

        name = input("Enter name: ").strip()
        category = input("Enter category: ").strip()

        while True:
            try:
                price = float(input("Enter price: ").strip())
                break
            except ValueError:
                print("Error: Price must be a number. Please try again.")

        short_desc = input("Enter short description: ").strip()
        designer = input("Enter designer: ").strip()

        new_item = {
            "item_id": item_id,
            "name": name,
            "category": category,
            "price": price,
            "old_price": None,
            "sellable_online": None,
            "other_colors": None,
            "short_description": short_desc,
            "designer": designer,
            "depth": None,
            "height": None,
            "width": None
        }

        try:
            collection.insert_one(new_item)
            print("Item successfully added!")
        except Exception as e:
            print(f"Failed to add item: {e}")

        choice = input("\nPress Enter to add another, or 'b' to go back: ").strip().lower()
        if choice == 'b':
            break


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 main.py <port_number>")
        sys.exit(1)

    port = int(sys.argv[1])
    client = MongoClient('localhost', port)
    db = client['291db']
    collection = db['furniture']

    while True:
        print("\n=============================")
        print("   IKEA Furniture Database   ")
        print("=============================")
        print("1. Discount Check")
        print("2. Keyword Search")
        print("3. Category Search")
        print("4. Add New Item")
        print("5. Exit")

        choice = input("\nChoose an option: ").strip()

        if choice == '1':
            discount_check(collection)
        elif choice == '2':
            keyword_search(collection)
        elif choice == '3':
            category_search(collection)
        elif choice == '4':
            add_item(collection)
        elif choice == '5':
            print("Exiting. Goodbye!")
            client.close()
            sys.exit(0)
        else:
            print("Invalid option, please try again.")


if __name__ == '__main__':
    main()
