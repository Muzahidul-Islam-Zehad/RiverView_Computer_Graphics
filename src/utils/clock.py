"""
Clock class for managing time and animation.
"""

import time


class Clock:
    """Manages time and frame delta calculations."""

    def __init__(self):
        """Initialize clock."""
        self.start_time = time.time()
        self.last_time = self.start_time
        self.current_time = self.start_time
        self.delta_time = 0.0
        self.elapsed_time = 0.0
        self.frame_count = 0
        self.fps = 0.0

    def tick(self):
        """Update clock for new frame."""
        self.last_time = self.current_time
        self.current_time = time.time()
        self.delta_time = self.current_time - self.last_time
        self.elapsed_time = self.current_time - self.start_time
        self.frame_count += 1

    def get_delta_time(self):
        """Get time since last tick."""
        return self.delta_time

    def get_elapsed_time(self):
        """Get total elapsed time."""
        return self.elapsed_time

    def get_fps(self):
        """Get average FPS."""
        if self.elapsed_time > 0:
            return self.frame_count / self.elapsed_time
        return 0.0

    def reset(self):
        """Reset clock."""
        self.start_time = time.time()
        self.last_time = self.start_time
        self.current_time = self.start_time
        self.delta_time = 0.0
        self.elapsed_time = 0.0
        self.frame_count = 0
