import re
import requests
import logging
from lxml import html


username = 'bookhoarder'  # Funsubstance username
search_key = 'lovorn|kik|lime|group'  # A term(s) in regexp form to search for in comments

page_id = ''

while True:
	if page_id == '':
		uri = 'http://funsubstance.com/{0}/comments/{1}'.format(username, page_id)
	else:
		uri = 'http://funsubstance.com/{0}/comments/next/{1}'.format(username, page_id)
	
	page = requests.get(uri)
	# logging.info('Searching page: %s', uri)
	# print('Searching page: {0}'.format(uri))

	tree = html.fromstring(page.content)

	comments = tree.xpath('//div[@class="comment-content"]/text()')

	# Go through the comments on each page and see if search_key is found
	for comment in comments:
		if re.search(search_key, comment, re.IGNORECASE):
			# logging.info('Page ID: %s; URI: %s; Comment: %s', page_id, uri, comment)
			print('URI: {1};\nComment: {2}'.format(page_id, uri, comment))

	# Try to obtain the next page ID to navigate to later
	try:
		page_id = tree.xpath('//div[@class="pager"]/a[contains(@href, "next")]')
		page_id = page_id[0]
		page_id = page_id.get('href').split('/')[4]
	except:
		# The next page ID was not found so probably the last page
		print('Search reached last page...')
		break
