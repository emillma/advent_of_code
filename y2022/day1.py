from utils import AocClient

client = AocClient.from_this_file()
data = client.get_input(use_example_data=False)

elves = data.split("\n\n")
cals = [el.split("\n") for el in elves]
cals = [[int(n) for n in cal if n] for cal in cals]
ans = max([sum(el) for el in cals])
client.submit(level=1, answer=ans)

total_per_elf = [sum(el) for el in cals]
ans2 = sum(sorted(total_per_elf, reverse=True)[:3])
client.submit(level=2, answer=ans2)
