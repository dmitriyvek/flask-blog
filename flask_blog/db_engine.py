from flask import abort, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from sqlalchemy.orm.exc import MultipleResultsFound


class CustomBaseQuery(BaseQuery):

    def get_object_or_404(self, **kwargs):
        '''
        Get object with given parameter from any model;
        if object does not exist then returns response with 404 status.
        '''
        try:
            self._mapper_zero().class_.__name__
        except Exception as e:
            raise e

        response = self.filter_by(**kwargs).all()
        try:
            if not response or response[0].is_deleted:
                error_message = {
                    'status': 'fail',
                    'message': 'Item not found',
                }
                abort(make_response(jsonify(error_message), 404))

        except AttributeError:
            print(
                'Warning: that supposed to be a "is_deleted" '
                'field on given model.'
            )

        if len(response) > 1:
            raise MultipleResultsFound(
                'Get more than one result with given search parameters.')

        return response[0]


db = SQLAlchemy(query_class=CustomBaseQuery)
