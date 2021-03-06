#!/usr/bin/env python

from basic_store import BasicStore, TTLStore
from conftest import ExtendedKeyspaceTests
from simplekv.contrib import ExtendedKeyspaceMixin

import pytest
redis = pytest.importorskip('redis')

from redis import StrictRedis
from redis.exceptions import ConnectionError


class TestRedisStore(TTLStore, BasicStore):
    @pytest.yield_fixture()
    def store(self):
        from simplekv.memory.redisstore import RedisStore
        r = StrictRedis()

        try:
            r.get('anything')
        except ConnectionError:
            pytest.skip('Could not connect to redis server')

        r.flushdb()
        yield RedisStore(r)
        r.flushdb()


class TestExtendedKeyspaceDictStore(TestRedisStore, ExtendedKeyspaceTests):
    @pytest.fixture
    def store(self):
        from simplekv.memory.redisstore import RedisStore

        class ExtendedKeyspaceStore(ExtendedKeyspaceMixin, RedisStore):
            pass
        r = StrictRedis()

        try:
            r.get('anything')
        except ConnectionError:
            pytest.skip('Could not connect to redis server')

        r.flushdb()
        yield ExtendedKeyspaceStore(r)
        r.flushdb()
