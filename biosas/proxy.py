import urllib2

def set_proxy(boolean, proxy = 'ral'):
    """Method for setting up proxy arrangements

    Default proxy is currently for RAL which is one of the few
    places where this will actually be needed.
    """

    assert type(boolean) == bool, 'Allowed arguments are True and False'

    proxies = {'none': {},
               'ral' : {'http' : 'http://wwwcache.rl.ac.uk:8080'}
              }

    if boolean == True:
        # If the method is called to setup proxies
        # Setup proxy handler and then install an opener for use
        assert proxy in proxies, 'No information for that proxy'
        proxy_support = urllib2.ProxyHandler(proxies[proxy])
        urllib2.install_opener(urllib2.build_opener(proxy_support))

    elif boolean == False:
        # If the method is called to remove proxies 
        # Set up as empty
        proxy_support = urllib2.ProxyHandler(proxies['none'])
        urllib2.install_opener(urllib2.build_opener(proxy_support))
        
    try:
        f = urllib2.urlopen('http://google.com')
        assert f.read(21) == '<!doctype html><html>'
        return True

    except urllib2.URLError:
        return False
