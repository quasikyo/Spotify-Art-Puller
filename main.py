import package_handler

REQUIRMENTS_FILE = 'requirements.txt'


if __name__ == '__main__':
	packages = package_handler.get_missing_packages(REQUIRMENTS_FILE)
	if len(packages) > 0:
		package_handler.prompt_package_install(packages)
	# auth
	# get artist and album
	# search for hit in spotify
	# download/resize image
	pass
