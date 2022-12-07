from utils import AocClient
import re

client = AocClient.from_this_file()
data = client.get_input(use_example_data=False)
charlist = list(data)
for i in range(len(charlist)):
    if len(set(charlist[:4])) == 4:
        ans = i + 4
        break
    else:
        charlist.pop(0)


client.submit(level=1, answer=ans)

"""Day2"""
data = client.get_input(use_example_data=False)
charlist = list(data)
for i in range(len(charlist)):
    if len(set(charlist[:14])) == 14:
        ans2 = i + 14
        break
    else:
        charlist.pop(0)
client.submit(level=2, answer=ans2)
