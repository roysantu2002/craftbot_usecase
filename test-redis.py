import redis

r = redis.Redis(host='192.168.1.101', port=6379)

try:
    response = r.ping()
    if response:
        print("Connected to Redis successfully!")
except Exception as e:
    print(f"Error connecting to Redis: {str(e)}")
