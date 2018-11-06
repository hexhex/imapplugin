import logging
import unittest
from testutil import *



class TestMailbox(unittest.TestCase):



    def mailbox(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains mailbox atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """


        logging.info("run test mailbox")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),],
                          [("INBOX", "from a", "subject a", ["to a1", "to a2"], ["cc-a1"], [], "text a"),
                           ("INBOX.Mailbox1", "from b", "subject b", [], ["cc-b1", "cc-b2"], [], "text b"),
                           ("INBOX.Mailbox2", "from c", "subject c", ["to c1", ], [], [], "text c1\ntext c2"),
                           ("INBOX.Mailbox 2", "from d", "subject d", ["to d1", "to d2", "to d3"], [], ["bcc d1"], ""),
                           ("INBOX.Mailbox2.Mailbox3", "from e", "subject e", ["to e1"], ["cc-e1", "cc-e2", "cc-e3"], [], "text e"),
                           ("INBOX.Mailbox 2.Mailbox4", "from f", "subject f", ["to f1", "to f2"], [], [], ""),
                           ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "mailbox.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and
                contains_answerset(answersets[-1], 'mailbox("INBOX")') and
                contains_answerset(answersets[-1], 'mailbox("INBOX.Mailbox1")') and
                contains_answerset(answersets[-1], 'mailbox("INBOX.Mailbox2")') and
                contains_answerset(answersets[-1], 'mailbox("INBOX.Mailbox 2")') and
                contains_answerset(answersets[-1], 'mailbox("INBOX.Mailbox2.Mailbox3")') and
                contains_answerset(answersets[-1], 'mailbox("INBOX.Mailbox 2.Mailbox4")') and
                count_atoms(answersets[-1], "mailbox") == 6
                ), "unexpected answer set " + str(answersets)


        # teardown

        kill_server(pid)



    def mailbox_wrong_connection_id(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains mailbox atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """


        logging.info("run test mailbox_wrong_connection_id")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], []))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "mailbox_wrong_connection_id.hex"
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



    def mailbox_no_mailboxes(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains mailbox atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """


        logging.info("run test mailbox_no_mailboxes")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], []))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "mailbox.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and
                contains_answerset(answersets[-1], 'mailbox("INBOX")') and
                count_atoms(answersets[-1], "mailbox") == 1
                ), "unexpected answer set " + str(answersets)


        # teardown

        kill_server(pid)



    def mailbox_invalid_path(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains mailbox atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """


        logging.info("run test mailbox_invalid_path")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),],
                          [("INBOX", "from a", "subject a", ["to a1", "to a2"], ["cc-a1"], [], "text a"),
                           ("INBOX.Mailbox1", "from b", "subject b", [], ["cc-b1", "cc-b2"], [], "text b"),
                           ("INBOX.Mailbox2", "from c", "subject c", ["to c1", ], [], [], "text c1\ntext c2"),
                           ("INBOX.Mailbox 2", "from d", "subject d", ["to d1", "to d2", "to d3"], [], ["bcc d1"], ""),
                           (
                           "INBOX.Mailbox2.Mailbox3", "from e", "subject e", ["to e1"], ["cc-e1", "cc-e2", "cc-e3"], [],
                           "text e"),
                           ("INBOX.Mailbox 2.Mailbox4", "from f", "subject f", ["to f1", "to f2"], [], [], ""),
                           ]
                          ))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "mailbox_invalid_path.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and answersets[-1] == "{}"), "unexpected answer set " + str(answersets)


        # teardown

        kill_server(pid)



    def mailbox_name_pattern(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains mailbox atoms,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """


        logging.info("run test mailbox_name_pattern")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),],
                          [("INBOX", "from a", "subject a", ["to a1", "to a2"], ["cc-a1"], [], "text a"),
                           ("INBOX.Mailbox1", "from b", "subject b", [], ["cc-b1", "cc-b2"], [], "text b"),
                           ("INBOX.Mailbox2", "from c", "subject c", ["to c1", ], [], [], "text c1\ntext c2"),
                           ("INBOX.Mailbox 2", "from d", "subject d", ["to d1", "to d2", "to d3"], [], ["bcc d1"], ""),
                           (
                           "INBOX.Mailbox2.Mailbox3", "from e", "subject e", ["to e1"], ["cc-e1", "cc-e2", "cc-e3"], [],
                           "text e"),
                           ("INBOX.Mailbox 2.Mailbox4", "from f", "subject f", ["to f1", "to f2"], [], [], ""),
                           ]
                          ))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "mailbox_name_pattern.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and
                contains_answerset(answersets[-1], 'mailbox("INBOX.Mailbox1")') and
                contains_answerset(answersets[-1], 'mailbox("INBOX.Mailbox2")') and
                contains_answerset(answersets[-1], 'mailbox("INBOX.Mailbox 2")') and
                contains_answerset(answersets[-1], 'mailbox("INBOX.Mailbox2.Mailbox3")') and
                contains_answerset(answersets[-1], 'mailbox("INBOX.Mailbox 2.Mailbox4")') and
                count_atoms(answersets[-1], "mailbox") == 5
                ), "unexpected answer set " + str(answersets)


        # teardown

        kill_server(pid)



def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestMailbox('mailbox'))
    test_suite.addTest(TestMailbox('mailbox_wrong_connection_id'))
    test_suite.addTest(TestMailbox('mailbox_no_mailboxes'))
    test_suite.addTest(TestMailbox('mailbox_invalid_path'))
    test_suite.addTest(TestMailbox('mailbox_name_pattern'))
    return test_suite