import socketio
import uvicorn

sio = socketio.AsyncServer()
app = socketio.ASGIApp(sio, static_files={'/': './public/'})

connected_clients = set()

@sio.event
async def connect(sid, environ):
    connected_clients.add(sid)
    await sio.emit('message', {'username': 'Server', 'message': 'A user has connected', 'timestamp': ''}, room=sid)
    print(f'Client {sid} connected')

@sio.event
async def disconnect(sid):
    connected_clients.remove(sid)
    await sio.emit('message', {'username': 'Server', 'message': 'A user has disconnected', 'timestamp': ''})
    print(f'Client {sid} disconnected')

@sio.event
async def message(sid, data):
    await sio.emit('message', data)
    print(f'Message from {data["username"]}: {data["message"]}')

@sio.event
async def edit_message(sid, data):
    await sio.emit('edit_message', data)
    print(f'Message edited by {data["username"]}: {data["message"]}')

@sio.event
async def delete_message(sid, data):
    await sio.emit('delete_message', data)
    print(f'Message deleted by {data["username"]}')

@sio.event
async def typing(sid, data):
    await sio.emit('typing', data, skip_sid=sid)
    print(f'{data["username"]} is typing...')

if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5000)
