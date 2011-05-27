### @export "imports"
from biosas.utils import *
import json

tracking = {} # change this to 'info' or 'run_info' maybe?

### @export "set-blog-url"
BLOG_URL = "http://biolab.isis.rl.ac.uk/camerons_labblog"
FROM_DATE_STRING = "2011-03-01"
TO_DATE_STRING = "2011-06-01"

def parse_date(date_string):
    return datetime.datetime.strptime(date_string, '%Y-%m-%d')

from_date = parse_date(FROM_DATE_STRING)
to_date = parse_date(TO_DATE_STRING)

tracking['blog-url'] = BLOG_URL
tracking['from-date'] = FROM_DATE_STRING
tracking['to-date'] = TO_DATE_STRING

### @export "retrieving-data-pages"
saxs_data_posts = getposts(BLOG_URL, "DATA_TYPE", "SAXS_Diamond",
                             from_date, to_date)
### @export end

numposts = len(saxs_data_posts)
tracking['num-posts'] = numposts

sas_patterns = []
name_mapping = {}
post_list = []
for data_post in saxs_data_posts:
    sas_data_object = get_data(data_post)
    sas_patterns.append(sas_data_object)
    name = sas_data_object.get_id()
    name_mapping[name] = len(sas_patterns)-1
    post_list.append(name)

tracking['post-list'] = post_list

### @export "first-set-subtractions"
subtracted_data = []
list1 = ['I22 29560 - b4', 'I22 29562 - b3', 'I22 29564 - b2',
               'I22 29565 - b1']

background = 'I22 29561 - buffer'

for data in list1:
    subtracted = sas_patterns[name_mapping[data]] - sas_patterns[
                                           name_mapping[background]]
    subtracted_data.append(subtracted)

### @export "second-set-subtractions"
list2 = ['I22 29574 - A3 - seems ok',
'I22 29575 - a2',
'I22 29576 - a1',
'I22 29577 - mono-olein',
'I22 29578 - DMPC',
'I22 29579 - b9',
'I22 29580 - b8',
'I22 29581 - b7',
'I22 29582 - b6',
'I22 29583 - b5',
'I22 29584-DLPC',
'I22 29585 - A9',
'I22 29586 A8',
'I22 29587 A7',
'I22 29588 - A6',
'I22 29589 - A5',
'I22 29590 - A4']

background = 'I22 29591 BUFFER'

for data in list2:
    subtracted = sas_patterns[name_mapping[data]] - sas_patterns[
                                           name_mapping[background]]
    subtracted_data.append(subtracted)

### @export "plotting-curve"
test = SasPlot(subtracted_data[0])
test.guinier_plot()
test.ax.set_ybound(0.01)
test.ax.set_xbound(0.01, 0.05)
test.canvas.print_figure("dexy--test.png")

### @export "save-tracking-data"
tracking_file = open("dexy--tracking.json", "w")
json.dump(tracking, tracking_file)
tracking_file.close()

