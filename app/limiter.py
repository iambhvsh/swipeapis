from slowapi import Limiter
from slowapi.util import get_remote_address

# Create a global rate limiter using the client's IP address
limiter = Limiter(key_func=get_remote_address)
