# Copyright (c) 2018 Andreas Schmidt

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.



import acthex
import imaplib
import sys
import email
import email.message



def login(connection_id, host, port, user, password, ssl):
    """
    Establish a connection to the specified IMAP server and logs into the specified email account.

    :param connection_id: term identifying the IMAP server to connect to
    :param host: string containing the IMAP server's hostname or IP address
    :param port: integer representing the IMAP server's port
    :param user: string containing the email account's user name
    :param password: string containing the email account's password
    :param ssl: iff 0, the connection is not encrypted
    :return:
    """

    print("called @login("+ str(connection_id) +", "+ str(host)+", "+ str(port)+", "+ str(user)+", "+ str(password)+", "+ str(ssl)+")")

    connection_id = get_term("connection_id", connection_id, True)
    host = get_string_from_term("host", host, True)
    port = get_int_from_term("port", port, True)
    user = get_string_from_term("user", user, True)
    password = get_string_from_term("password", password, True)

    ssl = get_term("ssl", ssl, True)
    if ssl == "0": ssl = False
    else: ssl = True

    acthex.environment().login(connection_id, host, port, user, password, ssl)



def logged_in(connection_id):
    """
    True if there is a connection to an IMAP server identified by connection_id.

    :param connection_id: term identifying the IMAP server connection
    :return:
    """

    print("called &logged_in("+ str(connection_id)+")")

    connection_id = get_term("connection_id", connection_id, False)

    if acthex.environment().logged_in(connection_id):
        print("logged in")
        acthex.output(())
    else: print("not logged in")



def filter(connection_id, mailbox, filter):
    """
    Return the message IDs of the messages that match the given filter

    :param connection_id: term identifying the IMAP server connection
    :param mailbox: string containing the mailbox name
    :param filter: string containing a filter
    :return:
    """

    print("called &filter("+ str(connection_id)+", "+ str(mailbox)+", "+ str(filter)+")")

    connection_id = get_term("connection_id", connection_id, False)
    mailbox = get_string_from_term("mailbox", mailbox, False)
    filter = get_string_from_term("filter", filter, False)
    filter = filter.replace("'", '"')

    messages = acthex.environment().filter(connection_id, mailbox, filter)
    if messages != None:
        print("found message_ids " + str(messages))
        for message in messages:
            acthex.output((message,))



def msg_header(connection_id, mailbox, message_id):
    """
    Return pairs (type, value) for each header information of the specified message.

    :param connection_id: term identifying the IMAP server connection
    :param mailbox: string containing the mailbox name
    :param message_id: integer representing the message ID
    :return:
    """

    print("called &msg_header(" + str(connection_id)+", "+ str(mailbox)+", "+ str(message_id)+")")

    connection_id = get_term("connection_id", connection_id, False)
    mailbox = get_string_from_term("mailbox", mailbox, False)
    message_id = get_int_from_term("message_id", message_id, False)

    headers = acthex.environment().msg_header(connection_id, mailbox, message_id)
    if headers != None:
        print("found headers", end=" ")
        for type, value in headers:
            type = type.replace("-", "")
            print("("+str(type.lower())+', "'+str(value)+'")', end=" ")
            acthex.output((type.lower(), '"'+value+'"'))
        print()



def msg_body(connection_id, mailbox, message_id):
    """
    Return the body of the specified message.

    :param connection_id: term identifying the IMAP server connection
    :param mailbox: string containing the mailbox name
    :param message_id: integer representing the message ID
    :return:
    """

    print("called &msg_body("+ str(connection_id)+", "+ str(mailbox)+", "+ str(message_id)+")")

    connection_id = get_term("connection_id", connection_id, False)
    mailbox = get_string_from_term("mailbox", mailbox, False)
    message_id = get_int_from_term("message_id", message_id, False)

    body = acthex.environment().msg_body(connection_id, mailbox, message_id)
    if body != None:
        body = body.replace("\r\n", "\n")
        print("found " + '"'+str(body.replace("\\", "\\\\"))+'"')
        acthex.output(('"'+body+'"',))



