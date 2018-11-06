import logging
import unittest
from testutil import *



class TestFilter(unittest.TestCase):



    def filter_success(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains filter atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """


        logging.info("run test filter_success")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),],
                          [("INBOX", "wanted_sender", "wanted_subject", ["recipient11", "recipient21"], [], ["bcc11", "bcc12", "bcc13"], ""),
                           ("INBOX", "wanted_sender", "subject1", ["recipient21", "wanted_recipient"], [], ["bcc2", ], ""),
                           ("INBOX", "sender3", "wanted_subject", ["recipient31", "recipient32"], ["cc3"], [], ""),
                           ("INBOX", "wanted_sender", "wanted_subject", ["recipient41", "wanted_recipient"], [], [], ""),
                           ("INBOX", "wanted_sender", "subject5", ["recipient5"], ["cc51", "cc52"], [], "")
                           ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "filter_success.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert len(answersets) >= 1 and len(answersets[-1].split(",")) == 3, "unexpected answer set " + str(answersets)


        # teardown

        kill_server(pid)



    def filter_no_messages(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains filter atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """


        logging.info("run test filter_no_messages")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], []))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "filter_success.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



    def filter_wrong_connection_id(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains filter atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """


        logging.info("run test filter_wrong_connection_id")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], []))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "filter_wrong_connection_id.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



    def filter_wrong_mailbox(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains filter atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """


        logging.info("run test filter_wrong_mailbox")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], []))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "filter_wrong_mailbox.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 2 and err[0] == "Error: selecting mailbox failed", "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



    def filter_invalid_filter(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains filter atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """


        logging.info("run test filter_invalid_filter")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], []))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "filter_invalid_filter.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 2 and err[0] == "Error: searching for messages failed", "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestFilter('filter_success'))
    test_suite.addTest(TestFilter('filter_no_messages'))
    test_suite.addTest(TestFilter('filter_wrong_connection_id'))
    test_suite.addTest(TestFilter('filter_wrong_mailbox'))
    test_suite.addTest(TestFilter('filter_invalid_filter'))
    return test_suite