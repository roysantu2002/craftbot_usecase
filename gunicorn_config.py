from backend.asgi import application as asgi_application
from backend.wsgi import application as wsgi_application

bind = "0.0.0.0:8000"
workers = 4  # Adjust the number of workers as needed

# Use uvicorn as the worker class and specify both ASGI and WSGI applications
worker_class = "uvicorn.workers.UvicornWorker"

# Specify the application for both HTTP and WebSocket
applications = {
    "/": wsgi_application,
    "/ws": asgi_application,
}

