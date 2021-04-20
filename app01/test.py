import redis

conn = redis.Redis(host='192.168.61.129', port=6379, password='redis123', encoding='utf-8')

conn.set('15568595905', 9999, ex=10)

value = conn.get('15568595905')
print(value)
