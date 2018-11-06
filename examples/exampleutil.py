import  sys
import logging
import subprocess
import os
import signal
import shutil



IMAP_PLUGIN = "imapplugin"

TEST_DIR = "./"
PLUGIN_DIR = "../"

# relative paths inside the 'dovecot' program argument:
IMAP_SERVER = sys.argv[-1] + "sbin/dovecot" # relative path to the dovecot executable
PASSWD_FILE = sys.argv[-1] + "etc/passwd"   # relative path to the dovecot passwd file
MAILDIR = sys.argv[-1] + "home/"            # relative path to the dovecot maildir
LOGFILE = sys.argv[-1] + "dovecot.log"      # relative path to the dovecot logfile



def start_server():
    """
    start dovecot,
    if it is already running, kill it and restart

    :return: pid
    """
    logging.info("start dovecot")

    f = subprocess.Popen(IMAP_SERVER, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    f.wait()

    if f.returncode != 0:
        logging.warn("dovecot could not be started")

        output = f.communicate()
        if len(output) <= 1:
            logging.error("unexpected dovecot error message")
            return

        output = output[1].decode()

        if output.startswith("Fatal: Dovecot is already running with PID "):
            logging.info("dovecot is already running")

            output = output.split(" ")
            if len(output) <= 8:
                logging.error("dovecot could not be killed and restarted")
                return

            try:
                logging.info("kill dovecot")
                pid = int(output[output.index("PID")+1])
                os.kill(pid, signal.SIGTERM)

                logging.info("restart dovecot")
                f = subprocess.Popen(IMAP_SERVER, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                f.wait()
                if f.returncode != 0:
                    logging.error("dovecot could not be restarted")
                    return

            except:
                logging.error("dovecot could not be killed and restarted")
                return

    logging.info("dovecot now running with PID " + str(f.pid))
    return f.pid+1



def kill_server(pid):
    logging.info("kill dovecot")
    try:
        os.kill(pid, signal.SIGTERM)
    except:
        logging.error("dovecot could not be killed")



def set_server_state(server_state):
    """
    write the given usernames/passwords to dovecot's passwd file,
    insert the given messages into the given username's Maildirs

    :param server_state: tuple containing
            a list of n pairs (username, password)
            and n lists of 6-tuples (mailbox, sender, subject, recipients, ccs, bccs, text)
    """
    logging.info("set server state")

    passwd_file = open(PASSWD_FILE, "w")

    for user in server_state[0]:
        passwd_file.write(user[0] + ":{PLAIN}"+user[1]+":::::"+"\n")

    shutil.rmtree(MAILDIR, ignore_errors=True)
    os.mkdir(MAILDIR)

    for i in range(0, len(server_state[0])):
        os.mkdir(MAILDIR + server_state[0][i][0]) #create directory for each user
        os.mkdir(MAILDIR + server_state[0][i][0]+"/Maildir")
        os.mkdir(MAILDIR + server_state[0][i][0] + "/Maildir/cur")

        mailboxes = []

        for j in range(0, len(server_state[i+1])):
            (mailbox, sender, subject, recipients, ccs, bccs, body) = server_state[i+1][j]

            msg = None
            if mailbox == "INBOX":
                msg = open(MAILDIR+server_state[0][i][0] + "/Maildir/cur/message"+str(j), "w")
            else:
                if not mailboxes.__contains__(mailbox):
                    os.mkdir(MAILDIR+server_state[0][i][0]+"/Maildir/."+mailbox)
                    os.mkdir(MAILDIR+server_state[0][i][0]+"/Maildir/."+mailbox+"/cur")
                    mailboxes.append(mailbox)
                msg = open(MAILDIR+server_state[0][i][0] + "/Maildir/."+mailbox+"/cur/message"+str(j), "w")


            msg.write("From: "+ sender+"\n")
            msg.write("Subject: "+ subject+"\n")
            for recipient in recipients:
                msg.write("To: " + recipient + "\n")
            for cc in ccs:
                msg.write("Cc: " + cc + "\n")
            for bcc in bccs:
                msg.write("Bcc: " + bcc + "\n")
            msg.write(body)



def run_hexlite(program, plugin_paths, plugins):
    """
    run hexlite with the given program args

    :param program:
    :param plugin_paths:
    :param plugins:
    :return: pair (hexlite's stdout output as a list, hexlite's stderr output as a list)
    """
    logging.info("run hexlite with program " + program + ", plugin path " + str(plugin_paths) + " and plugins " + str(plugins))


    # build program argument list:

    args = ["acthex", program, "--pluginpath"]

    for plugin_path in plugin_paths:
        args.append(plugin_path)

    args.append("--plugin")

    for plugin in plugins:
        args.append(plugin)

    #args.append("--verbose")

    # run hexlite:

    f = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)


    # process results:

    out, err = f.communicate()

    status = int(f.returncode)
    assert status == 0, "unexpected exit status " + str(status)

    assert out == None or len(out) == 0 or (len(out) >= 1 and out.decode().split("\n")[-1] == ""), "unexpected hexlite stdout output " + str(out)
    assert err == None or len(err) == 0 or (len(err) >= 1 and err.decode().split("\n")[-1] == ""), "unexpected hexlite stderr output " + str(err)

    if out != None: logging.debug("hexlite printed the following output to stdout:\n\t" + out.decode().replace("\n", "\n\t"))
    if err != None: logging.debug("hexlite printed the following output to stderr:\n\t" + err.decode().replace("\n", "\n\t"))


    # return results:

    return (out.decode().split("\n") if out != None and len(out) > 1 else None,
            err.decode().split("\n") if err != None and len(err) > 1 else None)



def get_answersets(list):
    """
    filter and return the answer sets of the given list of an acthex-program's output

    :param list: containing an acthex-program's output
    :return: list of answer sets contained in the given list
    """

    answersets=[]
    for elem in list:
        if len(elem) >= 2 and elem[0] == "{" and elem[-1:] == "}":
            answersets.append(elem)
    return answersets



def contains_answerset(answerset, atom):
    """
    check if the given answer set contains the given atom

    :param answerset:
    :param atom:
    :return: True iff the given answer set contains the given atom
    """
    logging.info("check if " + str(answerset) + " contains " + str(atom))

    answerset = get_atoms_from_answerset(answerset)

    logging.debug("the answer set contains " + str(answerset))

    for a in answerset:
        if a == atom:
            return True

    return False



def count_atoms(answerset, name):
    """
    compute the number atoms in answerset with the given predicate name

    :param answerset:
    :param name:
    :return:
    """
    logging.info("count the number of atoms with predicate name " + str(name) + " in " + str(answerset))

    answerset = get_atoms_from_answerset(answerset)

    logging.debug("the answer set contains " + str(answerset))

    if name == None:
        logging.error("name is None")

    if type(name) != str:
        logging.error("name is no string")

    count = 0
    for atom in answerset:
        if atom.__contains__("("):
            if name == atom[:atom.index("(")]: count = count + 1
        elif name == atom: count = count + 1

    return count



def get_atoms_from_answerset(answerset):
    """
    return a list containing the atoms of the given answer set

    :param answerset:
    :return:
    """

    if answerset == None:
        logging.error("answer set is None")

    if len(answerset) < 2:
        logging.error("answer set does not start with '{' and end with '}'")

    if answerset[0] != "{":
        logging.error("answer set does not start with '{'")

    if answerset[-1] != "}":
        logging.error("answer set does not end with '}'")

    found_atoms = []
    stack = ""
    look_for_atom = True
    string = False

    for i in range(1, len(answerset) - 1):
        if look_for_atom:
            if answerset[i] == "(":
                look_for_atom = False
            if answerset[i] != ",":
                stack = stack + answerset[i]

        else:
            if not string and answerset[i] == ")":
                look_for_atom = True
                found_atoms.append(stack + ")")
                stack = ""
            else:
                if answerset[i] == '"':
                    string = not string
                stack = stack + answerset[i]

    return found_atoms



def get_logfile():
    """
    read dovecot's logfile

    :return: list containing the logfile's lines as elements
    """
    return open(LOGFILE, 'r').read().split("\n")



def clear_logfile():
    logging.info("clear logfile")
    open(LOGFILE, 'w').close()
