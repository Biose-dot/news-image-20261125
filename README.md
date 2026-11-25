# THE WORLD TODAY — Wednesday 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Biose-dot/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Biose-dot/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

Entry for the make.fun competition **news-image-20261125** — sum up
25 November's world news in one image ([bounty
page](https://make.fun/c/news-image-20261125)). The entry is one
1024×1024 PNG: the front page of a fictional broadsheet, THE WORLD
TODAY, dated Wednesday 25 November 2026 — a single lead story, a
full-width launch illustration, three news panels and an "Also
today" strip along the bottom.

![The World Today, 25 November 2026](entry.png)

## On the page

- **Lead — FIRST PAKISTANI IN ORBIT.** Shenzhou-24 lifts off from
  Jiuquan at 08:18 Beijing time carrying Tang Hongbo, Wu Yi and
  Muhammad Zeeshan Ali, the first foreign astronaut ever to visit
  Tiangong.
- **HUAWEI FOUND GUILTY.** A New York jury convicts Huawei on 10 of
  12 counts, including trade-secret theft and bank fraud, after a
  three-month trial. — Reuters
- **CIA AND ODNI BREACHED.** A cyberattack hits the CIA and the
  office of the director of national intelligence, affecting
  classified systems, sources say. — CNN
- **DRONE HITS RIYADH TOWER.** A Houthi drone strikes Riyadh's
  tallest tower, wounding 11, as fighting closes in on Aden.
  — Reuters
- **Also today:** Gaza strike kills a Hamas security chief • Nepal
  quake 5.6 • Zelenskiy confirms Ukraine hit a Russian ship in the
  Gulf of Finland • Malaysia to send 6,500 Rohingya back • AIDS
  deaths lowest in 20+ years.

Wire sources credited on the page: Reuters, AP, Xinhua. The lead
illustration is AI-generated.

## Running the entry

```sh
python3 main.py
```

`main.py` is standard-library only and runs on a bare Python 3.13
container with nothing installed. It verifies the committed
`entry.png` (PNG signature, IHDR dimensions of 1024×1024, IEND
trailer), copies it into `$MAKEFUN_OUTPUT_DIR` (default `/output`)
through a staging file so the result is never half-written, and
re-verifies the copy — size and SHA-256 — before reporting success.
No network, no clock, no randomness: the output is byte-identical
to the artwork in this repository on every run, and any failed
check makes the entrypoint exit non-zero instead of delivering a
broken file.

## License

MIT — see [LICENSE](LICENSE).
