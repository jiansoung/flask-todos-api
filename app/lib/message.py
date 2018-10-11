# -*- coding: utf-8 -*-

class Message:

    @staticmethod
    def not_found(record = 'record'):
        return "Sorry, {} not found.".format(record)
    
    invalid_credentials = 'Invalid credentials'
    
    invalid_token = 'Invalid token'
    
    missing_token = 'Missing token'
    
    unauthorized = 'Unauthorized request'
    
    account_created = 'Account created successfully'

    account_not_created = 'Account could not be created'

    expired_token = 'Sorry, your token has expired. Please login to continue.'
