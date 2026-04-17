import json
import sys
from pymongo import MongoClient


def load_data(json_file):
    # read the file in chunks to avoid loading everything into memory at once
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 load_json.py <json_file> <port_number>")
        sys.exit(1)

    json_file = sys.argv[1]
    port = int(sys.argv[2])

    # connect to mongodb
    client = MongoClient('localhost', port)
    db = client['291db']

    # drop and recreate the furniture collection
    if 'furniture' in db.list_collection_names():
        db['furniture'].drop()

    collection = db['furniture']

    data = load_data(json_file)

    # insert in batches of 100
    batch_size = 100
    total = 0
    for i in range(0, len(data), batch_size):
        batch = data[i:i + batch_size]
        collection.insert_many(batch)
        total += len(batch)

    print(f"Done. {total} items loaded into 291db.furniture.")
    client.close()


if __name__ == '__main__':
    main()
