# -*- coding: utf-8 -*- 


class LogError(Exception):
    ''' log error
    '''
    def __init__(self, *args, **kwargs):
        super(LogError, self).__init__(*args, **kwargs)



class Unauthorized(Exception):
    ''' Unauthorized error
    '''
    def __init__(self, *args, **kwargs):
        super(Unauthorized, self).__init__(*args, **kwargs)


class AuthenticationError(ValueError):
    ''' AuthenticationError error
    '''
    def __init__(self, *args, **kwargs):
        super(AuthenticationError, self).__init__(*args, **kwargs)


class PasswordError(ValueError):
    ''' password error
    '''

    def __init__(self, *args, **kwargs):
        super(PasswordError, self).__init__(*args, **kwargs)
