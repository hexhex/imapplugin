import logging
import unittest
from testutil import *



class TestRenameMailbox(unittest.TestCase):



    def rename_mailbox(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a rename_mailbox action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test rename_mailbox")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], [
            ("Mailbox1", "from-a", "subject-a", ["to-a", ], [], [], "text-a1\ntext-a2"),
            ("Mailbox2", "from-b", "subject-b", ["to-b", ], ["cc-b1", "cc-b2"], [], "text-b"),
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "rename_mailbox.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and
                contains_answerset(answersets[-1], 'mailbox("INBOX")') and
                contains_answerset(answersets[-1], 'mailbox("Mailbox1")') and
                contains_answerset(answersets[-1], 'mailbox("INBOX.Mailbox2")') and
                count_atoms(answersets[-1], "mailbox") == 3), "unexpected answer set in " + str(answersets)


        # teardown

        kill_server(pid)



    def rename_mailbox_wrong_connection_id(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a rename_mailbox action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test rename_mailbox_wrong_connection_id")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], [
            ("Mailbox1", "from-a", "subject-a", ["to-a", ], [], [], "text-a1\ntext-a2")
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "rename_mailbox_wrong_connection_id.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 1 and err[0] == "Error: connection 'wrong_server' not found", "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



    def rename_mailbox_not_existing(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a rename_mailbox action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test rename_mailbox_not_existing")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], [
            ("Mailbox1", "from-a", "subject-a", ["to-a", ], [], [], "text-a1\ntext-a2")
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "rename_mailbox_not_existing.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 1 and err[0] == "Error: renaming mailbox failed", "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



    def rename_mailbox_already_exists(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a rename_mailbox action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test rename_mailbox_already_exists")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], [
            ("Mailbox1", "from-a", "subject-a", ["to-a", ], [], [], "text-a1\ntext-a2"),
            ("Mailbox2", "from-b", "subject-b", ["to-b", ], ["cc-b"], [], "text-b1\ntext-b2"),
            ("Mailbox3", "from-c", "subject-c", ["to-c", ], [], [], "text-c")
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "rename_mailbox_not_existing.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 1 and err[0] == "Error: renaming mailbox failed", "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestRenameMailbox('rename_mailbox'))
    test_suite.addTest(TestRenameMailbox('rename_mailbox_wrong_connection_id'))
    test_suite.addTest(TestRenameMailbox('rename_mailbox_not_existing'))
    test_suite.addTest(TestRenameMailbox('rename_mailbox_already_exists'))
    return test_suite