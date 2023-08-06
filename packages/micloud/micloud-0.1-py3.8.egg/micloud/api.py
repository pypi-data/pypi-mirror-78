import falcon
import config

class AuthMiddleware(object):

    def process_request(self, req, resp):
        token = req.get_header('Authorization')
        account_id = req.get_header('Account-ID')

        challenges = ['Token type="Fernet"']

        if token is None:
            description = ('Please provide an auth token '
                           'as part of the request.')

            raise falcon.HTTPUnauthorized(title='Auth token required',
                                          description=description,
                                          challenges=challenges)

        if not self._token_is_valid(token):
            description = ('The provided auth token is not valid. '
                           'Please request a new token and try again.')

            raise falcon.HTTPUnauthorized(title='Authentication required',
                                          description=description,
                                          challenges=challenges)

    def _token_is_valid(self, token):
        return token == config.TOKEN


def json_serializer(req, resp, exception):
    representation = exception.to_json()
    resp.body = representation
    resp.content_type = 'application/json'
    resp.append_header('Vary', 'Accept')