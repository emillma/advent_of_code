from utils import AocClient

client = AocClient.from_this_file()

data = client.get_input(False)


data = [int(i) for i in data.splitlines()]
ans = sum(data[i + 1] > data[i] for i in range(len(data) - 1))
client.submit(1, ans)

sliding_window = 3
data_slide = [
    sum(data[i + j] for j in range(sliding_window))
    for i in range(len(data) - sliding_window + 1)
]
ans = sum(data_slide[i + 1] > data_slide[i] for i in range(len(data_slide) - 1))
print(ans)
client.submit(2, ans)
