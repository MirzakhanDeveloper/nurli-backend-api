from fastapi import WebSocket

class ConnectionManager:
    def __init__(self):
        # Barcha tinglab turgan qurilmalar (Web, Desktop, Mobil) ro'yxati
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    # Yangi davomat kelganda hammaga tarqatuvchi funksiya
    async def broadcast_json(self, message: dict):
        for connection in self.active_connections:
            await connection.send_json(message)

manager = ConnectionManager()