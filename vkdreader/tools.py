import sys, os

def wait_click():
    result = None
    if os.name == 'nt':
        import msvcrt
        result = msvcrt.getch()
    else:
        import termios
        fd = sys.stdin.fileno()

        oldterm = termios.tcgetattr(fd)
        newattr = termios.tcgetattr(fd)
        newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
        termios.tcsetattr(fd, termios.TCSANOW, newattr)

        try:
            result = sys.stdin.read(1)
        except IOError:
            pass
        finally:
            termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)

    return result

def log_ok(text):
	print("[\033[32m*\033[0m] {}".format(str(text)))

def log_error(text):
	print("[\033[31merror\033[0m] {}".format(str(text)))

def log(text = None):
	if text:
		print(f"[\033[34m*\033[0m] {text}")
	else:
		print()