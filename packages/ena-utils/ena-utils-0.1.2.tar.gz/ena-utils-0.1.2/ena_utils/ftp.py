import os
import sys
import glob
import ftplib

class FtpConnect(object):

    def __init__(self, user, password, host):
        """FTP connection."""
        self.user = user
        self.password = password
        self.host = host

    def mput(self, local, verbose = True):
        """Upload multiple files using ftp."""

        n = 0
        summary = ''
        try:
            for path in glob.glob(local):
                with ftplib.FTP(self.host, self.user, self.password) as ftp, open(path, 'rb') as f:
                    response = ftp.storbinary('STOR ' + os.path.basename(path), f)
                n += 1
                summary = summary + 'Copied: ' + os.path.basename(path) + ' to ' + self.host + '\n'
            if verbose:
                print(summary + str(n) + ' file/s copied \n' + response)
            return 0
        except Exception as e:
            print('Error: ' + str(e))
            return 1