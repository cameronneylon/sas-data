### @export "imports"
from biosas.utils import *
tracking = open('dexy--tracking.txt', 'w')

### @export "set-blog-url"
BLOG_URL = "http://biolab.isis.rl.ac.uk/camerons_labblog"
FROM_DATE = datetime.datetime.strptime('2011-03-01', '%Y-%m-%d')
TO_DATE = datetime.datetime.strptime('2011-06-01', '%Y-%m-%d')

### @export "retrieving-data-pages"
saxs_data_posts = getposts(BLOG_URL, "DATA_TYPE", "SAXS_Diamond",
                             FROM_DATE, TO_DATE) 
### @export end

numposts = str(len(saxs_data_posts))
tracking.write("""\n### @export "number-data-posts"\n%s""" % numposts)

sas_patterns = []
name_mapping = {}
tracking.write("""\n### @export "post-list"\n""")
for data_post in saxs_data_posts:
    sas_data_object = get_data(data_post)
    sas_patterns.append(sas_data_object)
    name = sas_data_object.get_id()
    name_mapping[name] = len(sas_patterns)-1
    tracking.write("""%s, """ % name)

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

tracking.close()

