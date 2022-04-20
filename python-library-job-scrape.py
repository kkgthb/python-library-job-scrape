import re
from bs4 import BeautifulSoup
import requests

# Define a variable for what search phrase we'll be looking for in pages we visit
find_me = 'librar'
# Define a variable with nicknames & URLs of pages we plan to visit
job_pages = {
    'uni_nyu': 'https://careers-nyu.icims.com/jobs/search?mode=redo&pr=0&schemaId=%24T%7BJob%7D.%24T%7BJobPost%7D.%24F%7BPostedDateTime%7D&o=A&searchKeyword='+find_me+'*&searchRelation=keyword_all',
    'uni_nymc': 'https://nymccareers-touro.icims.com/jobs/search?mode=redo&pr=0&schemaId=%24T%7BJob%7D.%24T%7BJobPost%7D.%24F%7BPostedDateTime%7D&o=A&searchKeyword='+find_me+'*&searchRelation=keyword_all',
    'k12_yonk': 'https://careers.yonkerspublicschools.org/perl/cart/cart?search='+find_me+'&job_type=&type=&action=Search'
}
# Define a "regex" text-searching pattern for " a few words around wherever the keyword of interest shows up"
find_me_regex = re.compile(find_me, re.I)
find_me_with_padding_regex = re.compile(r'.{0,30}' + find_me + r'.{0,30}', re.I)

def parse_job_page(job_pages_key, job_pages_value):
    http_response = requests.get(job_pages_value)
    html_data = http_response.text
    parsed_html = BeautifulSoup(html_data, 'html.parser')
    # Reset things from the last loop
    search_results = []
    # Look through the text on the page for the keyword of interest
    search_results = parsed_html.body.findAll(find_me_regex) # Data type of each member of this list:  https://tedboy.github.io/bs4_doc/generated/generated/bs4.NavigableString.html
    # I can't figure out why, but some pages don't seem to work so well and this seems to help
    if (len(search_results) == 0): 
        body_stripped = ''.join(line.strip() for line in parsed_html.body.text.split("\n"))
        search_results = find_me_with_padding_regex.findall(body_stripped)
    print(job_pages_key + ':  Found ' + str(len(search_results)) + ' in-page case-insensitive occurrences of "' + find_me + '".')
    # Display snippets from any interesting finds
    if len(search_results) > 0:
        print('Check it out!  ' + job_pages_value)
        for search_result_counter, search_result in enumerate(search_results, start=1):
            print('In-page search result #' + str(search_result_counter))
            search_result_snippets = find_me_with_padding_regex.findall(search_result)
            for snippet_counter, snippet in enumerate(search_result_snippets, start=1):
                print('Snippet #' + str(snippet_counter) + '( search result #' + str(search_result_counter) + '):')
                print(snippet)
        print('Check it out!  ' + job_pages_value)
    # Lots of educational instutions (a common place with libraries) use ICIMS, which puts the jobs in an IFrame.
    first_iframe = parsed_html.find('iframe')
    if first_iframe is not None:
        iframe_src = first_iframe.attrs['src']
        if iframe_src is not None:
            iframe_http_response = requests.get(iframe_src)
            iframe_html_data = iframe_http_response.text
            iframe_parsed_html = BeautifulSoup(iframe_html_data, 'html.parser')
            # Reset things from the last loop
            iframe_search_results = []
            # Look through the text on the page for the keyword of interest
            iframe_search_results = iframe_parsed_html.body.findAll(text=find_me_regex) # Data type of each member of this list:  https://tedboy.github.io/bs4_doc/generated/generated/bs4.NavigableString.html)
            # I can't figure out why, but some pages don't seem to work so well and this seems to help
            if (len(iframe_search_results) == 0):
                iframe_body_stripped = ''.join(line.strip() for line in iframe_parsed_html.body.text.split("\n"))
                iframe_search_results = find_me_with_padding_regex.findall(iframe_body_stripped)
            print('  ' + job_pages_key + ' IFRAME:  Found ' + str(len(iframe_search_results)) + ' in-page case-insensitive occurrences of "' + find_me + '".')
            # Display snippets from any interesting finds
            if len(iframe_search_results) > 0:
                print('Check it out!  ' + job_pages_value)
                for iframe_search_result_counter, iframe_search_result in enumerate(iframe_search_results, start=1):
                    print('IFrame in-page search result #' + str(iframe_search_result_counter))
                    iframe_search_result_snippets = find_me_with_padding_regex.findall(iframe_search_result)
                    for iframe_snippet_counter, iframe_snippet in enumerate(iframe_search_result_snippets, start=1):
                        print('IFrame snippet #' + str(iframe_snippet_counter) + '( search result #' + str(iframe_search_result_counter) + '):')
                        print(iframe_snippet)
                print('Check it out!  ' + job_pages_value)
    print()
    

for k,v in job_pages.items():
    parse_job_page(k,v)
