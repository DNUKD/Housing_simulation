import threading
import time

# Current values to UI
animated = {}

# Target values
targets = {}

# Flag indicating new values
dirty = False


# Set a new target value
def set_target(key: str, value: float):
    global dirty
    targets[key] = float(value)

    # Initialize value if missing
    if key not in animated:
        animated[key] = 0.0

    dirty = True


# Get the current value for a given key
def get_value(key: str):
    return animated.get(key, 0.0)


# Return all values
def get_animated_values():
    return animated


# Consume and reset dirty flag
def consume_dirty():
    global dirty
    d = dirty
    dirty = False
    return d


# Anim Thread start
def start_animation_thread():
    def loop():
        global animated

        while True:
            # Only anim when new values
            if not consume_dirty():
                time.sleep(0.05)
                continue

            # Easing anim
            for step in range(15):
                for key, target in targets.items():
                    current = animated.get(key, 0.0)
                    diff = target - current
                    animated[key] = current + diff * 0.25
                time.sleep(0.03)

            for key, target in targets.items():
                animated[key] = target

    threading.Thread(target=loop, daemon=True).start()
