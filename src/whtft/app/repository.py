import typing


class ModelProtocol(typing.Protocol):

    def __init__(self, **kwargs: typing.Any): ...

    def model_dump(self) -> dict[str, typing.Any]: ...


class IdentifiedProtocol(ModelProtocol):
    id: typing.Any


class MockRepository[
    Model: ModelProtocol, IdentifiedModel: IdentifiedProtocol
]:
    factory: type[IdentifiedModel]

    @property
    def _items(self) -> list[IdentifiedModel]: ...

    async def add(self, item: Model):
        added = self.factory(id=len(self._items), **item.model_dump())
        self._items.append(added)
        return added.model_dump()

    async def get(self, id):
        for item in self._items:
            if item.id == id:
                return item.model_dump()

    async def delete(self, id):
        for item in self._items:
            if item.id == id:
                self._items.remove(item)
                return True
        return False

    async def list(self):
        return [item.model_dump() for item in self._items]
