import logging
import unittest
from testutil import *



class TestCopyMsg(unittest.TestCase):



    def copy_msg(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a copy_msg action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test copy_msg")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], [
            ("INBOX.Mailbox1", "from-a", "subject-a", ["to-a1", ], [], [], "text-a1\ntext-a2"),
            ("INBOX.Mailbox1", "from-b", "subject-b", ["to-b1", ], [], [], "text-b"),
            ("INBOX.Mailbox1", "from-c", "subject-c", ["to-c1", "to-c2"], ["cc-c1", "cc-c2"], ["bcc-c1"], "text-c1\ntext-c2"),
            ("INBOX.Mailbox2", "from-d", "subject-d", ["to-d1", ], [], [], "text-d"),
            ("INBOX.Mailbox2", "from-e", "subject-e", ["to-e1", ], [], [], "text-e"),
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "copy_msg.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and contains_answerset(answersets[-1], 'id1("from-c")') and contains_answerset(answersets[-1], 'id2("from-c")')), "unexpected answer set in " + str(answersets)


        # teardown

        kill_server(pid)



    def copy_msg_wrong_connection_id(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a copy_msg action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """

        logging.info("run test copy_msg_wrong_connection_id")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], [("INBOX", "from-a", "subject-a", ["to-a"], [], [], "test-a")]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "copy_msg_wrong_connection_id.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 1 and err[0] == "Error: connection 'wrong_server' not found", "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and answersets[-1] == "{}"), "unexpected answer set in " + str(answersets)


        # teardown

        kill_server(pid)



    def copy_msg_wrong_mailbox(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a copy_msg action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """

        logging.info("run test copy_msg_wrong_mailbox")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], [
            ("INBOX", "from-a", "subject-a", ["to-a"], [], [], "test-a")
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "copy_msg_wrong_mailbox.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 2 and err[0] == "Error: copying message failed", "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestCopyMsg('copy_msg'))
    test_suite.addTest(TestCopyMsg('copy_msg_wrong_mailbox'))
    test_suite.addTest(TestCopyMsg('copy_msg_wrong_connection_id'))
    return test_suite