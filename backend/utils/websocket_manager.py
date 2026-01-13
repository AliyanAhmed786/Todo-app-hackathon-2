import socketio
from typing import Dict, List
import jwt
from config import settings

# Create a Socket.IO server instance
sio = socketio.AsyncServer(
    cors_allowed_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
        "http://localhost:3002",
        "http://127.0.0.1:3002",
        "http://localhost:8000",  # Add the backend origin
        "http://127.0.0.1:8000"
    ],
    async_mode='asgi',
    logger=True,
    engineio_logger=True,
    cors_credentials=True  # Allow credentials for authentication
)
sio_app = socketio.ASGIApp(sio, socketio_path='/socket.io')

# Store active connections by user ID
active_connections: Dict[str, List[str]] = {}

@sio.event
async def connect(sid, environ, auth):
    """
    Handle new WebSocket connection with authentication.
    """
    print(f"WebSocket connection attempt: {sid}")

    try:
        # Try to get the token from the authorization header
        auth_header = environ.get('HTTP_AUTHORIZATION')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
        elif auth:  # Try to get token from auth object
            token = (auth or {}).get('token')
        else:
            # If no token, try to get user ID directly from auth (for development)
            user_id = (auth or {}).get('userId')
            if user_id:
                user_id = str(user_id)
                print(f"Connection accepted for user {user_id} (no auth required)")
                if user_id not in active_connections:
                    active_connections[user_id] = []
                active_connections[user_id].append(sid)
                return  # Accept connection without validation for development

            # Reject connection if no token or user ID provided
            print(f"Connection rejected: No token or user ID provided for {sid}")
            return False  # Reject the connection

        # Verify the JWT token
        payload = jwt.decode(token, settings.better_auth_secret, algorithms=[settings.algorithm])
        user_id = str(payload.get('user_id'))

        if user_id:
            print(f"Connection accepted for user {user_id}")
            if user_id not in active_connections:
                active_connections[user_id] = []
            active_connections[user_id].append(sid)
        else:
            print(f"Connection rejected: Invalid token for {sid}")
            return False  # Reject the connection

    except jwt.ExpiredSignatureError:
        print(f"Connection rejected: Token expired for {sid}")
        return False  # Reject the connection
    except jwt.InvalidTokenError:
        print(f"Connection rejected: Invalid token for {sid}")
        return False  # Reject the connection
    except Exception as e:
        print(f"Connection rejected: Error validating token for {sid}: {e}")
        return False  # Reject the connection

@sio.event
async def disconnect(sid):
    """
    Handle WebSocket disconnection.
    """
    print(f"WebSocket disconnected: {sid}")
    # Remove user from active connections
    for user_id, connections in active_connections.items():
        if sid in connections:
            connections.remove(sid)
            if not connections:  # Remove user if no more connections
                del active_connections[user_id]
            break

@sio.event
async def task_updated(sid, data):
    """
    Handle task update event from clients.
    This can be used to broadcast task changes to relevant users.
    """
    # Broadcast the task update to all connected clients for the same user
    user_id = None
    for uid, connections in active_connections.items():
        if sid in connections:
            user_id = uid
            break

    if user_id:
        await sio.emit('task-updated', data, room=user_id)

async def broadcast_dashboard_update(user_id: str, data: dict):
    """
    Broadcast dashboard update to all connected clients for a specific user.
    """
    if user_id in active_connections:
        for sid in active_connections[user_id]:
            try:
                await sio.emit('dashboard_update', data, room=sid)
            except Exception as e:
                print(f"Error broadcasting to {sid}: {e}")
                # Remove connection if it's no longer valid
                if sid in active_connections.get(user_id, []):
                    active_connections[user_id].remove(sid)
                    if not active_connections[user_id]:
                        del active_connections[user_id]

async def broadcast_to_all(data: dict):
    """
    Broadcast data to all connected clients.
    """
    await sio.emit('global_update', data)