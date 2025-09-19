# publisher.py
import redis
import time
import random

r = redis.Redis()

players = ["Alice", "Bob", "Charlie", "Dave"]

while True:
    # ランダムにプレイヤーを選んでスコア加算
    player = random.choice(players)
    score = random.randint(1, 10)
    new_score = r.zincrby("leaderboard", score, player)

    # Pub/Sub で通知
    message = f"{player} scored {score} (total {int(new_score)})"
    r.publish("score_updates", message)
    print("[PUBLISH]", message)

    time.sleep(2)
