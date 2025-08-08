import os
import sys
import asyncio
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import your FastAPI app and Tortoise config
from main import app
from core.tortoise_config import TORTOISE_ORM
from tortoise import Tortoise
from fastapi import Request
from starlette.responses import Response
from starlette.types import ASGIApp, Receive, Send, Scope
from commands.__init__ import create_superuser

# Create a synchronous WSGI wrapper
class SyncWSGIWrapper:
    def __init__(self, app: ASGIApp):
        self.app = app
        self.loop = None
        self.db_initialized = False
    
    def __call__(self, environ, start_response):
        # Create event loop if it doesn't exist
        if self.loop is None:
            self.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.loop)
        
        # Initialize database connection if not already done
        if not self.db_initialized:
            try:
                self.loop.run_until_complete(Tortoise.init(config=TORTOISE_ORM))
                self.db_initialized = True
                print("Database connection initialized successfully")
                
                # Create superuser after database initialization
                try:
                    self.loop.run_until_complete(create_superuser())
                    print("Superuser creation completed")
                except Exception as e:
                    print(f"Superuser creation error: {str(e)}")
                    # Continue anyway, superuser might already exist
                    
            except Exception as e:
                print(f"Database initialization error: {str(e)}")
                # Continue anyway, let the app handle database errors
        
        # Convert WSGI environ to ASGI scope
        headers = []
        for k, v in environ.items():
            if k.startswith('HTTP_'):
                # Convert HTTP_HEADER_NAME to header-name
                header_name = k[5:].lower().replace('_', '-')
                headers.append((header_name.encode(), v.encode()))
            elif k in ['CONTENT_TYPE', 'CONTENT_LENGTH']:
                headers.append((k.lower().encode(), v.encode()))
        
        # Debug: Print important headers
        print(f"Request method: {environ.get('REQUEST_METHOD', 'GET')}")
        print(f"Content-Type: {environ.get('CONTENT_TYPE', 'None')}")
        print(f"Content-Length: {environ.get('CONTENT_LENGTH', 'None')}")
        print(f"Authorization: {environ.get('HTTP_AUTHORIZATION', 'None')}")
        print(f"Total headers: {len(headers)}")
        
        scope = {
            'type': 'http',
            'asgi': {'version': '3.0', 'spec_version': '2.0'},
            'http_version': environ.get('SERVER_PROTOCOL', 'HTTP/1.1').split('/')[-1],
            'method': environ.get('REQUEST_METHOD', 'GET'),
            'scheme': environ.get('wsgi.url_scheme', 'http'),
            'server': (environ.get('SERVER_NAME', ''), int(environ.get('SERVER_PORT', 0))),
            'client': (environ.get('REMOTE_ADDR', ''), int(environ.get('REMOTE_PORT', 0))),
            'path': environ.get('PATH_INFO', ''),
            'query_string': environ.get('QUERY_STRING', '').encode(),
            'headers': headers,
            'raw_path': environ.get('PATH_INFO', '').encode(),
        }
        
        # Get request body from WSGI environ
        content_length = int(environ.get('CONTENT_LENGTH', 0))
        request_body = b''
        
        if content_length > 0:
            try:
                request_body = environ.get('wsgi.input').read(content_length)
                print(f"Request body length: {len(request_body)} bytes")
                if request_body:
                    print(f"Request body preview: {request_body[:100]}")
            except Exception as e:
                print(f"Error reading request body: {str(e)}")
                request_body = b''
        
        # Create response collector
        response_data = {'status': 200, 'headers': [], 'body': b''}
        
        async def receive():
            return {'type': 'http.request', 'body': request_body}
        
        async def send(message):
            if message['type'] == 'http.response.start':
                response_data['status'] = message['status']
                response_data['headers'] = message['headers']
            elif message['type'] == 'http.response.body':
                response_data['body'] += message['body']
        
        # Run the ASGI app
        try:
            # Debug: Print headers for authentication debugging
            auth_header = environ.get('HTTP_AUTHORIZATION', '')
            if auth_header:
                print(f"Authorization header found: {auth_header[:20]}...")
            else:
                print("No Authorization header found")
            
            self.loop.run_until_complete(self.app(scope, receive, send))
        except Exception as e:
            # Handle errors
            response_data['status'] = 500
            response_data['body'] = f'Internal Server Error: {str(e)}'.encode()
            import traceback
            print(f"Error in WSGI wrapper: {str(e)}")
            print(traceback.format_exc())
        
        # Send WSGI response
        status_line = f"{response_data['status']} OK"
        headers = [(k.decode(), v.decode()) for k, v in response_data['headers']]
        start_response(status_line, headers)
        
        return [response_data['body']]

# Create the WSGI application
application = SyncWSGIWrapper(app) 