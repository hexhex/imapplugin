import logging
import unittest
from testutil import *



class TestMoveMsg(unittest.TestCase):



    def move_msg(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a move_msg action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test move_msg")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], [
            ("INBOX.Mailbox1", "from-a", "subject-a", ["to-a1", ], [], [], "text-a1\ntext-a2"),
            ("INBOX.Mailbox1", "from-b", "subject-b", ["to-b1", ], [], [], "text-b"),
            ("INBOX.Mailbox2", "from-c", "subject-c", ["to-c1", ], [], [], "text-c")
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "move_msg.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and
                contains_answerset(answersets[-1], 'from1("from-a",no)') and
                contains_answerset(answersets[-1], 'from1("from-b",yes)') and
                contains_answerset(answersets[-1], 'from2("from-b",no)') and
                contains_answerset(answersets[-1], 'from2("from-c",no)')), "unexpected answer set in " + str(answersets)


        # teardown

        kill_server(pid)



    def move_msg_deleted(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a move_msg action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test move_msg_deleted")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], [
            ("INBOX.Mailbox1", "from-a", "subject-a", ["to-a1", ], [], [], "text-a1\ntext-a2"),
            ("INBOX.Mailbox1", "from-b", "subject-b", ["to-b1", ], [], [], "text-b"),
            ("INBOX.Mailbox2", "from-c", "subject-c", ["to-c1", ], [], [], "text-c")
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "move_msg_deleted.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and
                contains_answerset(answersets[-1], 'from1("from-a",no)') and
                contains_answerset(answersets[-1], 'from1("from-b",yes)') and
                contains_answerset(answersets[-1], 'from2("from-b",yes)') and
                contains_answerset(answersets[-1], 'from2("from-c",no)')), "unexpected answer set in " + str(answersets)


        # teardown

        kill_server(pid)



    def move_msg_wrong_connection_id(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a move_msg action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test move_msg_wrong_connection_id")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], [
            ("INBOX.Mailbox1", "from-a", "subject-a", ["to-a1", ], [], [], "text-a1\ntext-a2"),
            ("INBOX.Mailbox1", "from-b", "subject-b", ["to-b1", ], [], [], "text-b"),
            ("INBOX.Mailbox2", "from-c", "subject-c", ["to-c1", ], [], [], "text-c")
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "move_msg_wrong_connection_id.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 1 and err[0] == "Error: connection 'wrong_server' not found", "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



    def move_msg_wrong_mailbox(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a move_msg action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test move_msg_wrong_mailbox")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], [
            ("INBOX.Mailbox1", "from-a", "subject-a", ["to-a1", ], [], [], "text-a1\ntext-a2"),
            ("INBOX.Mailbox1", "from-b", "subject-b", ["to-b1", ], [], [], "text-b"),
            ("INBOX.Mailbox2", "from-c", "subject-c", ["to-c1", ], [], [], "text-c")
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "move_msg_wrong_mailbox.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) > 0 and err[0] == "Error: moving message failed (message could not be copied)", "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



    def move_msg_wrong_message_id(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a move_msg action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test move_msg_wrong_message_id")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], [
            ("INBOX.Mailbox1", "from-a", "subject-a", ["to-a1", ], [], [], "text-a1\ntext-a2"),
            ("INBOX.Mailbox1", "from-b", "subject-b", ["to-b1", ], [], [], "text-b"),
            ("INBOX.Mailbox2", "from-c", "subject-c", ["to-c1", ], [], [], "text-c")
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "move_msg_wrong_message_id.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) > 0 and err[0] == "Error: moving message failed (message could not be copied)", "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestMoveMsg('move_msg'))
    test_suite.addTest(TestMoveMsg('move_msg_deleted'))
    test_suite.addTest(TestMoveMsg('move_msg_wrong_connection_id'))
    test_suite.addTest(TestMoveMsg('move_msg_wrong_mailbox'))
    test_suite.addTest(TestMoveMsg('move_msg_wrong_message_id'))
    return test_suite