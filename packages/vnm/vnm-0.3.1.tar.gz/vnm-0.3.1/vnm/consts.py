NAME = 'VNM'
PROG = 'vnm'
VAR_PREFIX = 'VNM'
DESC = 'Virtual eNvironment Manager'
VERSION = [0, 3, 1, 'beta']
VERSION_STR = '.'.join([str(x) for x in VERSION[:2]])+(f'-{VERSION[3]}' if len(VERSION)>3 else '')
