from . import constants
from .accounts import accounts
from .categories import categories
from .wallets import wallets

data = {
    'accounts': accounts,
    'categories': categories,
    'wallets': wallets
}

__all__ = ['data', 'constants']
