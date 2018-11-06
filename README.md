# IMAP Plugin for ACTHEX

This a plugin for interacting with IMAP servers from ACTHEX.
It partially implements the client-side of the Internet Message Access Protocol (IMAP)
to allow the integration of email messages into ACTHEX programs.

## Usage

The IMAP plugin can be used like any other plugin for ACTHEX.
E.g. to use it with HEXLite's ACTHEX implementation, you can run  
```
acthex --plugin imapplugin ACTHEXFILE
```

## Testing

To run the tests, provided in tests/testcases, Dovecot needs to be installed locally and configured to be reachable at localhost:10143 and run without root privileges.
In the following, a brief instruction, on how to install Dovecot, is given:

*  Download Dovecot sources (e.g. v2.2.36 from https://dovecot.org/releases/2.2/dovecot-2.2.36.tar.gz).

*  Install Dovecot:
        
        ./configure --prefix=[PREFIX]/dovecot
        make
        make install

*  Copy the tests/dovecot.conf to [PREFIX]/dovecot/etc/dovecot/ and
    *  replace each occurrence of [PREFIX] in [PREFIX]/dovecot/etc/dovecot/dovecot.conf with the actual prefix and
    *  replace each occurrence of [USER] in [PREFIX]/dovecot/etc/dovecot/dovecot.conf with your user name.
*  OR follow the instructions provided at https://wiki.dovecot.org/HowTo/Rootless

Once Dovecot is installed, the tests can be run inside the repository with  
```
python tests/runtests.py [PREFIX]/dovecot
```