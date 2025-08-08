import os
import sys
import asyncio
import logging
from pathlib import Path
from datetime import datetime

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Import your FastAPI app and Tortoise config
from main import app
from core.tortoise_config import TORTOISE_ORM
from tortoise import Tortoise
from commands.__init__ import create_superuser

# Set up logging
log_file = os.path.join(current_dir, 'app_debug.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Global variables for database connection
db_initialized = False
loop = None

def initialize_db():
    """Initialize database connection"""
    global db_initialized, loop
    
    if not db_initialized:
        try:
            if loop is None:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            
            loop.run_until_complete(Tortoise.init(config=TORTOISE_ORM))
            db_initialized = True
            logger.info("Database connection initialized successfully")
            
            # Create superuser after database initialization
            try:
                loop.run_until_complete(create_superuser())
                logger.info("Superuser creation completed")
            except Exception as e:
                logger.error(f"Superuser creation error: {str(e)}")
                # Continue anyway, superuser might already exist
                
        except Exception as e:
            logger.error(f"Database initialization error: {str(e)}")
            # Continue anyway, let the app handle database errors

# Initialize database on module load
initialize_db()

def application(environ, start_response):
    """WSGI application wrapper for FastAPI with proper body handling"""
    
    # Ensure database is initialized
    if not db_initialized:
        initialize_db()
    
    # Get request method and debug info
    method = environ.get('REQUEST_METHOD', 'GET')
    content_type = environ.get('CONTENT_TYPE', '')
    content_length = int(environ.get('CONTENT_LENGTH', 0))
    path = environ.get('PATH_INFO', '')
    query = environ.get('QUERY_STRING', '')
    
    logger.info(f"=== Request Debug ===")
    logger.info(f"Method: {method}")
    logger.info(f"Path: {path}")
    logger.info(f"Query: {query}")
    logger.info(f"Content-Type: {content_type}")
    logger.info(f"Content-Length: {content_length}")
    
    # Get request body
    request_body = b''
    if content_length > 0:
        try:
            request_body = environ.get('wsgi.input').read(content_length)
            logger.info(f"Request body length: {len(request_body)} bytes")
            if request_body:
                logger.info(f"Request body preview: {request_body[:200]}")
        except Exception as e:
            logger.error(f"Error reading request body: {str(e)}")
            request_body = b''
    
    # Convert WSGI environ to ASGI scope
    headers = []
    for k, v in environ.items():
        if k.startswith('HTTP_'):
            # Convert HTTP_HEADER_NAME to header-name
            header_name = k[5:].lower().replace('_', '-')
            headers.append((header_name.encode(), v.encode()))
        elif k in ['CONTENT_TYPE', 'CONTENT_LENGTH']:
            headers.append((k.lower().encode(), v.encode()))
    
    logger.info(f"Total headers: {len(headers)}")
    for name, value in headers:
        logger.info(f"Header: {name.decode()} = {value.decode()}")
    
    scope = {
        'type': 'http',
        'asgi': {'version': '3.0', 'spec_version': '2.0'},
        'http_version': environ.get('SERVER_PROTOCOL', 'HTTP/1.1').split('/')[-1],
        'method': method,
        'scheme': environ.get('wsgi.url_scheme', 'http'),
        'server': (environ.get('SERVER_NAME', ''), int(environ.get('SERVER_PORT', 0))),
        'client': (environ.get('REMOTE_ADDR', ''), int(environ.get('REMOTE_PORT', 0))),
        'path': path,
        'query_string': query.encode(),
        'headers': headers,
        'raw_path': path.encode(),
    }
    
    # Response collector
    response_data = {'status': 200, 'headers': [], 'body': b''}
    
    async def receive():
        return {'type': 'http.request', 'body': request_body}
    
    async def send(message):
        if message['type'] == 'http.response.start':
            response_data['status'] = message['status']
            response_data['headers'] = message['headers']
        elif message['type'] == 'http.response.body':
            response_data['body'] += message['body']
    
    # Create event loop and run
    try:
        if loop is None:
            current_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(current_loop)
        else:
            current_loop = loop
            
        current_loop.run_until_complete(app(scope, receive, send))
        
        logger.info(f"=== Response Debug ===")
        logger.info(f"Status: {response_data['status']}")
        logger.info(f"Response headers: {len(response_data['headers'])}")
        logger.info(f"Response body length: {len(response_data['body'])}")
        
    except Exception as e:
        response_data['status'] = 500
        response_data['body'] = f'Internal Server Error: {str(e)}'.encode()
        logger.error(f"WSGI Error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
    
    # Send WSGI response
    status_line = f"{response_data['status']} OK"
    headers = [(k.decode(), v.decode()) for k, v in response_data['headers']]
    start_response(status_line, headers)
    
    return [response_data['body']] 