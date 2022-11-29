import re
from pathlib import Path
import inspect
import requests
from utils.private import session
import json


class AocClient:
    def __init__(self, year, day):
        self.year = year
        self.day = day
        self.url = f"https://adventofcode.com/{year}/day/{day}"

        self.using_example_input = False

        self.cache_dir = Path("data") / f"{year}_{day}"
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.cache_input = self.cache_dir / "input.txt"
        self.cache_example = self.cache_dir / "example.txt"
        self.cache_status = self.cache_dir / "status.json"

        self.status = (
            json.loads(self.cache_status.read_text())
            if self.cache_status.exists()
            else {}
        )

    @classmethod
    def from_this_file(cls):
        call_file = Path(inspect.getframeinfo(inspect.currentframe().f_back)[0])
        day = int(re.match(r"[^\d]*(\d+)[^\d]*", call_file.stem).group(1))
        year = int(re.match(r"[^\d]*(\d+)[^\d]*", call_file.parent.name).group(1))
        return cls(year, day)

    def get_puzzle_input(self, force_refresh=False):
        if self.cache_input.exists() and not force_refresh:
            return self.cache_input.read_text()
        r = self.reqest("get", "input")
        self.cache_input.write_text(r.text)
        return r.text

    def get_example_input(self, force_refresh=False):
        if self.cache_example.exists() and not force_refresh:
            return self.cache_example.read_text()
        r = self.reqest("get", "")
        data = re.search(
            r"example.*?<pre><code>(.*?)</code></pre>", r.text, re.DOTALL
        ).group(1)
        self.cache_example.write_text(data)
        return data

    def get_input(self, use_example_data=False, force_refresh=True):
        if use_example_data:
            self.using_example_input = True
            return self.get_example_input(force_refresh)
        else:
            self.using_example_input = False
            return self.get_puzzle_input(force_refresh)

    def get_input_both(self):
        return self.get_puzzle_input(), self.get_example_input()

    def submit(self, level, answer):
        if not isinstance(answer, int):
            print("Answer must be an int")
            answer = int(answer)

        if (self.status.get("level1_complete") and level == 1) or (
            self.status.get("level2_complete") and level == 2
        ):
            print("Already submitted")
            return

        if self.using_example_input:
            print(f"You are using puzzle data, not example data\n Answer was: {answer}")
            return

        r = self.reqest("post", "answer", data={"level": level, "answer": answer})
        text = re.search(r"<article><p>(.*?)</p></article>", r.text, re.DOTALL).group(0)

        if m := re.search(r"That's the right answer", text):
            print("Correct")
            self.status[f"level{level}_complete"] = True
            self.cache_status.write_text(json.dumps(self.status))

        elif m := re.search(r"You have ((?:\d+m)) ((?:\d+s)) left to wait.", text):
            print(m.group(1), m.group(2))

        elif m := re.search(r"You don\'t seem to be solving the right level", text):
            print("You don't seem to be solving the right level")
            self.status[f"level{level}_complete"] = True
            self.cache_status.write_text(json.dumps(self.status))
        else:
            return
        return text

    def reqest(self, method, path, **kwargs):
        r = requests.request(
            method=method,
            url=f"{self.url}{f'/{path}' if path else ''}",
            cookies={"session": session},
            **kwargs,
        )
        assert r.status_code == 200
        return r
