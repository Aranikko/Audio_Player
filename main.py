from typing import Dict
import os
import eyed3
import flet
from flet import *
from pygame import mixer

# Инициализируем pygame
mixer.init()

# Устанавливаем громкость (от 0.0 до 1.0)
mixer.music.set_volume(0.5)

audio_name = []
time_tracks = []
play = False
pos_sound = 0

index = 0

def script_load_music():
    global index
    
    for file in os.listdir('audio'):
        if file.endswith('.wav') or file.endswith('.aac') or file.endswith('.flac'):
            os.rename(os.path.join('audio', file), os.path.join('audio', file.replace('.wav', '.mp3')))
    
    audio_name.clear()
    time_tracks.clear()
    for file_name in os.listdir("audio"):
        if file_name.endswith(".mp3"):  # Убедимся, что файлы - это MP3
            audio_name.append(os.path.join("audio", file_name))
    for i in range(len(audio_name)):
        time_tracks.append(round(eyed3.load(audio_name[i]).info.time_secs / 60, 2))
    index = 0
    mixer.music.load(audio_name[index])
    

def main(page: Page):
    script_load_music()
    page.window_maximizable = False
    page.window_height = 670
    page.window_max_height = 670
    page.window_max_width = 1264
    page.window_min_height = 670
    page.window_min_width = 1264
    global play, pos_sound, index
    page.title = "Audio Player"
    files = Ref[Column]()
    upload_button = Ref[ElevatedButton]()

    # upload audio
    def file_picker_result(e: FilePickerResultEvent):
        if upload_button.current is not None:
            upload_button.current.disabled = True if e.files is None else False

        
        
        uf = []
        if file_picker.result is not None and file_picker.result.files is not None:
            for f in file_picker.result.files:
                audio_name.append(os.path.join("audio", f.name))
                uf.append(
                    FilePickerUploadFile(
                        f.name,
                        upload_url=page.get_upload_url(f.name, 600),
                    )
                )

            file_picker.upload(uf)
        
        for file in os.listdir('audio'):
            if file.endswith('.wav') or file.endswith('.aac') or file.endswith('.flac'):
                os.rename(os.path.join('audio', file), os.path.join('audio', file.replace('.wav', '.mp3')))
        
        page.update()

    file_picker = FilePicker(on_result=file_picker_result)

    page.overlay.append(file_picker)

    def volume(e):
        mixer.music.set_volume(e.control.value)

    def player_play(e):
        global play, pos_sound
        play = not play
        if play:
            btn_play_pause.icon = icons.PAUSE
            if pos_sound > 0:
                mixer.music.unpause()
            else:
                mixer.music.play()
        else:
            btn_play_pause.icon = icons.PLAY_ARROW
            pos_sound = mixer.music.get_pos()
            mixer.music.pause()
        page.update()

    def next_track(e):
        global index, pos_sound, play
        if index < len(audio_name) - 1:
            index += 1
            pos_sound = 0
            mixer.music.load(audio_name[index])
            mixer.music.play()
            play = True
            btn_play_pause.icon = icons.PAUSE
            page.update()
        else:
            index = 0
            mixer.music.load(audio_name[index])
            mixer.music.play()
            play = True
            btn_play_pause.icon = icons.PAUSE
            page.update()

    def previous_track(e):
        global index, pos_sound, play
        if index > 0:
            index -= 1
            pos_sound = 0
            mixer.music.load(audio_name[index])
            mixer.music.play()
            play = True
            btn_play_pause.icon = icons.PAUSE
            page.update()

    pb = flet.PopupMenuButton(
        items=[
            flet.PopupMenuItem(text="upload", icon=icons.FOLDER_OPEN,
                               on_click=lambda _: file_picker.pick_files(allow_multiple=True)),

        ]
    )

    btn_play_pause = flet.IconButton(icon=icons.PLAY_ARROW, on_click=player_play)
    btn_next_right = flet.IconButton(icon=icons.SKIP_NEXT, on_click=next_track)
    btn_next_left = flet.IconButton(icon=icons.SKIP_PREVIOUS, on_click=previous_track)

    page.add(
        pb,
        Column(ref=files),
    )

    space = [page.add(Text('')) for _ in range(17)]

    page.add(
        flet.Column(
            [
                flet.Row(
                    [

                        flet.Text("Volume:"),
                        flet.Slider(value=0.1, on_change=volume),
                        flet.Text("                                                                            "),
                        btn_next_left,
                        btn_play_pause,
                        btn_next_right,
                        flet.Text("                                                                                                                             "),

                    ],
                    alignment=flet.MainAxisAlignment.END,
                ),

            ],
            alignment=flet.MainAxisAlignment.CENTER,
        )
    )

flet.app(target=main, upload_dir="audio", view=flet.FLET_APP_WEB)
