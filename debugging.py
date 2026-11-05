paused = False
p_pressed = True
while True:
    if p_pressed and not paused:
        paused = True
    elif p_pressed:
        paused = False
    print(paused)