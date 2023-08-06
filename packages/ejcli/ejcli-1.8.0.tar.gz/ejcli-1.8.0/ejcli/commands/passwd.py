import ejcli.http, getpass, ejcli.error

def do_passwd(self, cmd):
    """
    usage: passwd

    Change contest login password.
    """
    if cmd.strip():
        return self.do_help('passwd')
    oldpass = getpass.getpass('Old password: ')
    newpass = getpass.getpass('New password: ')
    newpass2 = getpass.getpass('Retype new password: ')
    if newpass != newpass2:
        raise ejcli.error.EJError('Passwords do not match!')
    ejcli.http.change_password(self.url, self.cookie, oldpass, newpass)
    print('Password changed successfully, now relogin.')
    self.url = self.cookie = None
