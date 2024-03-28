import redis

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

def save_hiking_route_description(update, context):
    if context.args:
        route_name = context.args[0]
        # 保存路线名称到Redis
        redis_key = f"route:{update.effective_user.id}"
        redis_client.set(redis_key, route_name)
        
        reply_message = f"保存了名为 {route_name} 的徒步路线描述到Redis"
    else:
        reply_message = "请提供徒步路线名称作为参数"
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def share_hiking_route(update, context):
    redis_key = f"route:{update.effective_user.id}"
    route_name = redis_client.get(redis_key)
    
    if route_name:
        reply_message = f"分享名为 {route_name} 的徒步路线描述"
    else:
        reply_message = "未找到已保存的徒步路线描述"
    
    context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)
