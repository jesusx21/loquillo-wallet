from . import constants

from database.tables import Categories
from domain.entities.category import CategoryType

category_fixtures = {
    'table': Categories,
    'data': [
        {
            'id': constants.SALARY_CATEGORY_ID,
            'name': 'Salario',
            'type': CategoryType.INCOME.value,
            'account_id': constants.ALBO_ACCOUNT_ID,
            'user_id': constants.USER_ID,
            'parent_category_id': None,
        },
        {
            'id': constants.RENT_CATEGORY_ID,
            'name': 'Alquiler',
            'type': CategoryType.EXPENSE.value,
            'account_id': constants.BBVA_ACCOUNT_ID,
            'user_id': constants.USER_ID,
            'parent_category_id': None,
        },
        {
            'id': constants.LOAN_CATEGORY_ID,
            'name': 'Préstamo',
            'type': CategoryType.LOAN.value,
            'account_id': constants.NU_BANK_ACCOUNT_ID,
            'user_id': constants.SECOND_USER_ID,
            'parent_category_id': None,
        },
        {
            'id': constants.DEBT_CATEGORY_ID,
            'name': 'Deuda',
            'type': CategoryType.DEBT.value,
            'account_id': constants.STORI_ACCOUNT_ID,
            'user_id': constants.SECOND_USER_ID,
            'parent_category_id': None,
        }
    ]
}
