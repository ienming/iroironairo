import certifi
from pymongo import MongoClient
def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb+srv://root:root123@mycluster.uhrwact.mongodb.net/?retryWrites=true&w=majority"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING, tlsCAFile=certifi.where())
   db = client.test
   return db

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
   # Get the database
   dbname = get_database()