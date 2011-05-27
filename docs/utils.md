# Utility methods for retrieving Data from SAS experiments from the LaBLog

# Outline

Utility methods for collecting SAS data data from the blog 

# Getting the data post URLs

I'm re-using some of the code that I used to generate the structured data from tables. The method grabs a list of posts that match a key value pair. The method takes a main blog URL, the key and the value desired.

{{ d['biosas/utils.py|idio']['get-post-list'] }}

A request URL is then constructed and called.

{{ d['biosas/utils.py|idio']['gpl-construct-url'] }}

The returned page of XML is then parsed using ElementTree (inside a try clause) and a list of posts is generated and returned checking against the dates that were set.

{{ d['biosas/utils.py|idio']['gpl-parse-post-list'] }}

# Getting the data from the data posts

We still now need to go through to the data posts and then get the actual data file as a stream. The method to do this takes a URL for ad at a post, opens up the post XML and parses the response.

{{ d['biosas/utils.py|idio']['get-data-from-post'] }}

We then need to find the link to the actual data object container. There can be multiple data containers in each post. For the current set of I22 data there is only one to worry about.

{{ d['biosas/utils.py|idio']['gdfp-obtain-data-container-link'] }}

The data container then has to be read to find the actual download link

{{ d['biosas/utils.py|idio']['gdfp-data-download-link'] }}

With the fileurl in hand we can finally obtain the data and create a SASData object.


