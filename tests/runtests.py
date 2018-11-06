import sys
import logging
import subprocess
import os
import signal
import unittest

logging.basicConfig(level=logging.INFO, format="%(module)-15s - %(levelname)8s - %(message)s")



def usage():
    print("Usage: runtests.py dovecot")
    print("\tdovecot: path to the dovecot server")



if len(sys.argv) != 2:
    usage()
    sys.exit()



testmodules = ['testlogin', 'testfilter', 'testmailbox', 'testmsgheader', 'testmsgbody', 'testsetflag', 'testcopymsg', 'testcreatemsg', 'testmovemsg', 'testexpungemsgs', 'testcreatemailbox', 'testdeletemailbox', 'testrenamemailbox', 'testreply']

suite = unittest.TestSuite()

for testmodule in testmodules:
    try:
        logging.info("load test module " + testmodule)
        module = __import__("testcases."+testmodule, globals(), locals(), ['suite'])
        suite_function = getattr(module, 'suite')
        suite.addTests(suite_function())
    except (ImportError, AttributeError):
        print("test could not be loaded from module", testmodule)

unittest.TextTestRunner().run(suite)