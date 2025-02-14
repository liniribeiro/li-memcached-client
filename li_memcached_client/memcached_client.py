import re
import asyncio

class LiMemcachedClient:
    """
    A simple memcache client that can be used to interact with a memcache server.
    """
    def __init__(self, host='localhost', port=11211):
        self._host = host
        self._port = port
        self._key_regex = re.compile(r'ITEM (.*) \[(.*); (.*)\]')
        self._slab_regex = re.compile(r'STAT items:(.*):number')
        self._stat_regex = re.compile(r"STAT (.*) (.*)\r")

    async def command(self, cmd):
        reader, writer = await asyncio.open_connection(self._host, self._port)
        writer.write(f"{cmd}\r\n".encode('ascii'))
        await writer.drain()
        response = await reader.readuntil(b'END\r\n')
        writer.close()
        await writer.wait_closed()
        return response.decode('ascii')

    async def key_details(self, sort=True, limit=100):
        cmd = 'stats cachedump %s %s'
        keys = [key for id in await self.slab_ids()
                for key in self._key_regex.findall(await self.command(cmd % (id, limit)))]
        return sorted(keys) if sort else keys

    async def keys(self, sort=True, limit=100):
        return [key[0] for key in await self.key_details(sort=sort, limit=limit)]

    async def slab_ids(self):
        return self._slab_regex.findall(await self.command('stats items'))

    async def stats(self):
        return dict(self._stat_regex.findall(await self.command('stats')))

    async def get_key_value(self, key):
        response = await self.command(f'get {key}')
        lines = response.split('\r\n')
        if len(lines) > 1 and lines[0].startswith('VALUE'):
            return lines[1]
        return None

    async def set_key_value(self, key, value, exptime=0):
        response = await self.command(f'set {key} 0 {exptime} {len(value)}\r\n{value}')
        return response.startswith('STORED')

    async def delete_key(self, key):
        response = await self.command(f'delete {key}')
        return response.startswith('DELETED')

async def main():
    host = '127.0.0.1'
    port = 11211
    m = LiMemcachedClient(host, port)
    keys = await m.keys()
    print(keys)

    value = await m.get_key_value('enable_ml_sort_by_listicle_mode')
    print(value)


if __name__ == '__main__':
    asyncio.run(main())