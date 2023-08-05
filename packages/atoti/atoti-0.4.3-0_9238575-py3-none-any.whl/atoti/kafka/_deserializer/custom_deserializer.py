import json
from dataclasses import dataclass
from typing import Any, Callable, Mapping

from .kafka_deserializer import KafkaDeserializer


@dataclass(frozen=True)
class CustomDeserializer(KafkaDeserializer):
    """Class for python deserializer.

    Attributes:
        batch_size: Size of the batch of mesages. Should be tested with several values to find the most
            efficient. It enables to reduce the number of calls through py4J.
    """

    callback: Callable[[str], Mapping[str, Any]]
    batch_size: int

    def deserialize(self, data: str) -> str:
        """Deserialize json bytes in a string.

        Args:
            data: String that can be load in a json, keys are number ids, values are string containing kafka
                value's message part.
            datastore_columns: String like "[field_1, field_2, ...]" containing all the store fields.

        Returns:
            Stringified array of strings. {1:{field_1: ***, field_2: ***, ...}, 2: {***}, ...}
        """
        data_json = json.loads(data)

        try:
            result = {}
            for row_id, json_row in data_json.items():
                row = self.callback(json_row)
                result[row_id] = row
            return str(result)
        except KeyError as error:
            raise ValueError(
                "Error in custom deserializer : Missing field in datastore"
            ) from error

    def toString(self) -> str:  # pylint: disable=invalid-name
        """Get the name of the deserializer."""
        return self.name

    class Java:
        """Code needed for py4j callbacks."""

        implements = [
            "com.activeviam.chouket.loading.kafka.impl.serialization.IPythonDeserializer"
        ]