def mailbox(connection_id, path, name):
    """
    Return each mailbox name in the given path, matching the given name.

    :param connection_id: term identifying the IMAP server connection
    :param path: string containing a path
    :param name: string containing a mailbox name
    :return:
    """

    print("called &mailbox("+ str(connection_id)+", "+ str(path)+", "+ str(name)+")")

    connection_id = get_term("connection_id", connection_id, False)
    path = get_string_from_term("path", path, False)
    name = get_string_from_term("name", name, False)

    mailboxes = acthex.environment().mailbox(connection_id, path, name)
    if mailboxes is not None:
        print("found mailboxes", end=" ")
        for mailbox in mailboxes:
            print('"'+str(mailbox)+'"' , end=" ")
            acthex.output(('"'+mailbox+'"', ))
        print()



def set_flag(connection_id, mailbox, message_id, flag):
    """
    Set or unset the given flag for the specified message.

    :param connection_id: term identifying the IMAP server connection
    :param mailbox: string containing a mailbox name
    :param message_id: integer representing the message ID
    :param flag: the name of the flag (without leading backslash) with a leading "not " iff the flag should be unset
    :return:
    """

    print("called @set_flag("+ str(connection_id)+", "+ str(mailbox)+", "+ str(message_id)+", "+ str(flag)+")")

    connection_id = get_term("connection_id", connection_id, True)
    mailbox = get_string_from_term("mailbox", mailbox, True)
    message_id = get_int_from_term("message_id", message_id, True)

    flag = get_string_from_term("flag", flag, True)
    flag = flag.split(" ")
    if len(flag) == 2 and flag[0] == "not":
        acthex.environment().set_flag(connection_id, mailbox, message_id, "\\" + flag[1], False)
    elif len(flag) == 1:
        acthex.environment().set_flag(connection_id, mailbox, message_id, "\\" + flag[0], True)
    else:
        print("Error: term flag of action atom set_flag is invalid", file=sys.stderr)
        return



def copy_msg(connection_id, mailbox, message_id, new_mailbox):
    """
    Copy the specified message to the specified mailbox.

    :param connection_id: term identifying the IMAP server connection
    :param mailbox: string containing a mailbox name
    :param message_id: integer representing the message ID
    :param new_mailbox: string containing a mailbox name
    :return:
    """

    print("called @copy_msg("+ str(connection_id)+", " +str(mailbox)+", " +str(message_id)+", " +str(new_mailbox)+")")

    connection_id = get_term("connection_id", connection_id, True)
    mailbox = get_string_from_term("mailbox", mailbox, True)
    message_id = get_int_from_term("message_id", message_id, True)
    new_mailbox = get_string_from_term("new_mailbox", new_mailbox, True)

    acthex.environment().copy_msg(connection_id, mailbox, message_id, new_mailbox)



def create_msg(connection_id, mailbox, sender, subject, recipients, ccs, bccs, text):
    """
    Create a message with the given sender, subject, recipients and text.

    :param connection_id: term identifying the IMAP server connection
    :param mailbox: string containing a mailbox name
    :param sender:
    :param subject:
    :param recipients:
    :param ccs:
    :param bccs:
    :param text:
    :return:
    """

    print("called @create_msg("+ str(connection_id)+", " +str(mailbox)+", "+ str(sender)+", "+ str(subject)+", "+ str(recipients)+", "+ str(ccs)+", "+ str(bccs)+", " +str(text)+")")

    connection_id = get_term("connection_id", connection_id, True)
    mailbox = get_string_from_term("mailbox", mailbox, True)
    sender = get_string_from_term("sender", sender, True)
    subject = get_string_from_term("subject", subject, True)
    recipients = get_list_from_function("to", recipients, True)
    ccs = get_list_from_function("cc", ccs, True)
    bccs = get_list_from_function("bcc", bccs, True)
    text = get_string_from_term("text", text, True)

    acthex.environment().create_msg(connection_id, mailbox, sender, subject, recipients, ccs, bccs, text)



