import json

from flask import Response, jsonify, abort
from flask_sqlalchemy import SQLAlchemy, BaseQuery


class CustomBaseQuery(BaseQuery):

    def get_object_or_404(self, **kwargs):
        '''Get object with given parameter from any model; if object does not exist then returns response with 404 status'''
        model_class_name = ''
        try:
            model_class_name = self._mapper_zero().class_.__name__
        except Exception as e:
            raise e

        response = self.filter_by(**kwargs).first()
        if not response:
            error_message = json.dumps({
                'status': 'fail',
                'message': 'Item not found',
            })
            abort(Response(error_message, 404))

        return response


db = SQLAlchemy(query_class=CustomBaseQuery)
