from .constants import constants
from entities import Account

accounts = {
    str(constants['ALBO_ACCOUNT_ID']): Account('Albo Account', 'detail'),
    str(constants['BBVA_ACCOUNT_ID']): Account('BBVA Account', 'detail'),
    str(constants['CASH_ACCOUNT_ID']): Account('Cash Account', 'detail'),
    str(constants['HEY_ACCOUNT_ID']): Account('Hey Account', 'detail'),
    str(constants['NU_ACCOUNT_ID']): Account('Nu Account', 'detail'),
    str(constants['SPIN_ACCOUNT_ID']): Account('Spin Account', 'detail'),
    str(constants['STORI_ACCOUNT_ID']): Account('Stori Account', 'detail'),
    str(constants['DIDI_ACCOUNT_ID']): Account('Didi Account', 'detail')
}
