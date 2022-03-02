from dataclasses import asdict, dataclass
from dataclasses_json import dataclass_json
import json


@dataclass_json
@dataclass
class KademliaInfo:
    ip: str
    port: int
    followers: list
    following: list
    last_post_id: int

    @property
    def new_post_id(self):
        self.last_post_id += 1
        return self.last_post_id

    @property
    def serialize(self):
        return json.dumps(asdict(self))

    @staticmethod
    def deserialize(json_str: str):
        kademlia_info_json = json.loads(json_str)
        return KademliaInfo(
            kademlia_info_json["ip"],
            kademlia_info_json["port"],
            kademlia_info_json["followers"],
            kademlia_info_json["following"],
            kademlia_info_json["last_post_id"])
