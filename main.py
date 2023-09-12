from typing import Dict
from pygame import mixer
import os
import eyed3
import flet
from flet import *

mixer.init()

audio_name = []
time_tracks = []
play = False

for file_name in os.listdir("audio"):
    if os.path.isfile(os.path.join("audio", file_name)):
        audio_name.append("audio/" + file_name)
        
for i in range(len(audio_name)):
    time_tracks.append(round(eyed3.load(audio_name[i]).info.time_secs/60, 2))
print(time_tracks)

def main(page: Page):
    page.window_maximizable = False
    global play
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
    
    while play:
        for i in range(len(audio_name)):
            mixer.music.load(audio_name[i])
            mixer.music.play()
    
    def volume(e):
        mixer.music.set_volume(e.control.value)
    
    def player_play(e):
        global play
        if len(audio_name) > 0:
            mixer.music.load(audio_name[0])
        play = not play
        if play:
            btn_play_pause.icon = icons.PAUSE
        else:
            btn_play_pause.icon = icons.PLAY_ARROW
        page.update() 
        print(play)
        page.update()  # Исправление: Вызываем метод update()

    def check_item_clicked(e):
        e.control.checked = not e.control.checked
        page.update()

    pb = flet.PopupMenuButton(
        items=[
            flet.PopupMenuItem(text="upload", icon=icons.FOLDER_OPEN,
            on_click=lambda _: file_picker.pick_files(allow_multiple=True)),
        
        ]
    ) 
    # Создайте кнопку
    btn_play_pause = flet.IconButton(icon=icons.PLAY_ARROW, on_click=player_play)
    btn_next_right = flet.IconButton(icon=icons.SKIP_NEXT)
    btn_next_left = flet.IconButton(icon=icons.SKIP_PREVIOUS)

    # page.add(pb, Column(ref=files))

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
    
    # page.add(
    #     flet.Row(
    #             [
    #                 flet.Text("Volume:"),
    #                 flet.Slider(value=0.1, on_change=volume)
    #             ],
    #             alignment=flet.MainAxisAlignment.END,  # Изменили значение на END
    #         )
    #     )
      
flet.app(target=main, upload_dir="audio", view=flet.FLET_APP_WEB)