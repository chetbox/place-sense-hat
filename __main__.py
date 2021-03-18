from sense_hat import SenseHat, ACTION_PRESSED
import requests
from time import sleep
import sys

PALETTE = [
    (0xFF, 0xFF, 0xFF),
    (0xE4, 0xE4, 0xE4),
    (0x88, 0x88, 0x88),
    (0x22, 0x22, 0x22),
    (0xFF, 0xA7, 0xD1),
    (0xE5, 0x00, 0x00),
    (0xE5, 0x95, 0x00),
    (0xA0, 0x6A, 0x42),
    (0xE5, 0xD9, 0x00),
    (0x94, 0xE0, 0x44),
    (0x02, 0xBE, 0x01),
    (0x00, 0xD3, 0xDD),
    (0x00, 0x83, 0xC7),
    (0x00, 0x00, 0xEA),
    (0xCF, 0x6E, 0xE4),
    (0x82, 0x00, 0x80),
]

def get_item_at_index(canvas, canvas_depth, x, y):
    x_path = '{0:b}'.format(x).zfill(canvas_depth)
    y_path = '{0:b}'.format(y).zfill(canvas_depth)
    for i in range(canvas_depth):
        canvas = canvas[x_path[i] + y_path[i]]
    return canvas

def get_canvas(x=0, y=0, depth=0):
    x_path = '{0:b}'.format(x).zfill(depth)
    y_path = '{0:b}'.format(y).zfill(depth)
    path = ''.join([f'/{y_path[i]}{x_path[i]}' for i in range(depth)])
    r = requests.get(f'https://place-6ebc8.firebaseio.com/canvas/the-one-and-only/canvas{path}.json')
    if r.status_code == 200:
        return r.json()
    else:
        raise Error('HTTP ' + r.status_code)

def canvas_to_pixels(canvas, canvas_depth):
    return [
        PALETTE[get_item_at_index(canvas, canvas_depth, x, y)]
        for x in range(2**canvas_depth)
        for y in range(2**canvas_depth)
    ]

def redraw(sense, x, y):
    sense.set_pixels(pixels)

x = 0
y = 0
max_index = 15
canvas = False

def main():
    sense = SenseHat()
    sense.clear()
    sense.low_light = True

    def left(event):
        global x, max_index
        if event.action == ACTION_PRESSED:
            x = max(0, x - 1)

    def right(event):
        global x, max_index
        if event.action == ACTION_PRESSED:
            x = min(max_index, x + 1)

    def up(event):
        global y, max_index
        if event.action == ACTION_PRESSED:
            y = max(0, y - 1)

    def down(event):
        global y, max_index
        if event.action == ACTION_PRESSED:
            y = min(max_index, y + 1)

    def update_canvas():
        global canvas
        try:
            canvas = get_canvas()
        except:
            print('Error:', sys.exc_info()[0])    

    def redraw():
        global canvas
        if canvas:
            canvas_section = get_item_at_index(canvas, 4, y, x)
            sense.set_pixels(canvas_to_pixels(canvas_section, 3))

    sense.stick.direction_left = left
    sense.stick.direction_right = right
    sense.stick.direction_up = up
    sense.stick.direction_down = down
    sense.stick.direction_any = redraw
    
    while True:
        update_canvas()
        redraw()
        sleep(5)

if __name__ == '__main__':
    main()

