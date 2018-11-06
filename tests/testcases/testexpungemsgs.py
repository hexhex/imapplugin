import logging
import unittest
from testutil import *



class TestExpungeMsgs(unittest.TestCase):



    def expunge_msgs(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a expunge_msgs action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test expunge_msgs")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], [
            ("INBOX.Mailbox1", "from-a", "subject-a", ["to-a", ], [], [], "text-a1\ntext-a2"),
            ("INBOX.Mailbox1", "from-b", "subject-b", ["to-b1", "to-b2"], [], [], "text-b"),
            ("INBOX.Mailbox1", "from-c", "subject-c", ["to-c", ], ["cc-c1", "cc-c2"], ["bcc-c1", "bcc-c2", "bcc-c3"], "text-c1\ntextc2\n\ntextc3\ntextc4"),
            ("INBOX.Mailbox2", "from-d", "subject-d", ["to-d1", "to-d2"], ["cc-d1", "cc-d2"], [], "text-d"),
            ("INBOX.Mailbox2", "from-e", "subject-e", ["to-e", ], [], [], "text-e")
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "expunge_msgs.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and
                contains_answerset(answersets[-1], 'from("from-b")') and
                contains_answerset(answersets[-1], 'from("from-d")') and
                contains_answerset(answersets[-1], 'from("from-e")') and
                count_atoms(answersets[-1], "from") == 3), "unexpected answer set in " + str(answersets)


        # teardown

        kill_server(pid)



    def expunge_msgs_wrong_connection_id(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a expunge_msgs action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test expunge_msgs_wrong_connection_id")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], [
            ("INBOX.Mailbox1", "from-a", "subject-a", ["to-a", ], [], [], "text-a1\ntext-a2"),
            ("INBOX.Mailbox1", "from-b", "subject-b", ["to-b1", "to-b2"], [], [], "text-b"),
            ("INBOX.Mailbox1", "from-c", "subject-c", ["to-c", ], ["cc-c1", "cc-c2"], ["bcc-c1", "bcc-c2", "bcc-c3"],
             "text-c1\ntextc2\n\ntextc3\ntextc4"),
            ("INBOX.Mailbox2", "from-d", "subject-d", ["to-d1", "to-d2"], ["cc-d1", "cc-d2"], [], "text-d"),
            ("INBOX.Mailbox2", "from-e", "subject-e", ["to-e", ], [], [], "text-e")
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "expunge_msgs_wrong_connection_id.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 1 and err[0] == "Error: connection 'wrong_server' not found", "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and answersets[-1] == "{}"), "unexpected answer set in " + str(answersets)


        # teardown

        kill_server(pid)



    def expunge_msgs_wrong_mailbox(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a expunge_msgs action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test expunge_msgs_wrong_mailbox")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], [
            ("INBOX.Mailbox1", "from-a", "subject-a", ["to-a", ], [], [], "text-a1\ntext-a2"),
            ("INBOX.Mailbox1", "from-b", "subject-b", ["to-b1", "to-b2"], [], [], "text-b"),
            ("INBOX.Mailbox1", "from-c", "subject-c", ["to-c", ], ["cc-c1", "cc-c2"], ["bcc-c1", "bcc-c2", "bcc-c3"],
             "text-c1\ntextc2\n\ntextc3\ntextc4"),
            ("INBOX.Mailbox2", "from-d", "subject-d", ["to-d1", "to-d2"], ["cc-d1", "cc-d2"], [], "text-d"),
            ("INBOX.Mailbox2", "from-e", "subject-e", ["to-e", ], [], [], "text-e")
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "expunge_msgs_wrong_mailbox.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 1 and err[0] == "Error: selecting mailbox failed", "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and answersets[-1] == "{}"), "unexpected answer set in " + str(answersets)


        # teardown

        kill_server(pid)



def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestExpungeMsgs('expunge_msgs'))
    test_suite.addTest(TestExpungeMsgs('expunge_msgs_wrong_connection_id'))
    test_suite.addTest(TestExpungeMsgs('expunge_msgs_wrong_mailbox'))
    return test_suite