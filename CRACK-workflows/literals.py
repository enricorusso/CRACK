from sqlalchemy import Column, String, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

import enum
import json
import re

Base = declarative_base()

def removeNull(str):
    if str:
        if str.lower() == "null":
            return ""
        else:
            return str

def initParams(parameters, fact):
    paramvals = fact[fact.find("(") + 1:-1].replace("'", "").split(",")[1:]

    retval = {}
    for p in parameters:
        retval[p] = removeNull(paramvals[parameters.index(p)])

    return retval

class hasUser(Base):
    __tablename__ = 'hasuser'

    parameters = [ 'username', 'host', 'password', 'role' ]

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String)
    host = Column(String)
    password = Column(String)
    role = Column(String)

    @staticmethod
    def getNode(fact):
        params = initParams(hasUser.parameters, fact)

        return params['host']

    @staticmethod
    def fromDatalog(fact, ctx, session):
        params = initParams(hasUser.parameters, fact)

        ptr = [n for n in ctx.nodes if n.name == params['username']][0]

        # change username with real username in attribute/property
        params['username'] = removeNull(ptr.attributes['username'])
        if not params['username']:
            params['username'] = removeNull(ptr.properties['username'])

        # change password with real password in attribute/property
        params['password'] = removeNull(ptr.attributes['password'])
        if not params['password']:
            params['password'] = removeNull(ptr.properties['password'])

        return params

    @staticmethod
    def verifyResult(result):
        result = json.loads(result[result.keys()[0]])
        return result['username'] and result['role']

    @staticmethod
    def saveResult(result, session):
        result = json.loads(result[result.keys()[0]])

        h = hasUser(username=result['username'], host=result['host'], password=result['password'], role=result['role'])
        session.add(h)

class hasAccount(Base):
    __tablename__ = 'hasaccount'

    parameters = [ 'principal', 'host', 'username' ]
    extra_parameters = [ 'knowledge' ]

    id = Column(Integer, primary_key=True, autoincrement=True)
    principal = Column(String)
    username = Column(String)
    host = Column(String)

    @staticmethod
    def getNode(fact):
        params = initParams(hasAccount.parameters, fact)

        return params['host']

    @staticmethod
    def fromDatalog(fact, ctx, session):
        params = initParams(hasAccount.parameters, fact)

        ptr = [n for n in ctx.nodes if n.name == params['username']][0]

        # change username with real username in attribute/property
        params['username'] = ptr.attributes['username']
        if not params['username']:
            params['username'] = ptr.properties['username']

        filter = knows.principal == params['principal']
        knowledge = []
        for k in session.query(knows.data).filter(filter).distinct():
            knowledge.append(k.data)

        params['extra'] = { 'knowledge': knowledge }

        return params

    @staticmethod
    def verifyResult(result):
        result = json.loads(result[result.keys()[0]])
        return result['username']

    @staticmethod
    def saveResult(result, session):
        result = json.loads(result[result.keys()[0]])

        h = hasAccount(principal=result['principal'], username=result['username'], host=result['host'])
        session.add(h)

class listeningOn(Base):
    __tablename__ = 'listeningon'

    parameters = [ 'host', 'protocol', 'port' ]

    id = Column(Integer, primary_key=True, autoincrement=True)
    host = Column(String)
    protocol = Column(String)
    port = Column(Integer)

    @staticmethod
    def getNode(fact):
        params = initParams(listeningOn.parameters, fact)

        return params['host']

    @staticmethod
    def fromDatalog(fact, ctx, session):
        params = initParams(listeningOn.parameters, fact)

        return params

    @staticmethod
    def verifyResult(result):
        result = json.loads(result[result.keys()[0]])
        return result['protocol'] and result['port']

    @staticmethod
    def saveResult(result, session):
        result = json.loads(result[result.keys()[0]])

        l = listeningOn(host=result['host'], protocol=result['protocol'], port=result['port'])
        session.add(l)

