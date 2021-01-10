import os
import time
import random

import vkdreader.tools as tools
import vkdreader.preview as preview

preview.show()

try:
	import vk_api
except ImportError:
	tools.log_error("Module <vk_api> not found! Press any key to install...")
	tools.log()
	tools.wait_click()

	code = "python3 -m pip install vk_api"
	if os.name == "nt":
		code = "python -m pip install vk_api"
	os.system(code)
	
	tools.log()
	tools.log_ok("The module successfully installed! Restart the program")
	tools.log("Press any key to exit...")
	tools.wait_click()
	exit()

def read_dialogs(api, dialogs):
	tools.log()
	tools.log("Reading the dialogs...")
	count_dialogs = len(dialogs)
	count_read = 0

	for peer in dialogs:
		api.messages.markAsRead(peer_id=peer, mark_conversation_as_read=1)
		count_read +=1
		tools.log_ok(f"Read [{count_read}/{count_dialogs}] -> link: https://vk.com/write{peer}")
		time.sleep(random.random())
	tools.log_ok("Done!")

def get_dialogs(api):
	tools.log()
	tools.log("Getting the dialogs...")
	dialogs = []
	count = api.messages.getConversations(count=0)["count"]

	for offset in range((count - 1) // 200 + 1):
		peers = api.messages.getConversations(count=200, offset=offset * 200, filter="unread")

		for item in peers["items"]:
			dialogs.append(item["conversation"]["peer"]["id"])

	tools.log_ok(f"Received {len(dialogs)} dialogs! Press any key to continue...")
	tools.wait_click()
	return dialogs

def check_token(token):
	check = False
	api = vk_api.VkApi(token=token)
	api = api.get_api()

	try:
		info = api.users.get()
		tools.log()
		tools.log_ok("Account: {} {}. Press any key to continue...".format(
			info[0]["first_name"],
			info[0]["last_name"]
			)
		)
		tools.wait_click() 
		check = True
	except vk_api.exceptions.VkApiError as err:
		if err.code == 5:
			tools.log_error("Invalid token passed")
		else:
			tools.log_error(err)
		tools.log()
	return check

def main():
	while True:
		inp = input("[\033[34m*\033[0m] Enter the API token: ").strip()
		if check_token(inp):
			break

	api = vk_api.VkApi(token=inp)
	api = api.get_api()

	read_dialogs(
		api=api,
		dialogs=get_dialogs(api)
	)

	tools.log()
	tools.log("Press any key to exit...")
	tools.wait_click()
	exit()


if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		tools.log()
		tools.log("Stopped!")







