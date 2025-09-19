※ 分散に関する設定の例であり、うまく動かない

Configレプリカセットの設定
```sh
docker exec -it $(docker ps -qf name=mongodb-cfg1-1) mongosh --eval '
rs.initiate({
  _id: "cfgRS",
  configsvr: true,
  members: [
    { _id: 0, host: "cfg1:27017" },
    { _id: 1, host: "cfg2:27017" },
    { _id: 2, host: "cfg3:27017" }
  ]
});'
```

シャード1の設定
```sh
docker exec -it $(docker ps -qf name=shard1a) mongosh --eval '
rs.initiate({
  _id: "shard1",
  members: [
    { _id: 0, host: "shard1a:27017" },
    { _id: 1, host: "shard1b:27017" }
  ]
});'
```

シャード2の設定
```sh
docker exec -it $(docker ps -qf name=shard2a) mongosh --eval '
rs.initiate({
  _id: "shard2",
  members: [
    { _id: 0, host: "shard2a:27017" },
    { _id: 1, host: "shard2b:27017" }
  ]
});'
```

mongosにシャード追加
```sh
docker exec -it $(docker ps -qf name=mongos) mongosh --eval '
sh.addShard("shard1/shard1a:27017,shard1b:27017");
sh.addShard("shard2/shard2a:27017,shard2b:27017");
sh.status();'
```

mongosでデータベース＆コレクションをシャーディング
```sh
# mongos に対して
docker exec -it $(docker ps -qf name=mongos) mongosh

// DB をシャーディング対象に
sh.enableSharding("appdb")

// 例1: ハッシュ分割（分散が均等になりやすい）
db.app.createIndex({ userId: "hashed" })
sh.shardCollection("appdb.app", { userId: "hashed" })

// 例2: レンジ分割（範囲検索が効く）
db.orders.createIndex({ createdAt: 1 })
sh.shardCollection("appdb.orders", { createdAt: 1 })
```

Pythonで接続
```python
from pymongo import MongoClient

# mongos はホストの 27018 に公開した前提
client = MongoClient("mongodb://localhost:27018/?retryWrites=true&w=majority")
db = client["appdb"]
```