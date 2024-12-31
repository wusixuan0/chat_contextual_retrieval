from src.util.util import write_text_file, read_text_file, write_json_file, load_json_file
from datetime import datetime
# from filelock import FileLock
# TODO: add filelock and error handling for data structure validation
# if not isinstance(chat, dict) or 'uuid' not in chat:
#     raise ValueError(f"Invalid chat data structure: {chat}")
class ChatRegistry:
    def __init__(self, registry_path='./data/chat_registry.json'):
        self.registry_path = registry_path

    def get_unprocessed_chats(self):
        # Returns list of chat dicts from registry where status is missing
        chats = self._load_registry()
        return [chat for chat in chats['chats'] if 'status' not in chat or chat['status'] != "embedded"]

    def get_chats(self, uuids):
        # Returns list of chat dicts from registry matching given uuids
        chats = self._load_registry()
        return [chat for chat in chats['chats'] if chat['uuid'] in uuids]

    def mark_chat_status(self, uuid, status):
        # Atomic update to add status: "processing", "complete", "failed"
        # with FileLock(self.registry_path + '.lock'):
        chats = self._load_registry()
        chat = self._find_chat(chats, uuid)

        timestamp = datetime.now().isoformat()
        chats['last_updated'] = timestamp
        chat['status'] = {
            'state': status,
            'timestamp': timestamp
        }

        self._save_registry(chats)

    def _load_registry(self):
        return load_json_file(file_path=self.registry_path)

    def _save_registry(self, chats):
        write_json_file(data=chats, file_path=self.registry_path)

    def _find_chat(self, chats, uuid):
        return [chat for chat in chats['chats'] if chat['uuid'] == uuid][0]