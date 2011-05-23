# Record of using sas.py to process data from SM6717-1

# Outline

We collected data on I22 in mid-May on a range of SMALPs and this data was uploaded to the lab notebook system at http://biolab.isis.rl.ac.uk The aim here is to record the process of grabbing data from the notebook and processing it using some Python scripts.

# Getting the data post URLs

First we set a general blog URL and a date range to get data for.

{{ d['processing.py|idio']['set-blog-url'] }}

For this experiment I need to get I22 SAXS data files. The key is DATA_TYPE and the value is SAXS_Diamond.

{{ d['processing.py|idio']['retrieving-data-pages'] }}

There are {{ d['libs/howmanydataposts.py|py'] }} data files found between the dates set.

<-- TODO Get this figure automatically -->

