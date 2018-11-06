import logging
import unittest
from testutil import *



class TestReply(unittest.TestCase):



    def reply(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a reply action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test reply")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], [
            ("Mailbox1", "from-a", "subject-a", ["to-a1", "to-a2"], [], [], "text-a1\ntext-a2"),
            ("Mailbox2", "from-b", "subject-b", ["to-b", ], ["cc-b1", "cc-b2"], [], "text-b"),
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "reply.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert (len(answersets) >= 1 and
                contains_answerset(answersets[-1], 'draft(subject,"Re: subject-a")') and
                contains_answerset(answersets[-1], 'draft(cc,"to-a1")') and
                contains_answerset(answersets[-1], 'draft(cc,"to-a2")') and
                contains_answerset(answersets[-1], 'draft(from,"user1@example.com")') and
                contains_answerset(answersets[-1], 'draft(to,"from-a")') and
                contains_answerset(answersets[-1], 'draft(body,"reply-text")')), "unexpected answer set in " + str(answersets)


        # teardown

        kill_server(pid)



    def reply_wrong_connection_id(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a reply action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test reply_wrong_connection_id")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], [
            ("Mailbox1", "from-a", "subject-a", ["to-a1", "to-a2"], [], [], "text-a1\ntext-a2"),
            ("Mailbox2", "from-b", "subject-b", ["to-b", ], ["cc-b1", "cc-b2"], [], "text-b"),
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "reply_wrong_connection_id.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 1 and err[0] == "Error: connection 'wrong_server' not found", "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



    def reply_wrong_message_id(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that contains a reply action,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        """

        logging.info("run test reply_wrong_message_id")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], [
            ("Mailbox1", "from-a", "subject-a", ["to-a1", "to-a2"], [], [], "text-a1\ntext-a2"),
            ("Mailbox2", "from-b", "subject-b", ["to-b", ], ["cc-b1", "cc-b2"], [], "text-b"),
        ]))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "reply_wrong_message_id.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) >= 1 and err[0] == "Error: replying to message failed (fetching message headers failed)", "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestReply('reply'))
    test_suite.addTest(TestReply('reply_wrong_connection_id'))
    test_suite.addTest(TestReply('reply_wrong_message_id'))
    return test_suite