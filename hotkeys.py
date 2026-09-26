"""Cross-platform hotkey handling for botyaradash."""

import sys
import threading
import queue
import time
from typing import Callable, Optional

IS_WINDOWS = sys.platform == "win32"

if IS_WINDOWS:
    import msvcrt
else:
    import termios
    import tty
    import select


class KeyReader:
    """Background thread that reads keys and puts them in a queue."""

    def __init__(self) -> None:
        self._queue: queue.Queue[str] = queue.Queue()
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._old_settings = None

    def start(self) -> None:
        """Start reading keys in background."""
        if self._running:
            return
        self._running = True

        if not IS_WINDOWS:
            try:
                fd = sys.stdin.fileno()
                self._old_settings = termios.tcgetattr(fd)
                tty.setcbreak(fd)
            except (termios.error, ValueError, OSError):
                # Not a TTY (e.g., piped input)
                self._old_settings = None

        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        """Stop reading and restore terminal."""
        self._running = False

        if not IS_WINDOWS and self._old_settings is not None:
            try:
                fd = sys.stdin.fileno()
                termios.tcsetattr(fd, termios.TCSADRAIN, self._old_settings)
            except Exception:
                pass

        if self._thread:
            self._thread.join(timeout=0.5)

    def _loop(self) -> None:
        """Background loop reading keys."""
        while self._running:
            key = self._read_key_blocking()
            if key:
                self._queue.put(key)

    def _read_key_blocking(self) -> Optional[str]:
        """Read a single key, blocking briefly."""
        try:
            if IS_WINDOWS:
                return self._read_key_windows()
            return self._read_key_unix()
        except Exception:
            return None

    def _read_key_windows(self) -> Optional[str]:
        """Read key on Windows."""
        # Poll with short sleep to avoid busy-wait
        for _ in range(10):
            if not self._running:
                return None
            if msvcrt.kbhit():
                ch = msvcrt.getwch()
                # Handle arrow keys / function keys (prefix)
                if ch in ("\x00", "\xe0"):
                    ch2 = msvcrt.getwch()
                    return self._decode_windows_special(ch2)
                return ch
            time.sleep(0.02)
        return None

    def _decode_windows_special(self, ch: str) -> str:
        """Decode arrow keys on Windows."""
        mapping = {
            "H": "UP",
            "P": "DOWN",
            "K": "LEFT",
            "M": "RIGHT",
        }
        return mapping.get(ch, "")

    def _read_key_unix(self) -> Optional[str]:
        """Read key on Unix."""
        try:
            rlist, _, _ = select.select([sys.stdin], [], [], 0.2)
        except (ValueError, OSError):
            return None

        if not rlist:
            return None

        try:
            ch = sys.stdin.read(1)
        except Exception:
            return None

        if not ch:
            return None

        # Handle escape sequences (arrow keys)
        if ch == "\x1b":
            # Try to read more
            try:
                rlist, _, _ = select.select([sys.stdin], [], [], 0.05)
                if rlist:
                    seq = sys.stdin.read(2)
                    return self._decode_unix_escape(seq)
            except Exception:
                pass
            return "ESC"

        return ch

    def _decode_unix_escape(self, seq: str) -> str:
        """Decode escape sequences on Unix."""
        mapping = {
            "[A": "UP",
            "[B": "DOWN",
            "[C": "RIGHT",
            "[D": "LEFT",
        }
        return mapping.get(seq, "")

    def get_key(self) -> Optional[str]:
        """Get a key from the queue (non-blocking)."""
        try:
            return self._queue.get_nowait()
        except queue.Empty:
            return None

    def drain(self) -> list[str]:
        """Get all queued keys."""
        keys = []
        while True:
            k = self.get_key()
            if k is None:
                break
            keys.append(k)
        return keys


class HotkeyManager:
    """Manages hotkey bindings using KeyReader."""

    def __init__(self) -> None:
        self._bindings: dict[str, Callable] = {}
        self._reader = KeyReader()

    def bind(self, key: str, callback: Callable) -> None:
        """Bind a key to a callback."""
        self._bindings[key] = callback

    def unbind(self, key: str) -> None:
        """Remove a key binding."""
        self._bindings.pop(key, None)

    def start(self) -> None:
        """Start listening for keys."""
        self._reader.start()

    def stop(self) -> None:
        """Stop listening."""
        self._reader.stop()

    def process_pending(self) -> list[str]:
        """Process all pending key presses. Returns handled keys."""
        handled = []
        for key in self._reader.drain():
            if key in self._bindings:
                try:
                    self._bindings[key]()
                    handled.append(key)
                except Exception:
                    pass
        return handled
