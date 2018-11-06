import logging
import unittest
from testutil import *



class TestCreateMsg(unittest.TestCase):



    def create_msg(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a create_msg action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """

        logging.info("run test create_msg")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], [("INBOX", "from-a", "subject-a", ["to-a"], [], [], "test-a")]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "create_msg.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and
                contains_answerset(answersets[-1], 'msg(from,"from-b")') and
                contains_answerset(answersets[-1], 'msg(to,"to-a-1")') and
                contains_answerset(answersets[-1], 'msg(to,"to-a-2")') and
                contains_answerset(answersets[-1], 'msg(subject,"subject-b")') and
                contains_answerset(answersets[-1], 'msg(cc,"cc-b")')), \
            "unexpected answer set in " + str(answersets)


        # teardown

        kill_server(pid)



    def create_msg_wrong_connection_id(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a create_msg action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """

        logging.info("run test create_msg_wrong_connection_id")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], []))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "create_msg_wrong_connection_id.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 1 and err[0] == "Error: connection 'wrong_server' not found", "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



    def create_msg_wrong_mailbox(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a create_msg action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """

        logging.info("run test create_msg_wrong_mailbox")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], []))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "create_msg_wrong_mailbox.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 1 and err[0] == "Error: connection 'text_server' not found", "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



    def create_msg_invalid_recipients(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a create_msg action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """

        logging.info("run test create_msg_invalid_recipients")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], []))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "create_msg_invalid_recipients.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 2 and err[0] == 'Error: function "to-a" is invalid', "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



    def create_msg_subject_no_string(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a create_msg action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """

        logging.info("run test create_msg_subject_no_string")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], []))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "create_msg_subject_no_string.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 2 and err[0] == "Error: term subject is invalid (expected to begin with \", but was 'invalid_subject')", "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestCreateMsg('create_msg'))
    test_suite.addTest(TestCreateMsg('create_msg_wrong_connection_id'))
    test_suite.addTest(TestCreateMsg('create_msg_wrong_mailbox'))
    test_suite.addTest(TestCreateMsg('create_msg_invalid_recipients'))
    test_suite.addTest(TestCreateMsg('create_msg_subject_no_string'))
    return test_suite