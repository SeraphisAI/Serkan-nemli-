"""Protocol adapters scaffold (REST active, WS/MQTT stubs)."""


class WebSocketAdapter:
    def publish(self, topic: str, message: dict) -> None:
        return None


class MQTTAdapter:
    def publish(self, topic: str, message: dict) -> None:
        return None
