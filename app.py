from flask import Flask, jsonify
import redis

app = Flask(__name__)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def get_greetings_from_redis():
    cached_greeting = redis_client.get('latest_greeting')
    if cached_greeting:
        return cached_greeting
    else:
        # If the greeting is not cached in Redis, fetch it and cache it
        greeting = {"greeting": "Hello from Python App!"}
        redis_client.set('latest_greeting', greeting["greeting"])
        return greeting["greeting"]

@app.route('/greetings')
def greetings():
    greeting = get_greetings_from_redis()
    return jsonify({"greeting": greeting})

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=3000)
