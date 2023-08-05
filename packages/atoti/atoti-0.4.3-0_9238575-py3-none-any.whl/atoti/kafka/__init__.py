from typing import Any, Callable, Mapping

from ._deserializer.custom_deserializer import CustomDeserializer
from ._deserializer.kafka_deserializer import KafkaDeserializer


def create_deserializer(
    callback: Callable[[str], Mapping[str, Any]], *, batch_size: int = 1
) -> KafkaDeserializer:
    """Return a custom Kafka deserializer.

    Example:
        Considering Kafka records shaped like this: "{'c_1': v_1, 'c_2': v_2, 'c_3': v_3}" and a store with colums
        c_1, c_2 and c_3, a callback like this would work::

            columns = store.columns
            def callback(record: str):
                values = json.loads(record)
                fact = {}
                for column in columns:
                    fact[column] = values[column]
                return fact

        Considering Kafka records shaped like this: "v_1, v_2, v_3" and a store with colums
        c_1, c_2 and c_3, a callback like this would work::

            columns = store.columns
            def callback(record: str):
                values = record.split(", ")
                fact = {}
                for index, column in enumerate(columns):
                    fact[column] = values[index]
                return fact

    Args:
        callback: Function taking the record as a string and returning a mapping from a store column name to its value.
        batch_size: Size of the batch of records.

            If ``batch_size > 1`` the records will be batched then deserialized when either the batch size is reached
            or the `batch_duration` passed in :meth:`store.Store.load_kafka` has ellapsed.
            A bigger batch size means a higher latency but less store transactions so often better performance.
    """
    return CustomDeserializer("PythonDeserializer", callback, batch_size)


JSON_DESERIALIZER = KafkaDeserializer(
    "com.activeviam.chouket.loading.kafka.impl.serialization.JsonDeserializer"
)
"""Core JSON deserializer.
Each json correspond to a row of the store, keys of the json must match fields of the store.
"""
