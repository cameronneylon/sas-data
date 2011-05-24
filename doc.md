# Record of using sas.py to process data from SM6717-1

# Outline

We collected data on I22 in mid-May on a range of SMALPs and this data was uploaded to the lab notebook system at http://biolab.isis.rl.ac.uk The aim here is to record the process of grabbing data from the notebook and processing it using some Python scripts.

# Getting the data post URLs

First we set a general blog URL and a date range to get data for.

{{ d['processing.py|idio']['set-blog-url'] }}

For this experiment I need to get I22 SAXS data files. The key is DATA_TYPE and the value is SAXS_Diamond.

{{ d['processing.py|idio']['retrieving-data-pages'] }}

There are {{ d['tracking.txt|idio']['number-data-posts'] }} data files found between the dates set. Which are named:

{{ d['tracking.txt|idio']['post-list'] }}

Of these "I22 29554 - buffer", "I22 29561 - Buffer", and "I22 29591 BUFFER" are the buffer runs. The first of these was for a shorter collection time as are the runs up to 29558 according to the [run record for the first set of samples](http://biolab.isis.rl.ac.uk/camerons_labblog/14220/SAXS_on_SMALP_samples_1.html). 

The sample runs from 29560 to 29565 should have the buffer run 29561 subtracted.

{{ d['processing.py|idio']['first-set-subtractions'] }}

The second set of runs are handled similarly

{{ d['processing.py|idio']['second-set-subtractions'] }}

Here is a graph

<img src="../artifacts/test.png"> 