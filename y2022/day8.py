import re
from utils import AocClient
import numpy as np

client = AocClient.from_this_file()
data = client.get_input(use_example_data=False)
lines = [line for line in data.splitlines() if line]
arr = np.array([[int(i) for i in line] for line in lines])

total = 1
visible = np.zeros_like(arr, dtype=bool)
for i in range(arr.shape[0]):
    for j in range(arr.shape[1]):
        val = arr[i, j]
        if (
            np.all(arr[i + 1 :, j] < val)
            or np.all(arr[:i, j] < val)
            or np.all(arr[i, j + 1 :] < val)
            or np.all(arr[i, :j] < val)
        ):
            visible[i, j] = True
print(visible)
ans = np.sum(visible)
client.submit(level=1, answer=ans)

score = np.zeros((4, *arr.shape), dtype=int)
for i in range(1, arr.shape[0] - 1):
    for j in range(1, arr.shape[1] - 1):
        val = arr[i, j]

        comp = arr[i + 1 :, j] < val  # down
        score[0, i, j] = len(comp) if np.all(comp) else np.argmin(comp) + 1

        comp = arr[i - 1 :: -1, j] < val  # up
        score[1, i, j] = len(comp) if np.all(comp) else np.argmin(comp) + 1

        comp = arr[i, j + 1 :] < val  # right
        score[2, i, j] = len(comp) if np.all(comp) else np.argmin(comp) + 1

        comp = arr[i, j - 1 :: -1] < val  # left
        score[3, i, j] = len(comp) if np.all(comp) else np.argmin(comp) + 1
        # if i == 3 and j == 2:
        #     break
scenic_score = np.product(score, axis=0)
print(scenic_score)
max_scenic_score = np.amax(scenic_score)
print(max_scenic_score)
client.submit(level=2, answer=max_scenic_score)
