import random

import pytest
import pytest_asyncio
from starkware.starknet.testing.starknet import Starknet


@pytest_asyncio.fixture(scope="module")
async def datacopy(starknet: Starknet):
    class_hash = await starknet.deprecated_declare(
        source="./tests/src/kakarot/precompiles/test_datacopy.cairo",
        cairo_path=["src"],
        disable_hint_validation=True,
    )
    return await starknet.deploy(class_hash=class_hash.class_hash)


@pytest.mark.asyncio
class TestDataCopy:
    @pytest.mark.parametrize("calldata_len", [32])
    async def test_datacopy(self, datacopy, calldata_len):
        random.seed(0)
        calldata = [random.randint(0, 255) for _ in range(calldata_len)]

        await datacopy.test__datacopy_impl(calldata=calldata).call()
