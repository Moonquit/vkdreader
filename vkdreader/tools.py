import msvcrt

def wait_click():
	msvcrt.getch()

def log_ok(text):
	print("[\033[32m*\033[0m] {}".format(str(text)))

def log_error(text):
	print("[\033[31merror\033[0m] {}".format(str(text)))

def log(text = None):
	if text:
		print(f"[\033[34m*\033[0m] {text}")
	else:
		print()