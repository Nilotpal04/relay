from relay.realtime.manager import ConnectionManager
from relay.realtime.publisher import InMemoryEventPublisher

connection_manager = ConnectionManager()

event_publisher = InMemoryEventPublisher(connection_manager)
