from . import constants

from database.tables import Users

user_fixtures = {
    'table': Users,
    'data': [
        {
            'id': constants.USER_ID,
            'names': 'Jon',
            'last_names': 'Doe',
            'email': 'jon.doe@example.com',
        },
        {
            'id': constants.SECOND_USER_ID,
            'names': 'Jane',
            'last_names': 'Doe',
            'email': 'jane.doe@example.com',
        },
        {
            'id': constants.THIRD_USER_ID,
            'names': 'Jim',
            'last_names': 'Beam',
            'email': 'jim@gmail.com'
        }
    ]
}
