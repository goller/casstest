#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Cassandra Stress Test

Usage:
  stresstest [--username=<name>] [--passwd=<passwd>] [--port=<number>] [--keyspace=<name>] [--keys=<num>] [--size=<bytes>] [--ttl=<secs>] [--replication=<num>] [--timeout=<secs>] <servers>...
  stresstest -h | --help
  stresstest -v | --version

Options:
  -h --help            Show this screen.
  -v --version         Show version.
  <servers>            Cassandra Server IP addresses
  --username=<name>    Username for authentication [default: None]
  --passwd=<passwd>    Password for authentication [default: None]
  --port=<number>      Cassandra port [default: 9042]
  --keyspace=<name>    Keyspace name [default: test]
  --keys=<num>         Number of keys to insert into keyspace [default: 100]
  --size=<bytes>       Size in bytes of value [default: 1024]
  --ttl=<secs>         Time to live for keys in seconds [default: never]
  --replication=<num>  Replication Factor number [default: 2]
  --timeout=<secs>     Timeout seconds for queries before failure [default: 10.0]
"""
from docopt import docopt
import sys

from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
from cassandra.io.libevreactor import LibevConnection
from cassandra.protocol import ConfigurationException


class Connection(object):
    def __init__(self, servers, port, username, passwd, keyspace, replication, timeout):
        connect_kwargs = {}
        if username and passwd:
            auth = PlainTextAuthProvider(username=username, password=passwd)
            connect_kwargs['auth_provider'] = auth
        self.cluster = Cluster(servers, port=port, **connect_kwargs)
        self.cluster.connection_class = LibevConnection
        self.session = self.cluster.connect()
        self.timeout = timeout
        self.create_keyspace(keyspace, replication)
        self.create_table()

    def create_keyspace(self, keyspace, replication):
        query = "CREATE KEYSPACE %s WITH replication = {'class':'SimpleStrategy', 'replication_factor': %s};" % (keyspace, replication)
        self.session.execute(query, timeout=self.timeout)
        self.session.set_keyspace(keyspace)

    def create_table(self, ):
        self.session.execute("""CREATE TABLE stresstest (
                                id int PRIMARY KEY,
                                value blob
                                );""",
                                timeout=self.timeout)

    def insert(self, key, value, ttl=None):
        create_query = """INSERT INTO stresstest (id, value)
                          VALUES (%s, %s)
                       """
        if ttl is not None:
            create_query += " USING TTL {0}; ".format(ttl)
        self.session.execute(create_query, (key, value), timeout=self.timeout)

    def close(self):
        self.session.cluster.shutdown()
        self.session.shutdown()


def key_factory(num):
    for i in range(num):
        yield i


def value(size):
    return bytearray(size)


def main():
    args = docopt(__doc__, version='1.0', options_first=True)
    servers = args['<servers>']
    port = int(args['--port'])
    keyspace = args['--keyspace']
    keys = int(args['--keys'])
    size = int(args['--size'])
    try:
        ttl = int(args['--ttl'])
    except ValueError:
        ttl = None

    username = args['--username']
    username =  None if username == 'None' else username

    passwd = args['--passwd']
    passwd =  None if passwd == 'None' else passwd

    replication = int(args['--replication'])
    timeout = float(args['--timeout'])

    cxn = Connection(servers, port, username, passwd, keyspace, replication, timeout)
    v = value(size)
    for key in key_factory(keys):
        cxn.insert(key, v, ttl)
    cxn.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