def move_msg(connection_id, mailbox, message_id, new_mailbox):
    """
    Move the specified message to the specified mailbox.

    :param connection_id: term identifying the IMAP server connection
    :param mailbox: string containing a mailbox name
    :param message_id: integer representing the message ID
    :param new_mailbox: string containing a mailbox name
    :return:
    """

    print("called @move_msg("+ str(connection_id)+", " +str(mailbox)+", "+ str(message_id)+", "+ str(new_mailbox)+")")

    connection_id = get_term("connection_id", connection_id, True)
    mailbox = get_string_from_term("mailbox", mailbox, True)
    message_id = get_int_from_term("message_id", message_id, True)
    new_mailbox = get_string_from_term("new_mailbox", new_mailbox, True)

    acthex.environment().move_msg(connection_id, mailbox, message_id, new_mailbox)


def expunge_msgs(connection_id, mailbox):
    """
    Exunge all messages marked as deleted in the specified mailbox.

    :param connection_id: term identifying the IMAP server connection
    :param mailbox: string containing a mailbox name
    :return:
    """

    print("called @expunge_mailbox("+ str(connection_id)+", "+ str(mailbox)+")")

    connection_id = get_term("connection_id", connection_id, True)
    mailbox = get_string_from_term("mailbox", mailbox, True)

    acthex.environment().expunge_msgs(connection_id, mailbox)



def create_mailbox(connection_id, mailbox):
    """
    Create a new mailbox.

    :param connection_id: term identifying the IMAP server connection
    :param mailbox: string containing the name of the new mailbox
    :return:
    """

    print("called @create_mailbox("+ str(connection_id)+", "+ str(mailbox)+")")

    connection_id = get_term("connection_id", connection_id, True)
    mailbox = get_string_from_term("mailbox", mailbox, True)

    acthex.environment().create_mailbox(connection_id, mailbox)



def delete_mailbox(connection_id, mailbox):
    """
    Delete the specified mailbox.

    :param connection_id: term identifying the IMAP server connection
    :param mailbox: string containing the mailbox name
    :return:
    """

    print("called @delete_mailbox("+ str(connection_id)+", "+ str(mailbox)+")")

    connection_id = get_term("connection_id", connection_id, True)
    mailbox = get_string_from_term("mailbox", mailbox, True)

    acthex.environment().delete_mailbox(connection_id, mailbox)



def rename_mailbox(connection_id, mailbox, new_mailbox):
    """
    Rename the specified mailbox.

    :param connection_id: term identifying the IMAP server connection
    :param mailbox: string containing the mailbox name
    :param new_mailbox: string containing the new mailbox name
    :return:
    """

    print("called @rename_mailbox("+ str(connection_id)+", "+ str(mailbox)+", "+str(new_mailbox)+")")

    connection_id = get_term("connection_id", connection_id, True)
    mailbox = get_string_from_term("mailbox", mailbox, True)
    new_mailbox = get_string_from_term("new_mailbox", new_mailbox, True)

    acthex.environment().rename_mailbox(connection_id, mailbox, new_mailbox)



def reply(connection_id, mailbox, message_id, text):
    """
    Create a draft of a reply message to a specified message.

    :param connection_id: term identifying the IMAP server connection
    :param mailbox: string containing the mailbox name
    :param message_id: integer representing the message ID of the message to reply to
    :param text: string containing the text of the reply message
    :return:
    """

    print("called @reply("+ str(connection_id)+", "+ str(mailbox)+", " +str(message_id)+", "+ str(text)+")")

    connection_id = get_term("connection_id", connection_id, True)
    mailbox = get_string_from_term("mailbox", mailbox, True)
    message_id = get_int_from_term("message_id", message_id, True)
    text = get_string_from_term("text", text, True)

    acthex.environment().reply(connection_id, mailbox, message_id, text)



def register():
    acthex.setEnvironment(ImapEnvironment())

    acthex.addAction('login', (acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT))
    acthex.addAtom('logged_in', (acthex.CONSTANT,), 0)
    acthex.addAtom('filter', (acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT), 1)
    acthex.addAtom('msg_header', (acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT), 2)
    acthex.addAtom('msg_body', (acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT), 1)
    acthex.addAtom('mailbox', (acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT), 1)
    acthex.addAction('set_flag', (acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT))
    acthex.addAction('copy_msg', (acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT))
    acthex.addAction('create_msg', (acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT))
    acthex.addAction('move_msg', (acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT))
    acthex.addAction('expunge_msgs', (acthex.CONSTANT, acthex.CONSTANT))
    acthex.addAction('create_mailbox', (acthex.CONSTANT, acthex.CONSTANT))
    acthex.addAction('delete_mailbox', (acthex.CONSTANT, acthex.CONSTANT))
    acthex.addAction('rename_mailbox', (acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT))
    acthex.addAction('reply', (acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT, acthex.CONSTANT))



