import redis
import json
from hybrid_search.utils import singleton

@singleton
class Redis:
    def __init__(self):
        self.redis = redis.Redis(host = 'localhost', port=6379, decode_responses=True)

    def store_conversation(self, session_id, role, input):
        conversation = self.redis.get(session_id)
        if conversation:
            conversation = json.loads(conversation)
        else:
            conversation = []
        conversation.append({'role': role, 'content': input})
        self.redis.set(session_id, json.dumps(conversation))

    def get_conversation(self, session_id):
        conversation = self.redis.get(session_id)
        if conversation:
            return json.loads(conversation)
        return []
    
    def clear_conversation(self, session_id):
        self.redis.delete(session_id)