### @export "imports"
from libs.utils import *
tracking = open('tracking.txt', 'w')

### @export "set-blog-url"
BLOG_URL = "http://biolab.isis.rl.ac.uk/camerons_labblog"
FROM_DATE = datetime.datetime.strptime('2011-03-01', '%Y-%m-%d')
TO_DATE = datetime.datetime.strptime('2011-06-01', '%Y-%m-%d')

### @export "retrieving-data-pages"
saxs_data_posts = getposts(BLOG_URL, "DATA_TYPE", "SAXS_Diamond",
                             FROM_DATE, TO_DATE) 
numposts = str(len(saxs_data_posts))
tracking.write("""\n### @export "number-data-posts"\n%s""" % numposts)

sas_patterns = []
name_mapping = {}
for data_post in saxs_data_posts:
    sas_data_object = get_data(data_post)
    sas_patterns.append(sas_data_object)
    name_mapping(sas_data_object.get_id()) = len(sas_patterns)

