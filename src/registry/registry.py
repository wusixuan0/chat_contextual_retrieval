from src.util.util import write_text_file, read_text_file, write_json_file, load_json_file

class ChatRegistry:
    def __init__(self, registry_path='./data/chat_registry.json'):
        self.registry_path = registry_path
        
    def get_unprocessed_chats(self):
        # Returns list of chat dicts from registry where status is missing
        chats = self._load_registry()
        return [chat for chat in chats if 'status' not in chat]
    
    def get_chats(self, uuids):
        # Returns list of chat dicts from registry matching given uuids
        chats = self._load_registry()
        return [chat for chat in chats if chat['uuid'] in uuids]

    def mark_chat_status(self, uuid, status):
        # Atomic update to add status: "processing", "complete", "failed"
        with FileLock(self.registry_path + '.lock'):
            chats = self._load_registry()
            chat = self._find_chat(chats, uuid)
            chat['status'] = {
                'state': status,
                'start_time': datetime.now().isoformat()
            }
            self._save_registry(chats)

    def _load_registry(self):
        load_json_file(file_path=self.registry_path)

    def _save_registry(self, chats):
        write_json_file(data=chats, file_path=self.registry_path)

    def _find_chat(self, chats, uuid):
        return [chat for chat in chats if chat['uuid'] == uuid][0]
