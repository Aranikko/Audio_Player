from typing import Dict
import threading
import os
import eyed3
import flet
from flet import *
from pygame import mixer

mixer.init()

audio_name = []
time_tracks = []
play = False
current_track = 0
audio_thread = None  # Initialize audio_thread as None

for file_name in os.listdir("audio"):
    if os.path.isfile(os.path.join("audio", file_name)):
        audio_name.append("audio/" + file_name)

for i in range(len(audio_name)):
    time_tracks.append(round(eyed3.load(audio_name[i]).info.time_secs / 60, 2))

print(time_tracks)

def play_audio():
    global current_track
    while play:
        mixer.music.load(audio_name[current_track])
        mixer.music.play()
        while mixer.music.get_busy():
            pass  # Wait for the track to finish
        current_track = (current_track + 1) % len(audio_name)

def main(page: Page):
    page.window_maximizable = False
    global play, audio_thread
    page.title = "Audio Player"
    prog_bars: Dict[str, ProgressRing] = {}
    files = Ref[Column]()
    upload_button = Ref[ElevatedButton]()

    def file_picker_result(e: FilePickerResultEvent):
        if upload_button.current is not None:
            upload_button.current.disabled = True if e.files is None else False

        uf = []
        if file_picker.result is not None and file_picker.result.files is not None:
            for f in file_picker.result.files:
                audio_name.append("audio/" + f.name)
                uf.append(
                    FilePickerUploadFile(
                        f.name,
                        upload_url=page.get_upload_url(f.name, 600),
                    )
                )

            file_picker.upload(uf)

        page.update()

    file_picker = FilePicker(on_result=file_picker_result)

    page.overlay.append(file_picker)

    def volume(e):
        mixer.music.set_volume(e.control.value)

    def player_play(e):
        global play, audio_thread

        if audio_thread and audio_thread.is_alive():
            if mixer.music.get_busy():  # Check if audio is playing
                mixer.music.pause()
                btn_play_pause.icon = icons.PLAY_ARROW  # Change the icon to play
            else:
                mixer.music.unpause()
                btn_play_pause.icon = icons.PAUSE  # Change the icon to pause
        else:
            if len(audio_name) > 0:
                mixer.music.load(audio_name[0])

            play = not play

            if play:
                btn_play_pause.icon = icons.PAUSE
                audio_thread = threading.Thread(target=play_audio)
                audio_thread.start()
            else:
                btn_play_pause.icon = icons.PLAY_ARROW

        page.update()
        
        play = not play

        if play:
            btn_play_pause.icon = icons.PAUSE
            audio_thread = threading.Thread(target=play_audio)
            audio_thread.start()
        else:
            btn_play_pause.icon = icons.PLAY_ARROW

        page.update()

    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    pb = flet.PopupMenuButton(
        items=[
            flet.PopupMenuItem(text="upload", icon=icons.FOLDER_OPEN,
                                on_click=lambda _: file_picker.pick_files(allow_multiple=True)),

        ]
    )
    # Create a button
    btn_play_pause = flet.IconButton(icon=icons.PLAY_ARROW, on_click=player_play)
    btn_next_right = flet.IconButton(icon=icons.SKIP_NEXT)
    btn_next_left = flet.IconButton(icon=icons.SKIP_PREVIOUS)

    page.add(
        flet.Row(
            [
                pb,
                Column(ref=files),
                flet.Text("                                                                                                                             "),
                btn_next_left,
                btn_play_pause,
                btn_next_right,
                flet.Text("                                                                 "),
                flet.Text("Volume:"),
                flet.Slider(value=0.1, on_change=volume)
            ],
            alignment=flet.MainAxisAlignment.CENTER,
        )
    )

# Start the Flet application
flet.app(target=main, upload_dir="audio", view=flet.FLET_APP_WEB)
