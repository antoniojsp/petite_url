import urllib.request


def check_url_alive(url: str) -> bool:
	try:
		result = urllib.request.urlopen(url).getcode() == 200
	except (urllib.error.URLError, ValueError) as error:
		result = False

	return result


