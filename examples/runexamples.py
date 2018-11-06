import sys
import logging
import unittest
from exampleutil import *

logging.basicConfig(level=logging.DEBUG, format="%(module)-15s - %(levelname)8s - %(message)s")


class Test(unittest.TestCase):
    def copy_messages(self):
        logging.info("run example copy_messages")

        # setup

        set_server_state(([("user1@example.com", "password123"), ], [
                ("A", "user2@example.com", "example-subject", ["example-user", "user1@example.com"], [], [], "some text"),
                ("B", "user3@example.com", "example-IMAP-subject", ["user1@example.com"], [], [], "example text"),
                ("B", "user2@example.com", "example-imap-subject", ["user1@example.com", "user2@example.com"], [], [], "text"),
                ("A", "user2@example.com", "example-imap-subject", ["user1@example.com", "user4@example.com"], [], [], "example-text"),
                ("A", "user2@example.com", "Re: IMAP plugin", ["user4@example.com", "user5@example.com"], [], [], "message text")
        ]))
        pid = start_server()

        # execute

        acthex_program = TEST_DIR + "copy_messages.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)

        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stdout output " + str(err)

        # teardown

        kill_server(pid)



    def create_mailboxes(self):
        logging.info("run example create_mailboxes")

        # setup

        set_server_state(([("user1@example.com", "password123"), ], [
                ("A", "user2@example.com", "example subject 1", ["user1@domain.com", "user1@example.com"], [], [], "text"),
                ("A", "user2@example.com", "example subject 2", ["user1@example.com", "user1@example.com"], [], [], "example text"),
                ("A", "user2@example.com", "example subject 3", ["user4@domain.com", "user1@example.com"], [], [], "some text"),
                ("A", "user2@example.com", "example subject 4", ["user1@example.com"], [], [], "text"),
                ("A", "user2@example.com", "example subject 5", ["user1@example.com"], [], [], "example text"),

                ("B", "user3@example.com", "example subject", ["user1@example.com"], [], [], "example text"),
                ("INBOX.Mailbox1", "user3@example.com", "example subject", ["user1@example.com"], [], [], "example text"),
                ("A", "user3@example.com", "example subject 1", ["user1@example.com"], [], [], "example text 1"),
                ("A", "user3@example.com", "example subject 2", ["user1@example.com", "user2@example.com"], [], [], "example text 2"),
                ("A", "user3@example.com", "example subject 3", [], [], [], "example text 3"),
                ("A", "user3@example.com", "example subject 4", ["user1@example.com"], [], [], "example text 4"),
                ("A", "user3@example.com", "example subject 5", ["user1@example.com", "user3@example.com"], [], [], "example text 5"),
                ("A", "user3@example.com", "example subject 6", ["user1@example.com"], [], [], "example text 6"),

                ("B", "user3", "subject 123", ["user1@example.com", "user2@example.com"], [], [], "text"),
                ("A", "user2", "example subject", ["user1@example.com", "user4@domain.com"], [], [], "exampletext")
        ]))
        pid = start_server()

        # execute

        acthex_program = TEST_DIR + "create_mailboxes.hex"
        plugin_paths = (PLUGIN_DIR, ".")
        plugins = (IMAP_PLUGIN, "stringplugin")

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)

        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stdout output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and
                contains_answerset(answersets[-1], 'mailbox("MBuser3@example.com")')), "unexpected answer set in " + str(answersets)

        # teardown

        kill_server(pid)



    def delete_messages(self):
        logging.info("run example delete_messages")

        # setup

        set_server_state(([("user1@example.com", "password123"), ], [
                ("INBOX", "user2@example.com", "deleted message", ["user1@domain.com", "user1@example.com"], [], [], "text"),
                ("INBOX", "user2@example.com", "not-deleted message 1", ["user1@example.com"], [], [], "example text"),
                ("example mailbox", "user2@example.com", "not-deleted message 2", [], [], [], "some text"),
                ("INBOX", "user3@example.com", "example subject", ["user1@example.com"], [], [], "text"),
                ("example mailbox", "user4@example.com", "subject 123", ["user1@example.com"], [], [], "example text")
        ]))
        pid = start_server()

        acthex_program = TEST_DIR + "delete_messages_setup.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        run_hexlite(acthex_program, plugin_paths, plugins)


        # execute

        acthex_program = TEST_DIR + "delete_messages.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)

        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stdout output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and contains_answerset(answersets[-1], 'deleted("deleted message")') and contains_answerset(answersets[-1], 'deleted("not-deleted message 1")') and contains_answerset(answersets[-1], 'deleted("not-deleted message 2")') and count_atoms(answersets[-1], "deleted")), "unexpected answer set in " + str(answersets)

        # teardown

        kill_server(pid)




def usage():
    print("Usage: runexamples.py dovecot")
    print("\tdovecot: path to the dovecot server")



if len(sys.argv) != 2:
    usage()
    sys.exit()



suite = unittest.TestSuite()

suite.addTest(Test("copy_messages"))
suite.addTest(Test("create_mailboxes"))
suite.addTest(Test("delete_messages"))

unittest.TextTestRunner().run(suite)
