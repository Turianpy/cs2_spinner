import os

import docker
from fastapi import FastAPI, HTTPException

from servers import schemas

client = docker.from_env()
app = FastAPI()


def update_used_ports():
    global USED_PORTS
    USED_PORTS = set()
    for container in client.containers.list():
        for port_bindings in container.attrs[
            'NetworkSettings'
        ]['Ports'].values():
            if port_bindings:
                for port_binding in port_bindings:
                    USED_PORTS.add(int(port_binding['HostPort']))


update_used_ports()


@app.get("/containers/")
def list_containers():
    containers = client.containers.list()
    serialized_containers = []
    for container in containers:
        serialized_containers.append({
            "id": container.id,
            "name": container.name,
            "status": container.status
        })
    return {"containers": serialized_containers}


@app.post("/containers/")
def create_container(
    server: schemas.ServerCreate
):
    try:
        container = client.containers.run(
            server.image,
            detach=True,
            name=server.name,
            environment={"SRCDS_TOKEN": os.getenv("SRCDS_TOKEN")},
            ports={
                "27015/tcp": server.port,
                "27015/udp": server.port,
                "27020/tcp": server.rcon_port
            }
        )
        USED_PORTS.add(server.port)
        USED_PORTS.add(server.rcon_port)
        return {
            "message": f"Conmtainer {server.name} created",
            "id": container.id
        }
    except docker.errors.APIError as e:
        return HTTPException(status_code=400, detail=str(e))


@app.get("/used-ports/")
def list_ports():
    """Lists all used ports"""
    return {"used_ports": list(USED_PORTS)}


@app.get("/available-ports/")
def list_available_ports(
    limit: int = 10
):
    """Lists 10 unoccupied ports in the range 27000 to 28000."""
    available_ports = []
    for port in range(27000, 28001):
        if port not in USED_PORTS:
            available_ports.append(port)
            if len(available_ports) == limit:
                break

    return {"available_ports": available_ports}


@app.get("/containers/{container_name}/logs")
def get_container_logs(container_name: str):
    try:
        container = client.containers.get(container_name)
        logs = container.logs().decode("utf-8")
        return {"logs": logs}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail="Container not found")


@app.post("/containers/{container_name}/exec")
def exec_command(container_name: str, command: str):
    container = client.containers.get(container_name)
    return {"output": container.exec_run(command)}


@app.post("/containers/{container_name}/restart")
def restart_container(container_name: str):
    container = client.containers.get(container_name)
    container.restart()
    return {"message": "Container restarted"}


@app.delete("/containers/{container_name}")
def delete_container(container_name: str):
    container = client.containers.get(container_name)
    container.remove()
    return {"message": "Container removed"}

@app.post("/containers/{container_name}/stop")
def stop_container(container_name: str):
    container = client.containers.get(container_name)
    container.stop()
    return {"message": "Container stopped"}


@app.post("/containers/{container_name}/start")
def start_container(container_name: str):
    container = client.containers.get(container_name)
    container.start()
    return {"message": "Container started"}


@app.get("/containers/{container_name}/config")
def get_container_config(container_name: str):
    """Returns the contents of the container's .env file"""
    container = client.containers.get(container_name)
    return {"config": container.attrs["Config"]["Env"]}


@app.patch("/containers/{container_name}/config")
def update_container_config(container_name: str, dotenv: str):
    """Updates the container's .env file"""
    container = client.containers.get(container_name)
    container.exec_run(f"echo {dotenv} > .env")
    return {"message": "Config updated"}
