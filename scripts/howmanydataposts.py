from biosas.utils import *

### @export "set-blog-url"
BLOG_URL = "http://biolab.isis.rl.ac.uk/camerons_labblog"
FROM_DATE = datetime.datetime.strptime('2011-03-01', '%Y-%m-%d')
TO_DATE = datetime.datetime.strptime('2011-06-01', '%Y-%m-%d')

### @export "retrieving-data-pages"
saxs_data_list = getposts(BLOG_URL, "DATA_TYPE", "SAXS_Diamond",
                             FROM_DATE, TO_DATE) 

print len(saxs_data_list)

