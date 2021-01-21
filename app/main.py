import os
import sys
import time
import random

import vk_api
import colorama

colorama.init()

"""
Tools
"""
def show():
	AUTHOR = "\033[35m[*]\033[0m Made by Moonquit (github.com)"
	HOW_STOP = '\033[31m[*]\033[0m Press "CTRL + C" or "CTRL + Z" to exit'
	print(
		"""
         ____________________________________________
        |____________________________________________|

          {}
          {}
         ____________________________________________
        |____________________________________________|

        """.format(AUTHOR, HOW_STOP)
    )

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

"""
VK Tools
"""
def read_dialogs(api, dialogs):
	log()
	log("Reading the dialogs...")
	count_dialogs = len(dialogs)
	count_read = 0

	for peer in dialogs:
		api.messages.markAsRead(peer_id=peer, mark_conversation_as_read=1)
		count_read +=1
		log_ok(f"Read [{count_read}/{count_dialogs}] -> link: https://vk.com/write{peer}")
		time.sleep(random.random())
	log_ok("Done!")

def get_dialogs(api):
	log()
	log("Getting the dialogs...")
	dialogs = []
	count = api.messages.getConversations(count=0)["count"]

	for offset in range((count - 1) // 200 + 1):
		peers = api.messages.getConversations(count=200, offset=offset * 200, filter="unread")

		for item in peers["items"]:
			dialogs.append(item["conversation"]["peer"]["id"])

	log_ok(f"Received {len(dialogs)} unread dialogs! Press any key to start read...")
	wait_click()
	return dialogs

def check_token(token):
	check = False
	api = vk_api.VkApi(token=token)
	api = api.get_api()

	try:
		info = api.users.get()
		log()
		log_ok("Account: {} {}. Press any key to continue...".format(
			info[0]["first_name"],
			info[0]["last_name"]
			)
		)
		wait_click() 
		check = True
	except vk_api.exceptions.VkApiError as err:
		if err.code == 5:
			log_error("Invalid token passed")
		else:
			log_error(err)
		log()
	return check

def main():
	show()
	while True:
		log("Enter the API token:")
		inp = input("> ").strip()
		if check_token(inp):
			break

	api = vk_api.VkApi(token=inp)
	api = api.get_api()

	read_dialogs(
		api=api,
		dialogs=get_dialogs(api)
	)

	log()
	log("Press any key to exit...")
	wait_click()
	exit()


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		log()
		log("Stopped!")