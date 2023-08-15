#!/usr/bin/env python3
"""Python script that provides some stats about Nginx logs stored in MongoDB"""
from pymongo import MongoClient


def log_stats():
    """Log stats"""
    with MongoClient() as client:
        nginx_coll = client.logs.nginx
        print(nginx_coll.count_documents({}), 'logs')
        print('Methods:')
        methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
        for method in methods:
            method_count = nginx_coll.count_documents({'method': method})
            print(f'\tmethod {method}: {method_count}')
        status_count = nginx_coll.count_documents(
            {'method': 'GET', 'path': '/status'})
        print(f'{status_count} status check')


if __name__ == '__main__':
    log_stats()
