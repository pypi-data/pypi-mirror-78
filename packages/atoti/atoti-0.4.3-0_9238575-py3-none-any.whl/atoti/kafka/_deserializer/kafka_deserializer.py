from dataclasses import dataclass


@dataclass(frozen=True)
class KafkaDeserializer:
    """Kafka Deserializer.

    Attributes:
        name: Name of the deserializer.

    """

    name: str
