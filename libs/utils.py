### @export "imports"
from sas import *
from proxy import *
from numpy import *
import urllib2
import urllib
from xml.etree import ElementTree as ET



### @export "test-proxy"
#if set_proxy(False):
#    pass
#else:
#    set_proxy(True)

### @export "get-post-list"
def getposts(blogurl, key, value, from_date, to_date):
    """Obtain list of posts matching key=key and value=value"""

    ### @export "gpl-construct-url"
    requesturl = blogurl + '/meta/' + key + '/value/' + value + '/index.xml'

    response = urllib2.urlopen(requesturl)

    ### @export "gpl-parse-post-list"
    try:
        parsedresponse = ET.parse(response)
    except URLError:
        return []

    postlist = []
    posts = parsedresponse.getiterator('post')
    for post in posts:
        post_date = datetime.datetime.strptime(
                post.find('datestamp').text[0:10], '%Y-%m-%d')
        
        if post_date > from_date and post_date < to_date:
            postlist.append(post.find('formats').findall('format')[1].text)

    return postlist

### @export "get-data-from-post"
def get_data(posturl):
    """Recovers .DAT or CanSAS XML files given a blog data post URL"""

    response = urllib2.urlopen(posturl)
    parsedresponse = ET.parse(response)

    ### @export "gdfp-obtain-data-container-link"
    dataurllist = parsedresponse.find('post').find(
        'attached_data').getiterator('data')

    ### @export "gdfp-data-download-link"
    for dataurl in dataurllist:
        filepost = urllib2.urlopen(dataurl.text)
        parsedfilepost = ET.parse(filepost)
        fileurl = parsedfilepost.find('dataitems'
                                      ).findall('dataitem')[0].text
    ### @export "gdfp-data-to-SASData"
    datafile = urllib2.urlopen(fileurl).readlines()

    data = loadtxt(datafile, skiprows=3)
    data_q = data[:,0]
    data_i = data[:,1]

    sas_data = ExpSasData(data_q, data_i)

