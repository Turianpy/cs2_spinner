from pydantic import BaseModel

from typing import Optional


class ServerBase(BaseModel):
    name: str
    port: int
    rcon_port: int
    image: Optional[str] = "joedwards32/cs2:latest"
    detach: Optional[bool] = True


class ServerCreate(ServerBase):
    pass


class Server(ServerBase):
    pass
