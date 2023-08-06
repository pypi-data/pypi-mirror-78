import array

import serial


def async_serial_class(klass):
    """Class decorator forcing async read/write methods"""

    class Serial(klass):
        def __init__(self, *args, eol=serial.LF, **kwargs):
            self._eol = eol
            super().__init__(*args, **kwargs)

        async def readinto(self, b):
            data = await self.read(len(b))
            n = len(data)
            try:
                b[:n] = data
            except TypeError as err:
                import array

                if not isinstance(b, array.array):
                    raise err
                b[:n] = array.array("b", data)
            return n

        async def read_all(self):
            return await self.read(self.in_waiting)

        async def read_until(self, separator=serial.LF, size=None):
            """\
            Read until an expected sequence is found ('\n' by default) or the size
            is exceeded.
            """
            lenterm = len(separator)
            line = bytearray()
            timeout = serial.Timeout(self._timeout)
            while True:
                c = await self.read(1)
                if c:
                    line += c
                    if line[-lenterm:] == separator:
                        break
                    if size is not None and len(line) >= size:
                        break
                else:
                    break
                if timeout.expired():
                    break
            return bytes(line)

        async def writelines(self, lines):
            return await self.write(b"".join(lines))

        async def readline(self, eol=None):
            if eol is None:
                eol = self._eol
            return await self.read_until(separator=eol)

        async def readlines(self, n, eol=None):
            if eol is None:
                eol = self._eol
            return [await self.readline(eol=eol) for _ in range(n)]

        async def write_readline(self, data, eol=None):
            await self.write(data)
            return await self.readline(eol=eol)

        async def write_readlines(self, data, n, eol=None):
            await self.write(data)
            return await self.readlines(n, eol=eol)

        async def writelines_readlines(self, lines, n=None, eol=None):
            if n is None:
                n = len(lines)
            await self.writelines(lines)
            return await self.readlines(n, eol=eol)

        async def send_break(self, duration=0.25):
            """\
            Send break condition. Timed, returns to idle state after given
            duration.
            """
            if not self.is_open:
                raise portNotOpenError
            self.break_condition = True
            await asyncio.sleep(duration)
            self.break_condition = False

    return Serial
