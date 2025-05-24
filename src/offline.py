import socket
from src.database import Database
import uuid
from datetime import datetime


class OfflineManager:
    def __init__(self):
        try:
            self.db = Database()
        except Exception as e:
            print(f"Error in OfflineManager.__init__: {e}")
            raise

    def is_online(self):
        try:
            # Attempt to connect to localhost (loopback) on a common port (e.g., 80)
            # This checks if any network interface is active without external calls
            socket.create_connection(("127.0.0.1", 80), timeout=1).close()
            return True
        except (socket.timeout, socket.gaierror, ConnectionRefusedError, OSError):
            try:
                # Fallback: Check another local address (e.g., DNS server 8.8.8.8)
                # Still local to the network stack, no external packets sent
                socket.create_connection(("8.8.8.8", 53), timeout=1).close()
                return True
            except (socket.timeout, socket.gaierror, ConnectionRefusedError, OSError):
                return False

    def sync_if_online(self, sync_function):
        try:
            if self.is_online():
                return sync_function()
            return False, "Offline: Operation queued"
        except Exception as e:
            print(f"Error in sync_if_online: {e}")
            return False, str(e)

    def queue_operation(self, operation, entity, entity_id, data):
        try:
            queue_id = str(uuid.uuid4())
            created_at = datetime.now().isoformat()
            query = """
                INSERT INTO sync_queue (id, operation, entity, entity_id, data, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            self.db.execute(query, (queue_id, operation,
                            entity, entity_id, data, created_at))
            return True, "Operation queued"
        except Exception as e:
            print(f"Error in queue_operation: {e}")
            return False, str(e)

    def close(self):
        try:
            self.db.close()
        except Exception as e:
            print(f"Error in close: {e}")
            raise
