from typing import Optional

from pydantic import BaseModel


class ServerBase(BaseModel):
    name: str
    port: int
    rcon_port: int
    image: Optional[str] = "joedwards32/cs2:latest"


class ServerCreate(ServerBase):
    pass


class Server(ServerBase):
    pass