class hostACL(Base):
    __tablename__ = 'hostacl'

    parameters = [ 'srchost', 'dsthost', 'protocol', 'port' ]

    id = Column(Integer, primary_key=True, autoincrement=True)
    srchost = Column(String)
    dsthost = Column(String)
    protocol = Column(String)
    port = Column(String)

    @staticmethod
    def getNode(fact):
        params = initParams(hostACL.parameters, fact)

        return params['srchost']

    @staticmethod
    def fromDatalog(fact, ctx, session):
        params = initParams(hostACL.parameters, fact)

        filter = isConnected.host == params['dsthost']
        ips = []
        for ip in session.query(isConnected.address).filter(filter).distinct():
            ips.append(ip.address)

        params['dsthost'] = ips

        return params

    @staticmethod
    def verifyResult(result):
        result = json.loads(result[result.keys()[0]])
        return result['dsthost']

    @staticmethod
    def saveResult(result, session):
        result = json.loads(result[result.keys()[0]])

        for ip in result['dsthost']:
            c = hostACL(srchost=result['srchost'],dsthost=ip,
                        protocol=result['protocol'],port=result['port'])
            session.add(c)

class isConnected(Base):
    __tablename__ = 'isconnected'

    parameters = [ 'host', 'address' ]

    id = Column(Integer, primary_key=True, autoincrement=True)
    host = Column(String)
    address = Column(String)

    @staticmethod
    def getNode(fact):
        params = initParams(isConnected.parameters, fact)

        return params['host']

    @staticmethod
    def fromDatalog(fact, ctx, session):
        params = initParams(isConnected.parameters, fact)

        ptr = [n for n in ctx.nodes if n.name == params['address']][0]

        params['address'] = ptr.properties['subnet']['cidr']

        return params

    @staticmethod
    def verifyResult(result):
        result = json.loads(result[result.keys()[0]])
        return result['address']

    @staticmethod
    def saveResult(result, session):
        result = json.loads(result[result.keys()[0]])

        for ip in result['address']:
            c = isConnected(host=result['host'], address=ip)
            session.add(c)

class knows(Base):
    __tablename__ = 'knows'

    parameters = [ 'principal', 'data' ]
    extra_parameters = ['knowledge']

    id = Column(Integer, primary_key=True, autoincrement=True)
    principal = Column(String)
    data = Column(String)

    @staticmethod
    def getNode(fact):
        return False

    @staticmethod
    def fromDatalog(fact, ctx, session):
        params = initParams(knows.parameters, fact)

        filter = knows.principal == params['principal']
        knowledge = []
        for k in session.query(knows.data).filter(filter).distinct():
            knowledge.append(k.data)

        params['extra'] = { 'knowledge': knowledge }

        return params

    @staticmethod
    def verifyResult(result):
        result = json.loads(result[result.keys()[0]])
        return result['data']

    @staticmethod
    def saveResult(result, session):
        result = json.loads(result[result.keys()[0]])

        for d in result['data']:
            k = knows(principal=result['principal'], data=d)
            session.add(k)

class existsRoute(Base):
    __tablename__ = 'existsroute'

    parameters = [ 'srcnet', 'dstnet', 'host' ]

    id = Column(Integer, primary_key=True, autoincrement=True)
    srcnet = Column(String)
    dstnet = Column(String)
    host = Column(String)

    @staticmethod
    def getNode(fact):
        params = initParams(existsRoute.parameters, fact)

        return params['host']

    @staticmethod
    def fromDatalog(fact, ctx, session):
        params = initParams(existsRoute.parameters, fact)

        ptr = [n for n in ctx.nodes if n.name == params['srcnet']][0]
        params['srcnet'] = ptr.properties['subnet']['cidr']

        ptr = [n for n in ctx.nodes if n.name == params['dstnet']][0]
        params['dstnet'] = ptr.properties['subnet']['cidr']

        return params

    @staticmethod
    def verifyResult(result):
        result = json.loads(result[result.keys()[0]])
        return result['dstnet']

    @staticmethod
    def saveResult(result, session):
        result = json.loads(result[result.keys()[0]])

        r = existsRoute(srcnet=result['srcnet'], dstnet=result['dstnet'], host=result['host'])
        session.add(r)

class isRouter(Base):
    __tablename__ = 'isrouter'

    parameters = [ 'host' ]

    id = Column(Integer, primary_key=True, autoincrement=True)
    host = Column(String)

    @staticmethod
    def getNode(fact):
        params = initParams(isRouter.parameters, fact)

        return params['host']

    @staticmethod
    def fromDatalog(fact, ctx, session):
        params = initParams(isRouter.parameters, fact)

        return params

    @staticmethod
    def verifyResult(result):
        result = json.loads(result[result.keys()[0]])
        return result['host']

    @staticmethod
    def saveResult(result, session):
        result = json.loads(result[result.keys()[0]])

        i = isRouter(host=result['host'])
        session.add(i)
