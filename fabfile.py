from fabric.api import local


def grakn_clean():
    '''Clean Grakn database'''
    local('grakn server clean')


def grakn_stop():
    local('grakn server stop')


def grakn_start():
    local('grakn server start')


def grakn_factory_reset():
    '''Clean and restart Grakn'''
    grakn_stop()
    grakn_clean()
    grakn_start()


def dev():
    '''Start gunicorn and watch for changes'''
    local('gunicorn --reload api:api')
