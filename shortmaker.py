import subprocess
import os
import sys
from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import crop, mirror_x
from moviepy.video.io.bindings import mplfig_to_npimage
import numpy as np
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn, SpinnerColumn, ProgressColumn
from rich.console import Console
from rich.table import Table

console = Console()

def download_videos(channel_url, download_dir="downloads"):
    """Downloads videos from a YouTube channel."""
    console.print("[bold green]Downloading videos...", justify="center")
    command = f"youtube-dl -f 22 -o {download_dir}/%(title)s.%(ext)s {channel_url}"
    subprocess.run(command, shell=True)

    # Trim 18 seconds from each downloaded video (comment out if not needed, or adjust time)
    for video_file in os.listdir(download_dir):
        video_path = os.path.join(download_dir, video_file)
        trimmed_video_path = os.path.splitext(video_path)[0] + "_trimmed" + os.path.splitext(video_path)[1]
        subprocess.run(["ffmpeg", "-i", video_path, "-ss", "00:00:18", "-c", "copy", trimmed_video_path])
        console.log(f"[green]Trimmed: {video_file}")

def process_and_move_video(video_path, output_folder="processed_videos", max_segments=5):
    """Processes a video, segments it dynamically, and moves it to the output folder."""
    try:
        console.print(f"[bold blue]Processing {video_path}...", justify="center")
        base_name = os.path.basename(video_path)
        name, ext = os.path.splitext(base_name)
        
        clip = VideoFileClip(video_path)
        
        total_duration = int(clip.duration)
        segment_duration = total_duration // max_segments
        

        num_segments = total_duration // segment_duration
        
        with Progress(console=console, bar_column=BarColumn(bar_width=None), spinner_column=SpinnerColumn(), 
                      text_column=TextColumn("{task.fields[name]}"), time_remaining_column=TimeRemainingColumn()) as progress:
            for i in range(num_segments + 1): 
                start_time = i * segment_duration
                end_time = min(start_time + segment_duration, total_duration)
                
                segment = clip.subclip(start_time, end_time)
                
                cropped_segment = crop(segment, width=int(segment.h * 9 / 16), height=segment.h, x_center=segment.w / 2, y_center=segment.h / 2)
                
                # Comment out this line to get rid of video mirroring
                mirrored_segment = mirror_x(cropped_segment)
                
                output_filename = f"{name}_part{i+1}{ext}" if i < num_segments else f"{name}_remainder{ext}"
                output_path = os.path.join(output_folder, output_filename)
                mirrored_segment.write_videofile(output_path, codec='libx264', audio_codec='aac', fps=24)
                
                progress.update(f"Segment {i+1}/{num_segments}", advance=1)
        
        console.log(f"[green]All segments of {video_path} processed and saved.")
    except Exception as e:
        console.print(f"[red]Error processing {video_path}: {e}", justify="center")

def main(channel_url):
    # Create directories for downloads and processed videos, replace with desired path if needed
    download_dir = "downloads"
    processed_dir = "processed_videos"
    os.makedirs(download_dir, exist_ok=True)
    os.makedirs(processed_dir, exist_ok=True)
    
    console.print("[bold yellow]Starting video processing...", justify="center")
    
    download_videos(channel_url, download_dir)
    
    for video_file in os.listdir(download_dir):
        video_path = os.path.join(download_dir, video_file)
        process_and_move_video(video_path, processed_dir)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        console.print("[bold red]Usage: python script.py <YouTube_channel_URL>", justify="center")
        sys.exit(1)
    
    channel_url = sys.argv[1]
    main(channel_url)
