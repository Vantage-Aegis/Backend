import os
from pymongo import MongoClient
import searoute
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("MONGODB_URI")
db_name = os.getenv("DATABASE_NAME")

client = MongoClient(uri)
db = client[db_name]

# Fetch all nodes (suppliers and ports) to get their coordinates
suppliers = {s["_id"]: s for s in db.suppliers.find()}
ports = {p["_id"]: p for p in db.ports.find()}

# Combine them for easy lookup
nodes = {**suppliers, **ports}

routes_updated = 0
for route in db.routes.find():
    from_id = route.get("from_node")
    to_id = route.get("to_node")
    
    if from_id and from_id.startswith("sup_") and to_id and to_id.startswith("port_"):
        u = nodes.get(from_id)
        v = nodes.get(to_id)
        
        if u and v:
            origin = [u["lng"], u["lat"]]
            destination = [v["lng"], v["lat"]]
            
            try:
                # Calculate sea route
                res = searoute.searoute(origin, destination)
                waypoints = [[coord[1], coord[0]] for coord in res['geometry']['coordinates']]
                
                # Update route in DB
                db.routes.update_one(
                    {"_id": route["_id"]},
                    {"$set": {"waypoints": waypoints}}
                )
                print(f"Updated {route['_id']} with {len(waypoints)} waypoints.")
                routes_updated += 1
            except Exception as e:
                print(f"Error for route {route['_id']}: {e}")

print(f"Successfully updated {routes_updated} routes in MongoDB.")
