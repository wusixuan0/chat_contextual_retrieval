# src/types/chat_data.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict

@dataclass
class ChatStatus:
    state: str  # could be "processing", "embedded", "failed"
    timestamp: str

    @classmethod
    def from_dict(cls, data: dict) -> 'ChatStatus':
        return cls(
            state=data["state"],
            timestamp=data["timestamp"]
        )

    def to_dict(self) -> dict:
        return {
            "state": self.state,
            "timestamp": self.timestamp
        }

@dataclass
class ChatEntry:
    uuid: str
    url: str
    chat_file_path: str
    title: Optional[str] = None
    flow_file_path: Optional[str] = None
    status: ChatStatus = None

    def __post_init__(self):
        if self.status is None:
            self.status = ChatStatus(
                state="processing",
                timestamp=datetime.now().isoformat()
            )

    @classmethod
    def from_dict(cls, data: dict) -> 'ChatEntry':
        print(f"Converting chat data: {data}")
        required_fields = ['uuid', 'url', 'chat_file_path']
        missing = [f for f in required_fields if f not in data]
        if missing:
            raise ValueError(f"Missing required fields: {missing}")

        return cls(
            uuid=data["uuid"],
            url=data["url"],
            chat_file_path=data["chat_file_path"],
            title=data.get("title"),
            flow_file_path=data.get("flow_file_path"),
            status=ChatStatus.from_dict(data["status"]) if "status" in data else None
        )

    def to_dict(self) -> dict:
        return {
            "uuid": self.uuid,
            "url": self.url,
            "chat_file_path": self.chat_file_path,
            "title": self.title,
            "flow_file_path": self.flow_file_path,
            "status": self.status.to_dict()
        }

@dataclass
class Registry:
    last_updated: str
    chats: Dict[str, ChatEntry]

    @classmethod
    def from_dict(cls, data: dict) -> 'Registry':
        return cls(
            last_updated=data["last_updated"],
            chats={
                uuid: ChatEntry.from_dict(chat_data) 
                for uuid, chat_data in data["chats"].items()
            }
        )

    def to_dict(self) -> dict:
        return {
            "last_updated": self.last_updated,
            "chats": {
                uuid: chat.to_dict() 
                for uuid, chat in self.chats.items()
            }
        }