class ImapEnvironment(acthex.Environment):
    connections = []



    def login(self, id, host, port, user, password, ssl):
        for connection in self.connections:
            if connection.get_id() == id:
                connection.logout()
                self.connections.remove(connection)
                print("logged out from connection '" + id + "'")
                break

        self.connections.append(Connection(id, host, port, user, password, ssl))



    def logged_in(self, id):
        for connection in self.connections:
            if connection.get_id() == id:
                return True
        return False



    def filter(self, id, mailbox, filter):
        for connection in self.connections:
            if connection.get_id() == id:
                return connection.filter(mailbox, filter)



    def msg_header(self, id, mailbox, message_id):
        for connection in self.connections:
            if connection.get_id() == id:
                return connection.msg_header(mailbox, message_id)



    def msg_body(self, id, mailbox, message_id):
        for connection in self.connections:
            if connection.get_id() == id:
                return connection.msg_body(mailbox, message_id)



    def mailbox(self, id, path, name):
        for connection in self.connections:
            if connection.get_id() == id:
                return connection.mailbox(path, name)



    def set_flag(self, id, mailbox, message_id, flag, add):
        for connection in self.connections:
            if connection.get_id() == id:
                connection.set_flag(mailbox, message_id, flag, add)
                return
        print("Error: connection '" + id + "' not found", file=sys.stderr)



    def copy_msg(self, id, mailbox, message_id, new_mailbox):
        for connection in self.connections:
            if connection.get_id() == id:
                connection.copy_msg(mailbox, message_id, new_mailbox)
                return
        print("Error: connection '" + id + "' not found", file=sys.stderr)



    def create_msg(self, id, mailbox, sender, subject, recipients, ccs, bccs, text):
        for connection in self.connections:
            if connection.get_id() == id:
                connection.create_msg(mailbox, sender, subject, recipients, ccs, bccs, text)
                return
        print("Error: connection '" + id + "' not found", file=sys.stderr)



    def move_msg(self, id, mailbox, message_id, new_mailbox):
        for connection in self.connections:
            if connection.get_id() == id:
                connection.move_msg(mailbox, message_id, new_mailbox)
                return
        print("Error: connection '" + id + "' not found", file=sys.stderr)



    def expunge_msgs(self, id, mailbox):
        for connection in self.connections:
            if connection.get_id() == id:
                connection.expunge_msgs(mailbox)
                return
        print("Error: connection '" + id + "' not found", file=sys.stderr)



    def create_mailbox(self, id, mailbox):
        for connection in self.connections:
            if connection.get_id() == id:
                connection.create_mailbox(mailbox)
                return
        print("Error: connection '" + id + "' not found", file=sys.stderr)



    def delete_mailbox(self, id, mailbox):
        for connection in self.connections:
            if connection.get_id() == id:
                connection.delete_mailbox(mailbox)
                return
        print("Error: connection '" + id + "' not found", file=sys.stderr)



    def rename_mailbox(self, id, mailbox, new_mailbox):
        for connection in self.connections:
            if connection.get_id() == id:
                connection.rename_mailbox(mailbox, new_mailbox)
                return
        print("Error: connection '" + id + "' not found", file=sys.stderr)



    def reply(self, id, mailbox, message_id, text):
        for connection in self.connections:
            if connection.get_id() == id:
                connection.reply(mailbox, message_id, text)
                return
        print("Error: connection '" + id + "' not found", file=sys.stderr)



