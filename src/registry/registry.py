# src/registry/registry.py
import json
from datetime import datetime
from src.types.chat_data import Registry, ChatEntry, ChatStatus

class ChatRegistry:
    def __init__(self, registry_path='./data/chat_registry.json'):
        self.registry_path = registry_path
        self.registry = self._load_registry()

    def _load_registry(self) -> Registry:
        try:
            with open(self.registry_path, 'r') as f:
                data = json.load(f)
                print("Loaded registry data:", json.dumps(data, indent=2))
                return Registry.from_dict(data)
        except FileNotFoundError:
            # Initialize empty registry
            return Registry(
                last_updated=datetime.now().isoformat(),
                chats={}
            )

    def _save_registry(self):
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry.to_dict(), f, indent=2)

    def add_chat(self, url: str, chat_file_path: str, uuid: str, 
                 title: str = None, flow_file_path: str = None) -> str:
        if uuid in self.registry.chats and self.registry.chats[uuid].status.state != "failed":
            raise ValueError(f"Chat with UUID {uuid} already exists")

        chat_entry = ChatEntry(
            uuid=uuid,
            url=url,
            chat_file_path=chat_file_path,
            title=title,
            flow_file_path=flow_file_path
        )
        
        self.registry.chats[uuid] = chat_entry
        self.registry.last_updated = datetime.now().isoformat()
        self._save_registry()
        return uuid

    def mark_chat_status(self, uuid: str, state: str):
        if uuid not in self.registry.chats:
            raise ValueError(f"Chat with UUID {uuid} not found")
            
        chat = self.registry.chats[uuid]
        chat.status = ChatStatus(
            state=state,
            timestamp=datetime.now().isoformat()
        )
        self.registry.last_updated = datetime.now().isoformat()
        self._save_registry()

    def get_chat(self, uuid: str) -> ChatEntry:
        if uuid not in self.registry.chats:
            raise ValueError(f"Chat with UUID {uuid} not found")
        return self.registry.chats[uuid]

    def get_unprocessed_chats(self) -> list[ChatEntry]:
        return [
            chat for chat in self.registry.chats.values()
            if chat.status.state in ["processing", "failed"]
        ]