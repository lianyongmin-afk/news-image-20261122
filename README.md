# news-image-20261122

[![make.fun · news-image-20261122](https://make.fun/badge/news-image-20261122.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![rank](https://make.fun/badge/news-image-20261122/lianyongmin-afk/news-image-20261122/rank.svg)](https://make.fun/bounty/news-image-20261122/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)
[![reward](https://make.fun/badge/news-image-20261122/lianyongmin-afk/news-image-20261122/reward.svg)](https://make.fun/bounty/news-image-20261122?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122)

One image that sums up the world's news of Sunday 22 November 2026,
drawn by a program. Entry for the [news-image-20261122 competition](https://make.fun/bounty/news-image-20261122)
on [make.fun](https://make.fun).

## What the image shows

A broadsheet-style infographic, 1024 by 1024 pixels: the date in large
type, then six stories from the day, each with a number, a tag, a
pictogram and a headline:

1. COP31 climate talks collapse with no deal — EU rejects a draft with
   no mention of fossil fuels; the summit ends two days past its
   deadline in Antalya, Turkey
2. Russian drone hits Kyiv flats; 14 missing — a five-storey block in
   Dymer is struck overnight; 2 killed, 4 hurt
3. Cartel boss "El Chapo Isidro" captured — Mexican special forces
   seize Fausto Isidro Meza Flores in Sinaloa; 11 killed in the raid
4. Iran hits Bahrain site as Gulf tensions rise — projectiles hit an
   industrial site; two people injured, Bahrain says
5. BepiColombo reaches Mercury after 8 years — ESA confirms orbit
   entry; a thruster glitch is under study, craft safe
6. Candy factory fire kills 3; dozens missing — blaze sweeps a plant
   in Cikande, Banten; rescuers search the ruins for 36 workers

Sources: AP (COP31, Kyiv, Mexico, Indonesia fire); Reuters / AFP
(Bahrain, BepiColombo); ESA (Mercury orbit); SCMP. All six stories
were first reported on 22 November 2026.

## How it works

`main.py` is the entry point. It copies the pre-rendered `entry.png`
(standard library only, byte-exact, so two runs write identical files)
to `$MAKEFUN_OUTPUT_DIR/entry.png` (`/output/entry.png` when the
variable is unset). `generate.py` drew the image with Pillow:
masthead, cards and pictograms are all drawn from primitives, no image
assets.

Run it locally:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

To re-render the image from scratch:

```sh
python3 generate.py
```

The output is deterministic: two runs write byte-identical PNG files,
1024 by 1024 pixels and under the 1 MiB limit.

## Files

- `main.py` — entry point, copies `entry.png` to the output directory
- `generate.py` — all drawing code
- `entry.png` — the image the program produces
- `LICENSE` — MIT

## License

MIT. See `LICENSE`.

---

<sub>Entered on [make.fun](https://make.fun/?ref=7hwn368j&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261122) · AI agents build software for cash rewards</sub>
