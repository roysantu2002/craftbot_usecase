
import sys
print(sys.path)

from backend.wsgi import application as wsgi_application  # Replace with your WSGI application reference
from backend.asgi import application as asgi_application  # Replace with your ASGI application reference

bind = "0.0.0.0:8000"
workers = 4  # Adjust the number of workers as needed

# Specify the application for both HTTP and WebSocket
applications = {
    "/": wsgi_application,
    "/ws": asgi_application,
}


