"""An observable, settable value interface."""

import asyncio
import inspect
import sys

if sys.version_info.major == 3:
    from pyee import AsyncIOEventEmitter as EventEmitter
else:
    from pyee import BaseEventEmitter as EventEmitter


class Value(EventEmitter):
    """
    A property value.

    This is used for communicating between the Thing representation and the
    actual physical thing implementation.

    Notifies all observers when the underlying value changes through an
    external update (command to turn the light off) or if the underlying sensor
    reports a new value.
    """

    def __init__(self, initial_value=None, read_forwarder=None, write_forwarder=None):
        """
        Initialize the object.
        initial_value -- the initial value
        value_forwarder -- the method that updates the actual value on the
                           thing
        """
        EventEmitter.__init__(self)
        self._value = initial_value
        self.read_forwarder = read_forwarder
        self.write_forwarder = write_forwarder

    @property
    def readonly(self):
        return self.read_forwarder and not self.write_forwarder

    @property
    def writeonly(self):
        return self.write_forwarder and not self.read_forwarder

    async def set(self, value):
        """
        Set a new value for this thing.

        value -- value to set
        """
        if self.write_forwarder is not None:
            if inspect.iscoroutinefunction(self.write_forwarder):
                await self.write_forwarder(value)
            if asyncio.iscoroutine(self.write_forwarder):
                await self.write_forwarder
            else:
                self.write_forwarder(value)

        self.notify_of_external_update(value)
        return value

    async def get(self):
        """Return the last known value from the underlying thing."""
        if self.read_forwarder:
            if inspect.iscoroutinefunction(self.read_forwarder):
                self._value = await self.read_forwarder()
            elif asyncio.iscoroutine(self.read_forwarder):
                self._value = await self.read_forwarder
            else:
                self._value = self.read_forwarder()
        return self._value

    def notify_of_external_update(self, value):
        """
        Notify observers of a new value.

        value -- new value
        """
        if value is not None and value != self._value:
            self._value = value
            self.emit("update", value)
