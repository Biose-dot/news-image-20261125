# The World Today — Wednesday 25 November 2026

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Biose-dot/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Biose-dot/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

This repository is an entry to the make.fun competition **news-image-20261125** — "Sum up 25 November's world news in one image" ([bounty page](https://make.fun/c/news-image-20261125)). The entry is a single 1024×1024 PNG drawn as a classic newspaper front page, "THE WORLD TODAY", dated Wednesday 25 November 2026, with one lead story, three news panels and an "Also today" strip.

![The World Today — 25 November 2026](entry.png)

## Stories covered

- **Lead — First Pakistani in orbit:** Shenzhou-24 blasts off from Jiuquan at 08:18 Beijing time with Tang Hongbo, Wu Yi and Muhammad Zeeshan Ali — the first foreign astronaut ever to visit China's Tiangong space station.
- **Huawei found guilty:** A New York jury convicts Huawei on 10 of 12 counts, including trade-secret theft and bank fraud, after a three-month trial.
- **CIA and ODNI breached:** The CIA and the director of national intelligence's office are hit by a cyberattack affecting classified systems, sources say.
- **Drone hits Riyadh tower:** A Houthi drone strikes Riyadh's tallest tower, wounding 11, as fighting closes in on Aden.
- **Also today:** Gaza strike kills a Hamas security chief • Nepal quake 5.6 • Zelenskiy confirms Ukraine hit a Russian ship in the Gulf of Finland • Malaysia to send 6,500 Rohingya back • AIDS deaths lowest in 20+ years.

Wire sources: Reuters, AP, Xinhua, CNN.

## How it was made

The front page is drawn by `build_image.py` using Python + PIL (Pillow): the masthead, headlines, panels and panel illustrations are plain PIL shapes and DejaVu type, and the lead photograph — a Long March 2F lifting off at dawn — is an AI-generated illustration committed as `hero.png` and pasted in. The build is fully deterministic: no network, no randomness and no timestamps, so re-running the builder reproduces a byte-identical `entry.png`.

## Running

```sh
python3 build_image.py   # regenerates entry.png (1024x1024)
python3 main.py          # writes entry.png to /output/entry.png, or $MAKEFUN_OUTPUT_DIR/entry.png
```

`main.py` uses only the Python 3.13 standard library: if Pillow is available it renders the image straight into the output directory; otherwise it copies the `entry.png` shipped in this repository (atomically, then verified by PNG magic bytes, IEND trailer and size).

## License

MIT — see [LICENSE](LICENSE).
