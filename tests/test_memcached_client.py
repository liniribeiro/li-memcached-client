import unittest
from unittest.mock import patch, AsyncMock

from li_memcache_ui.memcache_client import LiMemcacheClient


class TestLiMemcacheClient(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.memcached_stats = LiMemcacheClient()

    @patch('li_memcache_ui.memcache_client.asyncio.open_connection', new_callable=AsyncMock)
    async def test_command(self, mock_open_connection):
        mock_reader = AsyncMock()
        mock_writer = AsyncMock()
        mock_reader.readuntil.return_value = b'STAT key value\r\nEND\r\n'
        mock_open_connection.return_value = (mock_reader, mock_writer)

        response = await self.memcached_stats.command('stats')
        self.assertEqual(response, 'STAT key value\r\nEND\r\n')
        mock_writer.write.assert_called_with(b'stats\r\n')
        mock_writer.close.assert_called_once()
        await mock_writer.wait_closed()  # Ensure the writer is properly closed


    @patch('li_memcache_ui.memcache_client.LiMemcacheClient.command', new_callable=AsyncMock)
    async def test_key_details(self, mock_command):
        mock_command.side_effect = [
            'STAT items:1:number\r\nEND\r\n',
            'ITEM key1 [123 b; 456 s]\r\nEND\r\n'
        ]

        keys = await self.memcached_stats.key_details()
        self.assertEqual(keys, [('key1', '123 b', '456 s')])

    @patch('li_memcache_ui.memcache_client.LiMemcacheClient.command', new_callable=AsyncMock)
    async def test_keys(self, mock_command):
        mock_command.side_effect = [
            'STAT items:1:number\r\nEND\r\n',
            'ITEM key1 [123 b; 456 s]\r\nEND\r\n'
        ]

        keys = await self.memcached_stats.keys()
        self.assertEqual(keys, ['key1'])

    @patch('li_memcache_ui.memcache_client.LiMemcacheClient.command', new_callable=AsyncMock)
    async def test_slab_ids(self, mock_command):
        mock_command.return_value = 'STAT items:1:number\r\nEND\r\n'

        slab_ids = await self.memcached_stats.slab_ids()
        self.assertEqual(slab_ids, ['1'])

    @patch('li_memcache_ui.memcache_client.LiMemcacheClient.command', new_callable=AsyncMock)
    async def test_stats(self, mock_command):
        mock_command.return_value = 'STAT key value\r\nEND\r\n'

        stats = await self.memcached_stats.stats()
        self.assertEqual(stats, {'key': 'value'})

    @patch('li_memcache_ui.memcache_client.LiMemcacheClient.command', new_callable=AsyncMock)
    async def test_get_key_value(self, mock_command):
        mock_command.return_value = 'VALUE key 0 5\r\nvalue\r\nEND\r\n'

        value = await self.memcached_stats.get_key_value('key')
        self.assertEqual(value, 'value')

    @patch('li_memcache_ui.memcache_client.LiMemcacheClient.command', new_callable=AsyncMock)
    async def test_get_key_value_not_found(self, mock_command):
        mock_command.return_value = 'END\r\n'

        value = await self.memcached_stats.get_key_value('nonexistent_key')
        self.assertIsNone(value)


    @patch('li_memcache_ui.memcache_client.LiMemcacheClient.command', new_callable=AsyncMock)
    async def test_set_key_value(self, mock_command):
        mock_command.return_value = 'STORED\r\n'

        result = await self.memcached_stats.set_key_value('new_key', 'new_value')
        self.assertTrue(result)
        mock_command.assert_called_with('set new_key 0 0 9\r\nnew_value')

    @patch('li_memcache_ui.memcache_client.LiMemcacheClient.command', new_callable=AsyncMock)
    async def test_set_key_value_fail(self, mock_command):
        mock_command.return_value = 'NOT_STORED\r\n'

        result = await self.memcached_stats.set_key_value('new_key', 'new_value')
        self.assertFalse(result)
        mock_command.assert_called_with('set new_key 0 0 9\r\nnew_value')


if __name__ == '__main__':
    unittest.main()