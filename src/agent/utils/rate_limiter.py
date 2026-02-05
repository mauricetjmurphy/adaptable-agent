"""Rate limiting utilities."""

import asyncio
import time
from typing import Optional
from collections import deque


class RateLimiter:
    """
    Token bucket rate limiter for API calls.
    
    Limits the rate of operations to prevent exceeding API limits.
    """
    
    def __init__(
        self,
        max_requests: int,
        time_window: float = 60.0
    ):
        """
        Initialize rate limiter.
        
        Args:
            max_requests: Maximum requests allowed in time window
            time_window: Time window in seconds
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self._requests: deque = deque()
        self._lock = asyncio.Lock()
    
    async def acquire(self, timeout: Optional[float] = None) -> bool:
        """
        Acquire permission to make a request.
        
        Blocks until a slot is available or timeout is reached.
        
        Args:
            timeout: Maximum time to wait in seconds
            
        Returns:
            True if acquired, False if timeout
        """
        start_time = time.time()
        
        while True:
            async with self._lock:
                now = time.time()
                
                # Remove old requests outside the window
                while self._requests and self._requests[0] < now - self.time_window:
                    self._requests.popleft()
                
                # Check if we can make a request
                if len(self._requests) < self.max_requests:
                    self._requests.append(now)
                    return True
                
                # Check timeout
                if timeout and (time.time() - start_time) >= timeout:
                    return False
                
            # Wait a bit before checking again
            await asyncio.sleep(0.1)
    
    def reset(self) -> None:
        """Reset the rate limiter."""
        self._requests.clear()
    
    def get_remaining(self) -> int:
        """Get the number of remaining requests in current window."""
        now = time.time()
        # Remove old requests
        while self._requests and self._requests[0] < now - self.time_window:
            self._requests.popleft()
        return self.max_requests - len(self._requests)
