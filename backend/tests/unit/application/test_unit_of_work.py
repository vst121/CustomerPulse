import pytest

from app.application.common.unit_of_work import UnitOfWork


class FakeUnitOfWork(UnitOfWork):

    def __init__(self):
        self.commit_count = 0
        self.rollback_count = 0

    async def commit(self) -> None:
        self.commit_count += 1

    async def rollback(self) -> None:
        self.rollback_count += 1


@pytest.mark.anyio
async def test_unit_of_work_rolls_back_on_exception():

    uow = FakeUnitOfWork()

    with pytest.raises(ValueError):

        async with uow:
            raise ValueError("Something went wrong")

    assert uow.rollback_count == 1


@pytest.mark.anyio
async def test_unit_of_work_does_not_rollback_when_successful():

    uow = FakeUnitOfWork()

    async with uow:
        pass

    assert uow.rollback_count == 0