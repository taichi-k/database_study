from cassandra.cluster import Cluster
import uuid

cluster = Cluster(["127.0.0.1"], port=9042)
session = cluster.connect()

session.execute("""
CREATE KEYSPACE IF NOT EXISTS demo
WITH replication = {'class': 'SimpleStrategy', 'replication_factor': 1}
""")
session.set_keyspace("demo")

session.execute("""
CREATE TABLE IF NOT EXISTS items (
  id uuid PRIMARY KEY,
  value text
)
""")

for i in range(100000):
    session.execute("INSERT INTO items (id, value) VALUES (%s, %s)",
                    (uuid.uuid4(), f"value-{i}"))

cluster.shutdown()
