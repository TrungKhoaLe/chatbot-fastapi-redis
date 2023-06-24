import os
from fastapi import APIRouter, FastAPI, WebSocket, Request
from fastapi import HTTPException, BackgroundTasks
from fastapi import WebSocketDisconnect
from fastapi import Depends
from ..socket import ConnectionManager
from ..socket.utils import get_token
import uuid

chat = APIRouter()
manager = ConnectionManager()


@chat.post("/token")
async def token_generator(name: str, request: Request):
    if not name:
        raise HTTPException(
                status_code=400,
                detail={
                    "loc": "name",
                    "msg": "Please enter a valid name"
                    }
                )
    token = str(uuid.uuid4())
    data = {"name": name, "token": token}
    return data


@chat.post("/refresh_token")
async def refresh_token(request: Request):
    return None


@chat.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket, token: str = Depends(get_token)):
    await manager.connect(websocket)
    try:
        while True:
            # receive any messages sent by the client
            data = await websocket.receive_text()
            print(data)
            await manager.send_personal_message(f"Response: Simulating response from the GPT service", websocket)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
