from threading import Lock
from typing import Iterable, Protocol


class Collector(Protocol):
    name: str

    def collect(self) -> Iterable:
        pass


class Registry(Protocol):
    def register(self, collector: Collector):
        pass

    def unregister(self, collector: Collector):
        pass

    def collect(self) -> Iterable:
        pass


class CollectorRegistry:
    def __init__(self, prefix: str = None) -> None:
        self._lock = Lock()
        self._prefix = prefix
        self._collectors: dict[str, Collector] = {}

    def register(self, collector: Collector) -> None:
        with self._lock:
            if collector.name in self._collectors:
                return
            self._collectors[collector.name] = collector

    def unregister(self, collector: Collector) -> None:
        with self._lock:
            if collector.name not in self._collectors:
                return
            del self._collectors[collector.name]

    def collect(self) -> Iterable:
        for collector in self._collectors.values():
            yield from collector.collect()


class CollectorRegistryProxy:
    def __init__(self, registry: Registry = None) -> None:
        self._registry = registry or CollectorRegistry()

    def set_registry(self, registry: Registry) -> None:
        self._registry = registry

    def register(self, collector: Collector) -> None:
        self._registry.register(collector)

    def unregister(self, collector: Collector) -> None:
        self._registry.unregister(collector)

    def collect(self) -> Iterable:
        return self._registry.collect()


REGISTRY_PROXY = CollectorRegistryProxy()
