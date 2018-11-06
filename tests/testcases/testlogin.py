import logging
import unittest
from testutil import *



class TestLogin(unittest.TestCase):



    def login_success(self):
        """
        clear the logfile,
        setup the imap server,
        start the imap server,

        run an acthex program that performs a login,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated,
        assert that the logfile reports a successful login
        """

        logging.info("run test login_success")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], []))
        pid = start_server()
        clear_logfile()


        # execute

        acthex_program = TEST_DIR + "login_success.hex"
        plugin_paths = (PLUGIN_DIR, PLUGIN_DIR + "tests")
        plugins = (IMAP_PLUGIN, "counterplugin")

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert len(answersets) >= 1 and answersets[-1] == "{login_successful}", "unexpected answer set"

        logs = get_logfile()
        assert (len(logs) >= 1 and len(logs[len(logs)-2]) >= 27 and logs[len(logs)-2][16:26] == "imap-login") or (len(logs) >= 2 and len(logs[len(logs)-3]) >= 27 and logs[len(logs)-3][16:26] == "imap-login"), "unexpected dovecot logfile"


        # teardown

        kill_server(pid)



    def login_username_no_string(self):
        """
        run an acthex program that performs a login,

        assert that the evaluation of the acthex program results in the expected output
        """

        logging.info("run test login_username_no_string")


        # execute

        acthex_program = TEST_DIR + "login_username_no_string.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) == 2 and err[0] == "Error: term user is invalid (expected to begin with \", but was 'username_no_string')", "unexpected hexlite stderr output " + str(err)



    def login_with_already_used_connection_id(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that performs two logins using the same connection_id,

        assert that the evaluation of the acthex program results in the expected output
        assert that the logfile reports two successful logins and one logout
        """

        logging.info("run test login_with_already_used_connection_id")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], []))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "login_with_already_used_connection_id.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stdout output " + str(err)

        logs = get_logfile()
        assert (
                (len(logs) >= 3 and
                len(logs[len(logs)-2]) >= 27 and logs[len(logs)-2][16:26] == "imap-login" and
                len(logs[len(logs)-3]) >= 16 and logs[len(logs)-3][16:].startswith("imap(user1@example.com): Info: Logged out") and
                len(logs[len(logs)-4]) >= 27 and logs[len(logs)-4][16:26] == "imap-login")
                or
                (len(logs) >= 4 and
                len(logs[len(logs) - 3]) >= 27 and logs[len(logs) - 3][16:26] == "imap-login" and
                len(logs[len(logs) - 4]) >= 16 and logs[len(logs) - 4][16:].startswith("imap(user1@example.com): Info: Logged out") and
                len(logs[len(logs) - 5]) >= 27 and logs[len(logs) - 5][16:26] == "imap-login")
        ), "unexpected dovecot logfile"


        # teardown

        kill_server(pid)



    def login_wrong_hostname(self):
        """
        run an acthex program that performs a login at a server with a not-existing hostname,

        assert that the evaluation of the acthex program results in the expected output
        """

        logging.info("run test login_wrong_hostname")


        # execute

        acthex_program = TEST_DIR + "login_wrong_hostname.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) == 2 and err[0] == "Error: connecting to server failed", "unexpected hexlite stderr output " + str(err)



    def login_wrong_password(self):
        """
        run an acthex program that performs a login with a wrong password,

        assert that the evaluation of the acthex program results in the expected output,
        """

        logging.info("run test login_wrong_password")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"),], []))
        pid = start_server()


        # execute

        acthex_program = TEST_DIR + "login_wrong_password.hex"
        plugin_paths = (PLUGIN_DIR,)
        plugins = (IMAP_PLUGIN,)

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err != None and len(err) == 2 and err[0] == "Error: login failed", "unexpected hexlite stderr output " + str(err)


        # teardown

        kill_server(pid)



    def not_logged_in(self):
        """
        setup the imap server,
        start the imap server,

        run an acthex program that performs a login,

        assert that the evaluation of the acthex program results in the expected output,
        assert that the expected answer set is evaluated
        """

        logging.info("run test not_logged_in")


        # setup

        set_server_state(([("user1@example.com", "passw0rd123"), ], []))
        pid = start_server()
        clear_logfile()


        # execute

        acthex_program = TEST_DIR + "not_logged_in.hex"
        plugin_paths = (PLUGIN_DIR, )
        plugins = (IMAP_PLUGIN, )

        out, err = run_hexlite(acthex_program, plugin_paths, plugins)


        # verify

        assert out != None, "unexpected hexlite stdout output " + str(out)
        assert err == None, "unexpected hexlite stderr output " + str(err)

        answersets = get_answersets(out)
        assert len(answersets) >= 1 and answersets[-1] == "{-logged_in(wrong_connection_id)}", "unexpected answer set"


        # teardown

        kill_server(pid)



def suite():
    test_suite = unittest.TestSuite()
    test_suite.addTest(TestLogin('login_success'))
    test_suite.addTest(TestLogin('login_username_no_string'))
    test_suite.addTest(TestLogin('login_with_already_used_connection_id'))
    test_suite.addTest(TestLogin('login_wrong_hostname'))
    test_suite.addTest(TestLogin('not_logged_in'))
    test_suite.addTest(TestLogin('login_wrong_password'))
    return test_suite