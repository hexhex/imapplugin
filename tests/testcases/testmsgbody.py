import logging
import unittest
from testutil import *



class TestMsgBody(unittest.TestCase):



    def msg_body_success(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains msg_body atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test msg_body_success")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], [
            ("INBOX", "test-sender-a", "test-subject-a", ["test-recipient-a-1", "test-recipient-a-2", "test-recipient-a-3"], [], [], "test-text-a"),
            ("INBOX", "test-sender-b", "test-subject-b", ["test-recipient-b-1", "test-recipient-b-2"], [], [], "test-text-b-1\ntest-text-b-2"),
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "msg_body_success.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and
                contains_answerset(answersets[-1], 'body("test-text-a")') and
                contains_answerset(answersets[-1], 'body("test-text-b-1\\ntest-text-b-2")')), \
            "unexpected answer set in " + str(answersets)


        # teardown

        kill_server(pid)



    def msg_body_no_text(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains msg_body atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test msg_body_no_text")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], [
            ("INBOX", "test-sender-a", "test-subject-a", ["test-recipient-a-1", "test-recipient-a-2", "test-recipient-a-3"], [], [], "test-text-a"),
            ("INBOX", "test-sender-b", "test-subject-b", ["test-recipient-b-1", "test-recipient-b-2"], [], [], ""),
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "msg_body_success.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and
                contains_answerset(answersets[-1], 'body("test-text-a")') and
                contains_answerset(answersets[-1], 'body("")')), \
            "unexpected answer set in " + str(answersets)


        # teardown

        kill_server(pid)



    def msg_body_wrong_connection_id(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains msg_body atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test msg_body_wrong_connection_id")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], []))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "msg_body_wrong_connection_id.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and answersets[-1] == "{}"), "unexpected answer set in " + str(answersets)


        # teardown

        kill_server(pid)



    def msg_body_wrong_mailbox(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains msg_body atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """

        logging.info("run test msg_body_wrong_mailbox")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], []))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "msg_body_wrong_mailbox.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 2 and err[0] == "Error: selecting mailbox failed", "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and answersets[-1] == "{}"), "unexpected answer set in " + str(answersets)


        # teardown

        kill_server(pid)



    def msg_body_wrong_message_id(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains msg_body atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """

        logging.info("run test msg_body_wrong_message_id")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], []))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "msg_body_wrong_message_id.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 2 and err[0] == "Error: fetching message body failed", "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and answersets[-1] == "{}"), "unexpected answer set in " + str(answersets)


        # teardown

        kill_server(pid)



def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestMsgBody('msg_body_success'))
    test_suite.addTest(TestMsgBody('msg_body_no_text'))
    test_suite.addTest(TestMsgBody('msg_body_wrong_connection_id'))
    test_suite.addTest(TestMsgBody('msg_body_wrong_mailbox'))
    test_suite.addTest(TestMsgBody('msg_body_wrong_message_id'))
    return test_suite