from __future__ import annotations

from typing import TYPE_CHECKING, Mapping

from ..kafka import CustomDeserializer, KafkaDeserializer
from . import DataSource

if TYPE_CHECKING:
    from .._java_api import JavaApi
    from ..store import Store


class KafkaDataSource(DataSource):
    """Kafka data source."""

    def __init__(self, java_api: JavaApi):
        """Init."""
        super().__init__(java_api, "KAFKA")

    def load_kafka_into_store(
        self,
        store: Store,
        bootstrap_servers: str,
        topic: str,
        group_id: str,
        value_deserializer: KafkaDeserializer,
        batch_duration: int,
        consumer_config: Mapping[str, str],
    ):
        """Consume a kafka topic and load it in an existing store.

        Args:
            store: The store to load kafka records into
            bootstrap_servers: ‘host[:port]’ that the consumer should contact to bootstrap
                initial cluster metadata.
            topic: List of topics to subscribe to.
            group_id: The name of the consumer group to join.
            value_deserializer: Deserializer for kafka records' value.
            batch_duration: Milliseconds waiting between batch creation.
            consumer_config: Mapping containing optional params to set up
                the KafkaConsumer. List of available parameters can be found
                `here <https://kafka.apache.org/10/javadoc/index.html
                ?org/apache/kafka/clients/consumer/ConsumerConfig.html>`_.

        """
        params = {
            "bootstrapServers": bootstrap_servers,
            "topic": topic,
            "consumerGroupId": group_id,
            "keyDeserializerClass": "org.apache.kafka.common.serialization.StringDeserializer",
            "batchDuration": batch_duration,
            "additionalParameters": consumer_config,
        }
        if isinstance(value_deserializer, CustomDeserializer):
            params["pythonValueDeserializer"] = value_deserializer
            params["batchSize"] = value_deserializer.batch_size
        else:
            params["valueDeserializerClass"] = value_deserializer.name
        self.load_data_into_store(store.name, None, False, True, False, params)