class Connection:
    __id = None
    __connection = None #type IMAP4 or IMAP4_SSL
    __user = None
    __selected_mailbox = None



    def __init__(self, id, host, port, user, password, ssl):
        self.__id = id
        self.__user = user

        try:
            if ssl: self.__connection = imaplib.IMAP4_SSL(host, port)
            else: self.__connection = imaplib.IMAP4(host, port)
        except:
            print("Error: connecting to server failed", file=sys.stderr)
            sys.exit(1)

        try:
            t, data = self.__connection.login(user, password)
        except:
            print("Error: login failed", file = sys.stderr)
            sys.exit(1)

        if t == "NO":
            print("Error: login failed", file = sys.stderr)
            sys.exit(1)

        print("established connection successfully")



    def get_id(self):
        return self.__id



    def logout(self):
        t,data = self.__connection.logout()
        if t != "BYE":
            print("Error: logout failed", file=sys.stderr)
            sys.exit(1)



    def select_mailbox(self, mailbox):
        if self.__selected_mailbox != mailbox:
            try:
                t, data = self.__connection.select('"'+mailbox+'"')

                if t == "NO":
                    print("Error: selecting mailbox failed", file=sys.stderr)
                    return False

                self.__selected_mailbox = mailbox

            except:
                print("Error: selecting mailbox failed", file=sys.stderr)
                return False

        return True



    def filter(self, mailbox, filter):
        if not self.select_mailbox(mailbox): return

        try:
            t, data = self.__connection.search(None, filter)

            if t == "NO":
                print("Error: searching for messages failed", file=sys.stderr)

            return data[0].decode().split()

        except:
            print("Error: searching for messages failed", file=sys.stderr)



    def msg_header(self, mailbox, message_id):
        if not self.select_mailbox(mailbox): return

        try:

            t, data = self.__connection.fetch(str(message_id), '(RFC822)')

            if t == "NO":
                print("Error: fetching message headers failed", file=sys.stderr)
                return

            try:
                msg = email.message_from_string(data[0][1].decode())
            except:
                print("Error: fetching message headers failed", file=sys.stderr)
                return

            return msg.items()

        except:
            print("Error: fetching message headers failed", file=sys.stderr)



    def msg_body(self, mailbox, message_id):
        if not self.select_mailbox(mailbox): return

        try:

            t, data = self.__connection.fetch(str(message_id), '(RFC822)')

            if t == "NO":
                print("Error: fetching message body failed", file=sys.stderr)
                return

            email_message = email.message_from_string(data[0][1].decode())

            for part in email_message.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload()

        except:
            print("Error: fetching message body failed", file=sys.stderr)



    def mailbox(self, path, name):
        try:
            t, data = self.__connection.list('"'+path+'"', '"'+name+'"')

            if t == "NO":
                print("Error: listing mailboxes failed", file=sys.stderr)
                return

            mailboxes = []

            if data == [None]: return mailboxes

            for m in data:
                print("got", m)

                try:
                    m = m.decode()
                except:
                    print("Error: unexpected IMAP server response", file=sys.stderr)
                    return

                if len(m) == 0:
                    print("Error: unexpected IMAP server response", file=sys.stderr)
                    return

                if m[-1] == '"':
                    m = m[:-1]
                    i = m[:-1].rfind('"')

                    if i == -1 or len(m) <= i+1:
                        print("Error: unexpected IMAP server response", file=sys.stderr)
                        return

                    mailboxes.append(m[i+1:])

                else:
                    m = m.split()

                    if len(m) == 0:
                        print("Error: unexpected IMAP server response", file=sys.stderr)
                        return

                    mailboxes.append(m[-1])

            return mailboxes

        except:
            print("Error: listing mailboxes failed", file=sys.stderr)
            return



    def set_flag(self, mailbox, message_id, flag, add):
        if not self.select_mailbox(mailbox): sys.exit(1)

        try:
            t, data = self.__connection.store(str(message_id), "+FLAGS" if add else "-FLAGS", flag)
            if t == "NO":
                print("Error: storing message flag failed", file=sys.stderr)
                sys.exit(1)

        except:
            print("Error: storing message flag failed", file=sys.stderr)
            sys.exit(1)



    def copy_msg(self, mailbox, message_id, new_mailbox):
        if not self.select_mailbox(mailbox): sys.exit(1)

        try:
            t, data = self.__connection.copy(str(message_id), new_mailbox)
            if t == "NO":
                print("Error: copying message failed", file=sys.stderr)
                sys.exit(1)

        except:
            print("Error: copying message failed", file=sys.stderr)
            sys.exit(1)



    def create_msg(self, mailbox, sender, subject, recipients, ccs, bccs, text):
        try:
            msg = email.message.Message()
            msg.add_header("From", sender)
            msg.add_header("Subject", subject)
            for recipient in recipients:
                msg.add_header("To", recipient)
            for cc in ccs:
                msg.add_header("Cc", cc)
            for bcc in bccs:
                msg.add_header("Bcc", bcc)
            msg.set_payload(text)

            t, data = self.__connection.append(mailbox, "", "", msg.as_string().encode())

            if t == "NO":
                print("Error: creating message failed", file=sys.stderr)
                sys.exit(1)

        except:
            print("Error: creating message failed", file = sys.stderr)
            sys.exit(1)



    def move_msg(self, mailbox, message_id, new_mailbox):

        if not self.select_mailbox(mailbox):
            sys.exit(1)

        try:

            t, data = self.__connection.copy(str(message_id), new_mailbox)
            if t == "NO":
                print("Error: moving message failed (message could not be copied)", file=sys.stderr)
                sys.exit(1)

            try:
                t, data = self.__connection.store(str(message_id), "+FLAGS", "\\Deleted")
                if t == "NO":
                    print("Error: moving message failed (message could be copied, but not deleted)", file=sys.stderr)
                    sys.exit(1)

            except:
                print("Error: moving message failed (message could be copied, but not deleted)", file=sys.stderr)
                sys.exit(1)

        except:
            print("Error: moving message failed (message could not be copied)", file=sys.stderr)
            sys.exit(1)



    def expunge_msgs(self, mailbox):
        if not self.select_mailbox(mailbox): sys.exit(1)

        try:
            t, data = self.__connection.expunge()

            if t == "NO":
                print("Error: expunging all messages failed", file=sys.stderr)
                sys.exit(1)

        except:
            print("Error: expunging all messages failed", file=sys.stderr)
            sys.exit(1)



    def create_mailbox(self, mailbox):
        try:
            t, data = self.__connection.create(mailbox)

            if t == "NO":
                print("Error: creating mailbox failed", file=sys.stderr)
                sys.exit(1)

        except:
            print("Error: creating mailbox failed", file=sys.stderr)
            sys.exit(1)



    def delete_mailbox(self, mailbox):
        try:
            t, data = self.__connection.delete(mailbox)

            if t == "NO":
                print("Error: deleting mailbox failed", file=sys.stderr)
                sys.exit(1)

        except:
            print("Error: deleting mailbox failed", file=sys.stderr)
            sys.exit(1)



    def rename_mailbox(self, mailbox, new_mailbox):
        try:
            t, data = self.__connection.rename(mailbox, new_mailbox)

            if t == "NO":
                print("Error: renaming mailbox failed", file=sys.stderr)
                sys.exit(1)

        except:
            print("Error: renaming mailbox failed", file=sys.stderr)
            sys.exit(1)



    def reply(self, mailbox, message_id, text):
        if not self.select_mailbox(mailbox): sys.exit(1)

        try:
            t, data = self.__connection.fetch(str(message_id), '(RFC822)')

            if t == "NO":
                print("Error: replying to message failed (fetching message headers failed)", file=sys.stderr)
                sys.exit(1)

            headers = email.message_from_string(data[0][1].decode()).items()

            try:
                sender = None
                subject = None
                recipients = []
                ccs = []
                bccs = []

                for (type, value) in headers:
                    if type == "From": sender = value
                    elif type == "Subject": subject = value
                    elif type == "To": recipients.append(value)
                    elif type == "Cc": ccs.append(value)
                    elif type == "Bcc": bccs.append(value)

                msg = email.message.Message()
                if sender is not None: msg.add_header("To", sender)
                if self.__user is not None: msg.add_header("From", self.__user)
                if subject is not None: msg.add_header("Subject", "Re: " + subject)
                for recipient in recipients:
                    if recipient != self.__user:
                        msg.add_header("Cc", recipient)
                for cc in ccs:
                    msg.add_header("Cc", cc)
                for bcc in bccs:
                    msg.add_header("Bcc", bcc)
                msg.set_payload(text)

                t, data = self.__connection.append(mailbox, "\Draft", "", msg.as_string().encode())

                if t == "NO":
                    print("Error: replying to message failed (creating message failed)", file=sys.stderr)
                    sys.exit(1)
            except:
                print("Error: replying to message failed (creating message failed)", file = sys.stderr)
                sys.exit(1)

        except:
            print("Error: replying to message failed (fetching message headers failed)", file=sys.stderr)
            sys.exit(1)



