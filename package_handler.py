import subprocess
import sys


def _parse_packages(version_list: list[str]) -> dict:
	return { package.split('==')[0] for package in version_list }


def _install_packages(packages: set[str]) -> None:
	command_args = [sys.executable, '-m', 'pip', 'install', *packages]
	print(f'Attempting command: {" ".join(command_args)}')
	code = subprocess.call(command_args)
	if code != 0:
		print(f'The command failed with exit code {code}', file=sys.stderr)
		sys.exit(1)


def get_missing_packages(requirements_file: str) -> bool:
	required_packages = None
	with open(requirements_file, 'r') as file:
		contents = file.read()
		required_packages = _parse_packages(contents.splitlines())

	pip_output = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).splitlines()
	installed_packages = _parse_packages([as_bytes.decode('utf-8') for as_bytes in pip_output])

	missing_packages = required_packages.difference(installed_packages)
	return missing_packages


def prompt_package_install(packages: set[str]) -> None:
	print(f'Found the following missing packages: {packages}')
	while True:
		match input('Install (y/n)? ').lower():
			case 'y':
				_install_packages(packages)
				break
			case 'n':
				print('Must install the missing packages to proceed. Exiting...')
				sys.exit(0)
			case _:
				print('Invalid input. Re-prompting...')
