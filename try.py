#! /usr/bin/env python
# -*- coding: utf-8 -*-

import detuyun
from pprint import pprint


# ------------------ CONFIG ---------------------
BUCKETNAME = 'atest'
ACCESS_KEY = '10001'
ACCESS_SECRET = '123456'
# -----------------------------------------------


def ascii():
    content = "abcdefghijklmnopqrstuvwxyz\n" + \
              "01234567890112345678901234\n" + \
              "!@#$%^&*()-=[]{};':',.<>/?\n" + \
              "01234567890112345678901234\n" + \
              "abcdefghijklmnopqrstuvwxyz\n"

    return content


def run():

    dt = detuyun.DetuYun(BUCKETNAME, ACCESS_KEY, ACCESS_SECRET, timeout=30)

    print "=================================================="
    print "Getting Started with DetuYun Storage Service"
    print "==================================================\n"

    rootpath = '/test/'

    try:
        res = None

        print "Uploading a new object to DetuYun from a file ... ",
        headers = {"x-gmkerl-rotate": "180"}
        with open('unix.png', 'rb') as f:
            res = dt.put(rootpath + 'xinu.png', f, checksum=False,
                         headers=headers)
        print "oked\n"

        
        ispicbucket = True
        if res:
            print "[ width:%s, height:%s, frames:%s, type:%s ]\n" %\
                (res['width'], res['height'], res['frames'], res['type'])
        else:
            ispicbucket = False

        print "Downloading an object(%sxinu.png) ... " % rootpath,
        with open('xinu.png', 'wb') as f:
            dt.get(rootpath + 'xinu.png', f)
        print 'oked\n'

        if not ispicbucket:
            print "Uploading a new object to DetuYun from a stream "\
                  "of ASCII characters ... ",
            res = dt.put(rootpath + 'ascii.txt', ascii(), checksum=True)
            print "oked\n"

            print "Downloading an object(%sascii.txt) ... " % rootpath,
            res = dt.get(rootpath + 'ascii.txt')
            print "oked\n"

            if res:
                print res

        print "Creating an empty directory(%stemp/) ..." % rootpath,
        dt.mkdir(rootpath + 'temp')
        print "oked\n"

        # dt.endpoint = detuyun.ED_TELECOM

        print "Listing objects ...",
        res = dt.getlist(rootpath)
        print "oked\n"
        if res:
            space = 12
            types = ["name", "type", "size", "time"]
            print '|'.join([t.center(space) for t in types])
            print '-'*(space*len(types)+len(types)-1)
            for item in res:
                print '|'.join([' ' + item[t].ljust(space-1) for t in types])
            print

        print "Querying bucket usage ... ",
        res = dt.usage()
        print "oked\n"
        if res:
            print "[ use:" + res + " ]\n"

        print "Querying an object(%sxinu.png) info ..." % rootpath,
        res = dt.getinfo(rootpath + 'xinu.png')
        print "oked\n"
        print res 
        

        print "Deleting objects ...",
        dt.delete(rootpath + 'xinu.png')
        if not ispicbucket:
            dt.delete(rootpath + 'ascii.txt')
        dt.delete(rootpath + 'temp')
        dt.delete(rootpath)
        print "oked\n"

    except detuyun.DetuYunServiceException as se:
        print "failed\n"
        print "Except an DetuYunServiceException ..."
        print "HTTP Status Code: " + str(se.status)
        print "Error Message:    " + se.msg + "\n"
        if se.err:
            print se.err
    except detuyun.DetuYunClientException as ce:
        print "failed\n"
        print "Except an DetuYunClientException ..."
        print "Error Message: " + ce.msg + "\n"


if __name__ == '__main__':
    run()
