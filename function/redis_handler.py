import redis

# 创建Redis连接
redis1 = redis.Redis(host='localhost', port=6379, db=0)

def save_data(update, context):
    try:
        user_id = update.effective_user.id
        data = context.args
        
        # 构建键值对字典
        key_value_pairs = {}
        for i in range(len(data)):
            key = f"{user_id}:{i+1}"
            value = data[i]
            key_value_pairs[key] = value
        
        # 批量存储数据
        redis1.mset(key_value_pairs)
        
        update.message.reply_text('Data saved successfully.')
    except IndexError:
        update.message.reply_text('Usage: /save <data1> <data2> ...')

def get_data(update, context):
    try:
        user_id = update.effective_user.id
        
        # 获取所有键
        keys = redis1.keys(f"{user_id}:*")
        
        # 遍历每个键，并获取对应的值
        data = []
        for key in keys:
            value = redis1.get(key)
            data.append((key.decode('UTF-8'), value.decode('UTF-8')))
        
        # 构建查询结果
        result = ""
        for key, value in data:
            result += f"Key: {key}, Value: {value}\n"
        
        # 回复查询结果
        if result:
            update.message.reply_text(result)
        else:
            update.message.reply_text("No data found.")
    except IndexError:
        update.message.reply_text('Usage: /get')