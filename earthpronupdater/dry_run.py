"""Dry run script."""

from earthpron import test

if __name__ == '__main__':
    print 'Run with python -i to tinker with the "t" variable after execution'
    t = test(limit=25)
