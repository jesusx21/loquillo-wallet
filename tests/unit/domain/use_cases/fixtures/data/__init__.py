from . import constants
from .accounts import accounts
from .wallets import wallets

data = {
    'accounts': accounts,
    'wallets': wallets
}

__all__ = ['data', 'constants']
