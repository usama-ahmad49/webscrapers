import pymongo

def Mongoconexion(database):
        MONGODB_HOST = '104.225.140.236'
        MONGODB_PORT = '27017'
        MONGODB_TIMEOUT = 1000
        MONGODB_SOCKETTIMEOUT = 3000
        MONGODB_DATABASE = database
        MONGODB_USER = 'Pad31'
        MONGODB_PASS = 'BCsm13wbSbgKIrpd'
        URI_CONNECTION = 'mongodb://' + MONGODB_USER + ':' + MONGODB_PASS + '@' + MONGODB_HOST + ':' + MONGODB_PORT + '/Crudo'

        client = pymongo.MongoClient(URI_CONNECTION, connectTimeoutMS=MONGODB_TIMEOUT,socketTimeoutMS=MONGODB_SOCKETTIMEOUT)

        return client, MONGODB_DATABASE