def get_term(term_name, term, isAction):
    """
    Check the given term and return its string value.
    If the given term is invalid, an error message is printed and if isAction is True, the evaluation of the acthex program is aborted.

    :param term_name: string containing an identifier for the given term. (Required for error message)
    :param term:
    :param isAction:
    :return:
    """

    if term is None:
        print("Error: term " + str(term_name) +" is 'None'", file=sys.stderr)
        if isAction: sys.exit(1)
        return

    if type(term.value()) is not str:
        print("Error: term " + str(term_name) + " is not a string", file=sys.stderr)
        if isAction: sys.exit(1)
        return

    if len(term.value()) < 1:
        print("Error: term " + str(term_name) + " is too short. (expected a term of length >= 1, but was '" + str(term.value()) + "'", file=sys.stderr)
        if isAction: sys.exit(1)
        return

    return term.value()



def get_string_from_term(term_name, term, isAction):
    """
    Check if the given term is a valid string (i.e. if it is in double quotes) and return its string value (without quotes).
    If the given term is invalid, an error message is printed and if isAction is True, the evaluation of the acthex program is aborted.

    :param term_name: string containing an identifier for the given term. (Required for error message)
    :param term:
    :param isAction:
    :return:
    """

    term = get_term(term_name, term, isAction)

    if len(term) < 2:
        print("Error: term " +  str(term_name) + " is too short (expected a term of length >= 2, but was '" +  str(term) + "')", file=sys.stderr)
        if isAction: sys.exit(1)
        return

    if term[0] != '"':
        print("Error: term " +  str(term_name) + " is invalid (expected to begin with \", but was '" + str( term) + "')", file=sys.stderr)
        if isAction: sys.exit(1)
        return

    if term[-1] != '"':
        print("Error: term " +  str(term_name) + " is invalid (expected to end with \", but was '" +  str(term) + "')", file=sys.stderr)
        if isAction: sys.exit(1)
        return

    return term[1:-1]



