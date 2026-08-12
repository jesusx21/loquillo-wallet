from uuid import uuid4, UUID
from typing import Final

constants: Final[dict[str, UUID]] = {
    'ALBO_ACCOUNT_ID': uuid4(),
    'BBVA_ACCOUNT_ID': uuid4(),
    'CASH_ACCOUNT_ID': uuid4(),
    'HEY_ACCOUNT_ID': uuid4(),
    'NU_ACCOUNT_ID': uuid4(),
    'SPIN_ACCOUNT_ID': uuid4(),
    'STORI_ACCOUNT_ID': uuid4(),
    'DIDI_ACCOUNT_ID': uuid4()
}
