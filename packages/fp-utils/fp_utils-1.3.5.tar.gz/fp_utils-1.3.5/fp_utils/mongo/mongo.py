from pymongo import MongoClient
import gridfs
from bson.objectid import ObjectId

def get_mongo_client(mongo_string):
    client = MongoClient(mongo_string)
    return client

def create_docs(client, database, collection, data, many=False):
    # Get db and collection.
    db = client[database]
    col = db[collection]

    if many:
        # Insert data.
        doc = col.insert_many(data)

        # Return doc id
        return doc.inserted_ids

    else:
        # Insert data.
        doc = col.insert_one(data)

        # Return doc id
        return doc.inserted_id


def get_docs(client, database, collection, query, many=False):
    # Get db and collectino
    db = client[database]
    col = db[collection]

    if many:
        # Find
        data = col.find(query)

        return [row for row in data]
    else:
        # Find
        data = col.find_one(query)

        return data


def update_docs(client, database, collection, query, data, upsert=False):
    # Get db and collectino
    db = client[database]
    col = db[collection]

    # Update one.
    col.update_one(query, data, upsert=upsert)


def delete_docs(client, database, collection, query):
    # Get db and collectino
    db = client[database]
    col = db[collection]

    # Update one.
    col.delete_one(query)

def get_file(client, database, file_id):
    fs = gridfs.GridFS(database=client[database])
    file_data = fs.find_one({"_id": ObjectId(file_id)})
    data = file_data.read()
    return data

def upload_file(client, database, file):
    fs = gridfs.GridFS(database=client[database])
    file_id = fs.put(file, file_name=str(file), content_type=str(file.content_type))
    return file_id
