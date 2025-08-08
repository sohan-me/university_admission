import os
import sys
import asyncio
import logging
import json
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

# Set up comprehensive logging
log_file = os.path.join(current_dir, 'debug_simple_multipart.log')
logging.basicConfig(
    level=logging.DEBUG,
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
    """WSGI application wrapper with simple multipart handling"""
    
    # Log the start of request processing
    logger.info("=" * 80)
    logger.info(f"NEW REQUEST STARTED AT {datetime.now()}")
    logger.info("=" * 80)
    
    # Ensure database is initialized
    if not db_initialized:
        initialize_db()
    
    # Get all request information
    method = environ.get('REQUEST_METHOD', 'GET')
    content_type = environ.get('CONTENT_TYPE', '')
    content_length = int(environ.get('CONTENT_LENGTH', 0))
    path = environ.get('PATH_INFO', '')
    query = environ.get('QUERY_STRING', '')
    
    logger.info("=== REQUEST DETAILS ===")
    logger.info(f"Method: {method}")
    logger.info(f"Path: {path}")
    logger.info(f"Query: {query}")
    logger.info(f"Content-Type: {content_type}")
    logger.info(f"Content-Length: {content_length}")
    
    # Check if this is a multipart form data request
    is_multipart = 'multipart/form-data' in content_type
    logger.info(f"Is multipart form data: {is_multipart}")
    
    # Get request body
    request_body = b''
    if content_length > 0:
        logger.info(f"Content-Length is {content_length}, reading body...")
        try:
            # Read the entire body at once
            request_body = environ.get('wsgi.input').read(content_length)
            logger.info(f"Successfully read {len(request_body)} bytes")
            
            if request_body and is_multipart:
                logger.info("=== MULTIPART BODY ANALYSIS ===")
                # Show first 500 bytes of multipart data
                body_preview = request_body[:500]
                logger.info(f"Multipart body preview: {body_preview}")
                
                # Try to find file data in multipart
                if b'filename=' in request_body:
                    logger.info("Found filename in multipart data")
                if b'Content-Type:' in request_body:
                    logger.info("Found Content-Type in multipart data")
                if b'Content-Disposition:' in request_body:
                    logger.info("Found Content-Disposition in multipart data")
                    
                # For multipart requests, we'll pass the raw body to FastAPI
                # and let it handle the parsing
                logger.info("Passing raw multipart body to FastAPI")
            elif request_body:
                try:
                    body_text = request_body.decode('utf-8', errors='ignore')
                    logger.info(f"Request body (UTF-8): {body_text}")
                except UnicodeDecodeError as e:
                    logger.error(f"Unicode decode error: {e}")
                    logger.info(f"Request body (raw bytes): {request_body}")
            else:
                logger.warning("Request body is empty despite content-length > 0")
                
        except Exception as e:
            logger.error(f"Error reading request body: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            request_body = b''
    else:
        logger.info("No content-length, trying to read available data...")
        try:
            # For requests without content-length, read what's available
            request_body = environ.get('wsgi.input').read()
            logger.info(f"Read {len(request_body)} bytes without content-length")
            if request_body:
                if is_multipart:
                    logger.info("Multipart data found without content-length")
                else:
                    try:
                        body_text = request_body.decode('utf-8', errors='ignore')
                        logger.info(f"Request body (no content-length): {body_text}")
                    except UnicodeDecodeError as e:
                        logger.error(f"Unicode decode error: {e}")
                        logger.info(f"Request body (raw bytes): {request_body}")
            else:
                logger.info("No data available to read")
        except Exception as e:
            logger.error(f"Error reading request body (no content-length): {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            request_body = b''
    
    # Convert WSGI environ to ASGI scope with detailed logging
    logger.info("=== HEADER CONVERSION ===")
    headers = []
    for k, v in environ.items():
        if k.startswith('HTTP_'):
            # Convert HTTP_HEADER_NAME to header-name
            header_name = k[5:].lower().replace('_', '-')
            headers.append((header_name.encode(), v.encode()))
            logger.info(f"Converted header: {k} -> {header_name} = {v}")
        elif k in ['CONTENT_TYPE', 'CONTENT_LENGTH']:
            headers.append((k.lower().encode(), v.encode()))
            logger.info(f"Added header: {k.lower()} = {v}")
    
    logger.info(f"Total headers: {len(headers)}")
    
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
    
    logger.info("=== ASGI SCOPE ===")
    logger.info(f"Scope: {json.dumps(scope, default=str, indent=2)}")
    
    # Response collector
    response_data = {'status': 200, 'headers': [], 'body': b''}
    
    async def receive():
        logger.info("=== RECEIVE CALLED ===")
        receive_data = {'type': 'http.request', 'body': request_body}
        logger.info(f"Receive data length: {len(request_body)} bytes")
        return receive_data
    
    async def send(message):
        logger.info(f"=== SEND CALLED: {message['type']} ===")
        if message['type'] == 'http.response.start':
            response_data['status'] = message['status']
            response_data['headers'] = message['headers']
            logger.info(f"Response status: {message['status']}")
            logger.info(f"Response headers: {message['headers']}")
        elif message['type'] == 'http.response.body':
            response_data['body'] += message['body']
            logger.info(f"Response body chunk: {len(message['body'])} bytes")
    
    # Create event loop and run
    logger.info("=== STARTING ASGI APP ===")
    try:
        if loop is None:
            current_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(current_loop)
            logger.info("Created new event loop")
        else:
            current_loop = loop
            logger.info("Using existing event loop")
            
        current_loop.run_until_complete(app(scope, receive, send))
        
        logger.info("=== ASGI APP COMPLETED ===")
        logger.info(f"Final status: {response_data['status']}")
        logger.info(f"Final headers: {len(response_data['headers'])}")
        logger.info(f"Final body length: {len(response_data['body'])}")
        if response_data['body']:
            try:
                body_text = response_data['body'].decode('utf-8', errors='ignore')
                logger.info(f"Final response body: {body_text}")
            except Exception as e:
                logger.error(f"Error decoding response body: {e}")
        
    except Exception as e:
        logger.error("=== ASGI APP ERROR ===")
        logger.error(f"Error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        
        response_data['status'] = 500
        response_data['body'] = f'Internal Server Error: {str(e)}'.encode()
    
    # Send WSGI response
    logger.info("=== SENDING WSGI RESPONSE ===")
    status_line = f"{response_data['status']} OK"
    headers = [(k.decode(), v.decode()) for k, v in response_data['headers']]
    logger.info(f"Status line: {status_line}")
    logger.info(f"Response headers: {headers}")
    
    start_response(status_line, headers)
    
    logger.info("=" * 80)
    logger.info(f"REQUEST COMPLETED AT {datetime.now()}")
    logger.info("=" * 80)
    
    return [response_data['body']]

# For direct ASGI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 