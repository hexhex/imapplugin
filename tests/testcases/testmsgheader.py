import logging
import unittest
from testutil import *



class TestMsgHeader(unittest.TestCase):



    def msg_header_success(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains msg_header atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test msg_header_success")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], [
            ("INBOX", "matching_sender", "subject_a", ["to_a1", "to_a2", "to_a3"], [], ["bcc_a1"], "text_a1\ntext_a2"),
            ("INBOX", "wrong_sender", "subject_b", ["to_b1", ], ["cc_b1", "cc_b2"], ["bcc_b1", ], "text_b"),
            ("INBOX", "wrong_sender", "subject_c", ["to_c1", "to_c2"], [], [], "text_c"),
            ("INBOX", "matching_sender", "subject_d", ["to_d1", "to_d2", "to_d3"], ["cc_cd",], ["bcc_d1", ], "text_d"),
            ("INBOX", "wrong_sender", "subject_e", ["to_e1", ], ["cc_e1", "cc_e2"], [], "text_e"),
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "msg_header_success.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and
                contains_answerset(answersets[-1], 'msg("matching_sender","subject_a")') and
                contains_answerset(answersets[-1], 'msg("matching_sender","subject_d")')), \
            "unexpected answer set in " + str(answersets)


        # teardown

        kill_server(pid)

        pass



    def msg_header_wrong_connection_id(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains msg_header atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """

        logging.info("run test msg_header_wrong_connection_id")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], []))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "msg_header_wrong_connection_id.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and answersets[-1] == "{}"), "unexpected answer set in " + str(answersets)


        # teardown

        kill_server(pid)



    def msg_header_wrong_mailbox(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains msg_header atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """

        logging.info("run test msg_header_wrong_mailbox")

        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], []))
        pid = start_server()

        # execute

        acthex_program = TEST_DIR + "msg_header_wrong_mailbox.hex"
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



    def msg_header_wrong_msg_id(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains msg_header atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """

        logging.info("run test msg_header_wrong_msg_id")

        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], []))
        pid = start_server()

        # execute

        acthex_program = TEST_DIR + "msg_header_wrong_msg_id.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)

        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 2 and err[0] == "Error: fetching message headers failed", "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and answersets[-1] == "{}"), "unexpected answer set in " + str(answersets)

        # teardown

        kill_server(pid)



    def msg_header_different_mailboxes(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains msg_header atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """

        logging.info("run test msg_header_different_mailboxes")

        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], [
            ("INBOX", "from-a", "subject-a", ["to-a1", "to-a2"], ["cc-a"], [], "text-a"),
            ("INBOX", "from-b", "subject-b", ["to-b"], [], [], "text-b"),
            ("INBOX.MyMailbox", "from-c", "subject-c", ["to-c1", "to-c1", "to-c3"], ["cc-c1", "cc-c2"], [], "text-c"),
        ]))
        pid = start_server()

        # execute

        acthex_program = TEST_DIR + "msg_header_different_mailboxes.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)

        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and
                contains_answerset(answersets[-1], 'subject("subject-a")') and
                contains_answerset(answersets[-1], 'subject("subject-b")') and
                contains_answerset(answersets[-1], 'subject("subject-c")')), \
            "unexpected answer set in " + str(answersets)

        # teardown

        kill_server(pid)



def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestMsgHeader('msg_header_success'))
    test_suite.addTest(TestMsgHeader('msg_header_wrong_connection_id'))
    test_suite.addTest(TestMsgHeader('msg_header_wrong_mailbox'))
    test_suite.addTest(TestMsgHeader('msg_header_wrong_msg_id'))
    test_suite.addTest(TestMsgHeader('msg_header_different_mailboxes'))
    return test_suite