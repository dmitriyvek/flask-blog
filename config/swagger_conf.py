import os


SWAGGER_HOST_NAME = os.getenv('SWAGGER_HOST_NAME')

template = {
    'swagger': '2.0',
    'info': {
        'title': 'Myblog API',
        'description': 'API for my flask blog applicaion',
        'contact': {
            'name': 'Dmitriy Veksharev',
            'email': 'dmitriyvek@mail.ru'
        },
        'version': '0.0.1'
    },
    'host': SWAGGER_HOST_NAME,
    'basePath': '/',
    'schemes': [
        # 'http',
        'https'
    ],
    'components': {
        'examples': {},
        'schemas': {
            'serverFail': {
                'type': 'object',
                'properties': {
                    'status': {
                        'type': 'string',
                        'enum': ['fail']
                    }
                }
            },
            'clientFail': {
                'type': 'object',
                'properties': {
                    'status': {
                        'type': 'string',
                        'enum': ['fail']
                    },
                    'message': {
                        'type': 'string',
                        'description': \
                        'Expanded message about result of account confirmation'
                    }
                },
                'required': [
                    'status',
                    'message'
                ]
            },
            'defaultResponse': {
                'required': ['status', 'message'],
                'type': 'object',
                'properties': {
                    'status': {
                        'enum': ['success'],
                        'type': 'string'
                    },
                    'message': {
                        'type': 'string'
                    }
                }
            },
            'defaultResponseWithToken': {
                'required': ['status', 'message', 'token'],
                'type': 'object',
                'properties': {
                    'status': {
                        'enum': ['success'],
                        'type': 'string'
                    },
                    'message': {
                        'type': 'string'
                    },
                    'token': {
                        'type': 'string',
                        'description': 'Auth jwt token'

                    }
                }
            },
            'postInList': {
                'type': 'object',
                'properties': {
                    'author': {
                        'type': 'string'
                    },
                    'created_on': {
                        'type': 'string'
                    },
                    'id': {
                        'type': 'integer',
                        'minimum': '1'
                    },
                    'title': {
                        'type': 'string'
                    }
                },
                'required': ['author', 'created_on', 'id', 'title'],
            },
            'postDetail': {
                'type': 'object',
                'properties': {
                    'status': {
                        'enum': ['success'],
                        'type': 'string'
                    },
                    'post': {
                        'type': 'object',
                        'properties': {
                            'content': {
                                'type': 'string'
                            },
                            'created_on': {
                                'type': 'string'
                            },
                            'title': {
                                'type': 'string'
                            },
                            'updated_on': {
                                'type': 'string'
                            },
                            'author_id': {
                                'minimum': 1,
                                'type': 'integer'
                            },
                            'id': {
                                'minimum': 1,
                                'type': 'integer'
                            }
                        }
                    }
                }
            }
        },
        'parameters': {
            'authToken': {
                'required': True,
                'in': 'header',
                'description': 'String in format: Bearer AuthToken',
                'name': 'Authorization',
                'schema': {
                    'type': 'string',
                    'format': 'jwt'
                }
            },
            'postId': {
                'required': True,
                'in': 'path',
                'description': 'The target post id',
                'name': 'post_id',
                'schema': {
                    'minimum': 1,
                    'type': 'integer'
                }
            }
        },
        'securitySchemes': {
            'bearerAuth': {
                'type': 'http',
                'scheme': 'bearer',
                'bearerFormat': 'JWT'
            }
        }
    }
}
