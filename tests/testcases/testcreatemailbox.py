import logging
import unittest
from testutil import *



class TestCreateMailbox(unittest.TestCase):



    def create_mailbox(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a create_mailbox action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test create_mailbox")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], [
            ("INBOX.Mailbox1", "from-a", "subject-a", ["to-a", ], [], [], "text-a1\ntext-a2"),
            ("INBOX.Mailbox1", "from-b", "subject-b", ["to-b1", "to-b2"], [], [], "text-b"),
            ("Mailbox2", "from-c", "subject-c", ["to-c", ], ["cc-c1", "cc-c2"], ["bcc-c1", "bcc-c2", "bcc-c3"], "text-c"),
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "create_mailbox.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and
                contains_answerset(answersets[-1], 'mailbox("INBOX")') and
                contains_answerset(answersets[-1], 'mailbox("INBOX.Mailbox1")') and
                contains_answerset(answersets[-1], 'mailbox("Mailbox2")') and
                contains_answerset(answersets[-1], 'mailbox("Mailbox3")') and
                contains_answerset(answersets[-1], 'mailbox("Mailbox2.Mailbox4")') and
                contains_answerset(answersets[-1], 'mailbox("Mailbox2.Mailbox1.Mailbox5")') and
                count_atoms(answersets[-1], "mailbox") == 6), "unexpected answer set in " + str(answersets)


        # teardown

        kill_server(pid)



    def create_mailbox_already_exists(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a create_mailbox action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test create_mailbox_already_exists")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], [("INBOX.Mailbox1", "from-a", "subject-a", ["to-a", ], [], [], "text-a1\ntext-a2")]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "create_mailbox_already_exists.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 1 and err[0] == "Error: creating mailbox failed", "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



    def create_mailbox_wrong_connection_id(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a create_mailbox action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test create_mailbox_wrong_connection_id")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], []))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "create_mailbox_wrong_connection_id.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 1 and err[0] == "Error: connection 'wrong_server' not found", "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



    def create_mailbox_empty_string(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a create_mailbox action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test create_mailbox_empty_string")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], []))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "create_mailbox_empty_string.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None, "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestCreateMailbox('create_mailbox'))
    test_suite.addTest(TestCreateMailbox('create_mailbox_already_exists'))
    test_suite.addTest(TestCreateMailbox('create_mailbox_wrong_connection_id'))
    test_suite.addTest(TestCreateMailbox('create_mailbox_empty_string'))
    return test_suite