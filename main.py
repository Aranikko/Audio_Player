from typing import Dict
import os
import eyed3
import flet
from flet import *


audio_name = []
time_tracks = []
play = False

index = 0

def script_load_music():
    for file_name in os.listdir("audio"):
        if os.path.isfile(os.path.join("audio", file_name)):
            audio_name.append("audio/" + file_name)
    for i in range(len(audio_name)):
        time_tracks.append(round(eyed3.load(audio_name[i]).info.time_secs/60, 2))

def main(page: Page):
    script_load_music()
    page.window_maximizable = False
    page.window_height = 670
    page.window_max_height = 670
    page.window_max_width = 1264
    page.window_min_height = 670
    page.window_min_width = 1264
    global play
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
        pass
    
    def player_play(e):
        global play
        play = not play
        if play:
            btn_play_pause.icon = icons.PAUSE
        else:
            btn_play_pause.icon = icons.PLAY_ARROW
        page.update() 
        print(page.width, page.height)
        page.update()  

    def next_track(e):
        global index
        if index < len(audio_name)-1:
            index += 1
        print(index)
    
    def previous_track(e):
        global index
        if index >= len(audio_name)-1:
            index -= 1
        print(index)
    
    pb = flet.PopupMenuButton(
        items=[
            flet.PopupMenuItem(text="upload", icon=icons.FOLDER_OPEN,
            on_click=lambda _: file_picker.pick_files(allow_multiple=True)),
        
        ]
    ) 

    btn_play_pause = flet.IconButton(icon=icons.PLAY_ARROW, on_click=player_play)
    btn_next_right = flet.IconButton(icon=icons.SKIP_NEXT, on_click=next_track)
    btn_next_left = flet.IconButton(icon=icons.SKIP_PREVIOUS, on_click=previous_track)

    page.add(pb,
            Column(ref=files),
    )

    space = [page.add(Text('')) for i in range(17)]
    
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