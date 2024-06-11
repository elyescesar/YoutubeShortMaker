# YoutubeShortMaker

A script to download, process and trim youtube videos from any given channel, this script was created to automate the task of creating hundreds of youtube shorts/tiktoks of movie scenes, thus the trimming of 18 seconds because of the outro, if you wish to remove mirroring or trimming, feel free to modify the code with the help of the comments.

## Requirements

- Python 3.x
- `moviepy` >= 1.0.3
- `rich` >= 2.12.0

Install dependencies with:

`bash pip install -r requirements.txt`


Additionally, ensure [youtube-dl](https://github.com/ytdl-org/youtube-dl) and [ffmpeg](https://github.com/FFmpeg/FFmpeg) are installed on your system. Instructions for installing these tools can be found in their official documentation.

## Usage

Run the script with a YouTube channel URL as an argument:
`
python shortmaker.py https://www.youtube.com/channel/CHANNEL_ID`

Replace `https://www.youtube.com/channel/CHANNEL_ID` with the actual URL of the YouTube channel you want to process.

## Contributing

Contributions are welcome Please feel free to submit a pull request.
