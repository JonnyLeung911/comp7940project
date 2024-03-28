import redis

# 创建Redis连接
redis1 = redis.Redis(host='localhost', port=6379, db=0)

def write_review(tv_show, review):
    # 将评论存储到Redis中
    redis1.set(tv_show, review)

def read_review(tv_show):
    # 从Redis中获取评论内容
    review = redis1.get(tv_show)
    return review.decode('UTF-8') if review else None