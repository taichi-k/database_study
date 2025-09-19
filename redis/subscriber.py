# subscriber.py
import redis

r = redis.Redis()
pubsub = r.pubsub()
pubsub.subscribe("score_updates")

print("Listening for score updates...")

for message in pubsub.listen():
    if message["type"] == "message":
        print("[SUBSCRIBE]", message["data"].decode("utf-8"))

        # 最新ランキングを取得
        leaderboard = r.zrevrange("leaderboard", 0, -1, withscores=True)
        print("Current Leaderboard:")
        for rank, (player, score) in enumerate(leaderboard, start=1):
            print(f" {rank}. {player.decode('utf-8')} - {int(score)}")
        print("-" * 30)
