import pyglet

# Загружаем аудиофайл (измените на ваш файл)
music = pyglet.media.load('audio/Why Not.mp3')

# Создаем плеер
player = pyglet.media.Player()
player.queue(music)

# Устанавливаем начальную громкость
player.volume = 1.0  # Максимальная громкость

# Создаем окно для обработки клавиш
window = pyglet.window.Window()

@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        if player.playing:
            player.pause()
        else:
            player.play()
    elif symbol == pyglet.window.key.UP:
        # Увеличиваем громкость при нажатии на стрелку вверх
        if player.volume < 1.0:
            player.volume += 0.1
    elif symbol == pyglet.window.key.DOWN:
        # Уменьшаем громкость при нажатии на стрелку вниз
        if player.volume > 0.0:
            player.volume -= 0.1

@window.event
def on_draw():
    window.clear()
    pyglet.text.Label('Нажмите SPACE для паузы/продолжения', 
                     x=window.width//2, y=window.height//2, anchor_x='center', anchor_y='center').draw()
    pyglet.text.Label('Нажмите стрелку вверх/вниз для изменения громкости', 
                     x=window.width//2, y=window.height//2 - 30, anchor_x='center', anchor_y='center').draw()

# Запускаем цикл обработки событий Pyglet
pyglet.app.run()
