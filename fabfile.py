from fabric.api import local


def dev():
    '''Start gunicorn and watch for changes'''
    local('gunicorn --reload api:api')