def get_int_from_term(term_name, term, isAction):
    """
    Check if the given term is a valid integer and return its integer value.
    If the given term is invalid, an error message is printed and if isAction is True, the evaluation of the acthex program is aborted.

    :param term_name: string containing an identifier for the given term. (Required for error message)
    :param term:
    :param isAction:
    :return:
    """

    term = get_term(term_name, term, isAction)

    try:
        return int(term)
    except ValueError:
        print("Error: term " +  str(term_name) + " is invalid (expected an integer, but was '" +  str(term )+ "')", file=sys.stderr)
        if isAction: sys.exit(1)
        return



def get_list_from_function(expected_function_name, function, isAction):
    """
    Check if the given term is a valid function of form f(x1, x2, ...), where f is the expected function name, and return its terms x1, x2, ... as a list
    If the given term is invalid, an error message is printed and if isAction is True, the evaluation of the acthex program is aborted.

    :param expected_function_name:
    :param function:
    :param isAction:
    :return:
    """

    function = get_term(expected_function_name, function, True)

    if function == expected_function_name: # 0-ary function
        return []

    try:
        function_name = function[:function.index("(")]

        if function_name != expected_function_name:
            print("Error: function name of function " +  str(function) + " is invalid (expected '" +  str(expected_function_name) + "', but was '" +  str(function_name )+ "')", file=sys.stderr)
            if isAction: sys.exit(1)

        if function[-1] != ")":
            print("Error: function " +  str(function) + " is invalid", file=sys.stderr)
            if isAction: sys.exit(1)

        list = []
        i = len(function_name) + 1

        while i < len(function)-1:

            if function[i] == '"':
                list.append(function[(i+1):i+1+(function[(i+1):].index('"'))])
                i = i+1+function[(i+1):].index('"') + 2

            else:

                list.append(function[(i+1):i+1+function[(i+1):].index(',')-1])
                i = i+1+function[(i+1):].index(',') + 1

        return list

    except:
        print("Error: function " +  str(function) + " is invalid", file=sys.stderr)
        if isAction: sys.exit(1)
