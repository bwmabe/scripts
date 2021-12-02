# scripts
misc scripts that aren't important enough for their own repo

## What They Are

### downloaders

#### dg_scraper.py
used to download multiple files on a direct-download site instead of clicking on each button individually

#### lynxchan\_media\_downloader.py
A script that downloads *all* the media from a a thread on a site running the `lynxchan` image board software

#### ytdl-wrapper
A wrapper script written in Python around my common use-cases for `youtube-dl`

#### zippy.py
A script that leverages Selenium, Geckodriver, and asyncio to download files from multiple Zippyshare pages. In need of serious cleanup to make it more usable.


### files

#### copy-videos-to-phone.sh
Copies a list of files (not just videos!) to an Android phone connected via USB over ADB.

#### ebooks.sh
Batch converts ebooks using Calibre's `ebook-convert` command

#### manga_zipper.sh
Used to zip individual chapters of downloaded manga into `.cbz` files

### music

#### ape2flac.py
A script that converts all `.ape` files in the current directory (and subdirectories!) into `.flac` files.

#### flacsplit.py
Recursively searches directories for `flac + cue` rips to split them into one `.flac` per track using `shntool` and `cuetools`. Sometimes makes mistakes when applying metadata. Creates a backup of the original single-file `.flac` and preserves the cuesheet to allow for manual correction.

#### tag_fixer.py
Fixes artist tags on all files of a type in a directory

### util

#### calc
A simple command line calculator that uses python; takes input as a quoted string. 

**ex:**
```sh
~> calc "1 + 1"
2
~> calc "math.sin(math.pi/2)"
1.0
```

#### cpu-temps.py
prints the temperatures of each CPU core. includes, min, max, and a rolling average

#### fix-discord.sh
Fixes an issue with Discord not respecting default browser settings on linux sometimes. Adapted from [here](https://old.reddit.com/r/discordapp/comments/89c881/default_web_browser_setting_not_respected_by/)

#### gen-password.py
Generates either passwords made from random words or characters. 

```
usage: gen-password.py CMD [--length LENGTH]
where CMD is either 'words' or 'chars'
```

#### iommu.sh
Assists with Identifying IOMMU Groups on Linux

#### minecraft-color-text.py
Formats text so that it will be rainbow in Minecraft chat.

#### screenshot-manager.sh
Watches my home directory for new screenshots and then crops them so only the right monitor is captured. Also moves them to `~/Screenshots`.
