import logging
import unittest
from testutil import *



class TestSetFlag(unittest.TestCase):



    def set_deleted(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains set_flag atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test set_deleted")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], [
            ("INBOX", "sender-a", "subject-a", ["recipient-a-1", "recipient-a-2", "recipient-a-3"], [], [], "text-a"),
            ("INBOX", "sender-b", "subject-b", ["recipient-b-1", "recipient-b-2"], [], [], "text-b-1\ntext-b-2"),
            ("INBOX", "sender-c", "subject-c", ["recipient-c-1", "recipient-c-2"], [], [], "test-text-c"),
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "set_deleted_1.hex"
        plugin_paths = (PLUGIN_DIR, PLUGIN_DIR + "tests")
        plugins = (IMAP_PLUGIN, "counterplugin")

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        acthex_program = TEST_DIR + "set_deleted_2.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and
                contains_answerset(answersets[-1], 'deleted("sender-a")') and
                contains_answerset(answersets[-1], 'deleted("sender-b")') and
                contains_answerset(answersets[-1], 'deleted("sender-c")')), \
            "unexpected answer set in " + str(answersets)

        # teardown

        kill_server(pid)



    def set_not_deleted(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains set_flag atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test set_not_deleted")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], [
            ("INBOX", "sender-a", "subject-a", ["recipient-a-1", "recipient-a-2", "recipient-a-3"], [], [], "text-a"),
            ("INBOX", "sender-b", "subject-b", ["recipient-b-1", "recipient-b-2"], [], [], "text-b-1\ntext-b-2"),
            ("INBOX", "sender-c", "subject-c", ["recipient-c-1", "recipient-c-2"], [], [], "test-text-c"),
        ]))
        pid = start_server()

        acthex_program = TEST_DIR + "set_deleted_1.hex"
        plugin_paths = (PLUGIN_DIR, PLUGIN_DIR + "tests")
        plugins = (IMAP_PLUGIN, "counterplugin")

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)


        # execute

        acthex_program = TEST_DIR + "set_not_deleted_1.hex"
        plugin_paths = (PLUGIN_DIR, PLUGIN_DIR + "tests")
        plugins = (IMAP_PLUGIN, "counterplugin")

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        acthex_program = TEST_DIR + "set_not_deleted_2.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and
                contains_answerset(answersets[-1], 'not_deleted("sender-a")') and
                contains_answerset(answersets[-1], 'not_deleted("sender-b")') and
                contains_answerset(answersets[-1], 'not_deleted("sender-c")')), \
            "unexpected answer set in " + str(answersets)

        # teardown

        kill_server(pid)



    def set_draft_seen(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains set_flag atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test set_draft_seen")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], [
            ("INBOX", "sender-a", "subject-a", ["recipient-a-1", "recipient-a-2", "recipient-a-3"], [], [], "text-a"),
            ("INBOX", "sender-b", "subject-b", ["recipient-b-1", "recipient-b-2"], [], [], "text-b-1\ntext-b-2"),
            ("INBOX", "sender-c", "subject-c", ["recipient-c-1", "recipient-c-2"], [], [], "test-text-c"),
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "set_draft_seen_1.hex"
        plugin_paths = (PLUGIN_DIR, PLUGIN_DIR + "tests")
        plugins = (IMAP_PLUGIN, "counterplugin")

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        acthex_program = TEST_DIR + "set_draft_seen_2.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and
                contains_answerset(answersets[-1], 'from("sender-a")') and
                contains_answerset(answersets[-1], 'from("sender-b")') and
                contains_answerset(answersets[-1], 'from("sender-c")')), \
            "unexpected answer set in " + str(answersets)


        # teardown

        kill_server(pid)



    def set_deleted_wrong_connection_id(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains set_flag atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test set_deleted_wrong_connection_id")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], [
            ("INBOX", "sender-a", "subject-a", ["recipient-a-1", "recipient-a-2", "recipient-a-3"], [], [], "text-a"),
            ("INBOX", "sender-b", "subject-b", ["recipient-b-1", "recipient-b-2"], [], [], "text-b-1\ntext-b-2"),
            ("INBOX", "sender-c", "subject-c", ["recipient-c-1", "recipient-c-2"], [], [], "test-text-c"),
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "set_deleted_wrong_connection_id.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 1 and err[0] == "Error: connection 'wrong_server' not found", "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



    def set_deleted_wrong_mailbox(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains set_flag atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test set_deleted_wrong_mailbox")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], [
            ("INBOX", "sender-a", "subject-a", ["recipient-a-1", "recipient-a-2", "recipient-a-3"], [], [], "text-a"),
            ("INBOX", "sender-b", "subject-b", ["recipient-b-1", "recipient-b-2"], [], [], "text-b-1\ntext-b-2"),
            ("INBOX", "sender-c", "subject-c", ["recipient-c-1", "recipient-c-2"], [], [], "test-text-c"),
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "set_deleted_wrong_mailbox.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 2 and err[0] == "Error: selecting mailbox failed", "unexpected hexlite stderr output " + str(err)


        # teardown


        kill_server(pid)



    def set_deleted_wrong_message_id(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains set_flag atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test set_deleted_wrong_mailbox")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], [
            ("INBOX", "sender-a", "subject-a", ["recipient-a-1", "recipient-a-2", "recipient-a-3"], [], [], "text-a"),
            ("INBOX", "sender-b", "subject-b", ["recipient-b-1", "recipient-b-2"], [], [], "text-b-1\ntext-b-2"),
            ("INBOX", "sender-c", "subject-c", ["recipient-c-1", "recipient-c-2"], [], [], "test-text-c"),
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "set_deleted_wrong_message_id.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 2 and err[0] == "Error: storing message flag failed", "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestSetFlag('set_deleted'))
    test_suite.addTest(TestSetFlag('set_not_deleted'))
    test_suite.addTest(TestSetFlag('set_draft_seen'))
    test_suite.addTest(TestSetFlag('set_deleted_wrong_connection_id'))
    test_suite.addTest(TestSetFlag('set_deleted_wrong_mailbox'))
    test_suite.addTest(TestSetFlag('set_deleted_wrong_message_id'))
    return test_suite