from typing import Generator
from unittest import mock
from unittest.mock import MagicMock

import pytest
from elasticsearch import Elasticsearch
from elasticsearch._sync.client import IndicesClient
from langchain_community.chat_models.fake import FakeMessagesListChatModel
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage

from langchain_elasticsearch import ElasticsearchCache, ElasticsearchEmbeddingsCache


@pytest.fixture
def es_client_fx() -> Generator[MagicMock, None, None]:
    client_mock = MagicMock(spec=Elasticsearch)
    client_mock.indices = MagicMock(spec=IndicesClient)
    yield client_mock()


@pytest.fixture
def es_embeddings_cache_fx(
    es_client_fx: MagicMock,
) -> Generator[ElasticsearchEmbeddingsCache, None, None]:
    with mock.patch(
        "langchain_elasticsearch.cache.create_elasticsearch_client",
        return_value=es_client_fx,
    ):
        cache = ElasticsearchEmbeddingsCache(
            es_url="http://localhost:9200",
            index_name="test_index",
            store_input=True,
            namespace="test",
            metadata={"project": "test_project"},
        )
        yield cache


@pytest.fixture
def es_cache_fx(es_client_fx: MagicMock) -> Generator[ElasticsearchCache, None, None]:
    with mock.patch(
        "langchain_elasticsearch.cache.create_elasticsearch_client",
        return_value=es_client_fx,
    ):
        cache = ElasticsearchCache(
            es_url="http://localhost:30096",
            index_name="test_index",
            store_input=True,
            store_input_params=True,
            metadata={"project": "test_project"},
        )
        yield cache


@pytest.fixture
def fake_chat_fx() -> Generator[BaseChatModel, None, None]:
    yield FakeMessagesListChatModel(
        cache=True, responses=[AIMessage(content="test output")]
    )
