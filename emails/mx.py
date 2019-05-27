# sudo pip install dnspython
import dns.resolver

whitelist = 'gmail.com googlemail.com hotmail.com hotmail.co.uk hotmail.fr hotmail.it outlook.com live.com live.co.uk live.de live.ie yahoo.com yahoo.co.uk yahoo.es yahoo.fr aol.com gmx.com gmx.de sky.com bt.com btinternet.com ntlworld.com talktalk.net interia.pl wp.pl seznam.cz'


def check_mx(email):
    """Validate email domain by checking MX records

    Domains on the whitelist are valid without checking.
    """
    if '@' not in email:
        return
    domain = email.split('@')[-1]
    if domain in whitelist.split():
        return True

    resolver = dns.resolver.Resolver()
    resolver.lifetime = 0.5
    for x in resolver.query(domain, 'MX'):
        # print x.to_text()
        return True

    return
