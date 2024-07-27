import asyncio
import socketio

sio = socketio.AsyncServer()
app = socketio.ASGIApp(sio)

connected_clients = set()

@sio.event
async def connect(sid, environ):
    connected_clients.add(sid)
    await sio.emit('message', {'username': 'Server', 'message': 'A user has connected'}, room=sid)
    print(f'Client {sid} connected')

@sio.event
async def disconnect(sid):
    connected_clients.remove(sid)
    await sio.emit('message', {'username': 'Server', 'message': 'A user has disconnected'})
    print(f'Client {sid} disconnected')

@sio.event
async def message(sid, data):
    await sio.emit('message', data)
    print(f'Message from {data["username"]}: {data["message"]}')

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=5000)
