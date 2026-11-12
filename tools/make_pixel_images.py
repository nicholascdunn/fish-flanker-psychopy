"""
Draw the pixel stimuli in images/ from the same pixel maps and colors as the
fish flanker demo on ncdunn.com (src/scripts/task-demo.ts and colors.ts).

Run from the repository root:  python tools/make_pixel_images.py
Needs Pillow (installed with PsychoPy).
"""
import os

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'images')

# One pixel of a stimulus becomes SCALE x SCALE pixels in the PNG. PsychoPy draws
# the images without smoothing, so they stay sharp at any size on screen.
SCALE = 16

# The website's fish: facing right, tail on the left, eye near the nose.
FISH_ROWS = ['d..rr..', 'ddrrrr.', 'drrrrer', 'ddrrrh.', 'd..rr..']
FISH_COLORS = {'r': '#ff5a68', 'd': '#a8303c', 'h': '#ffb3ba', 'e': '#1c1b1d'}

# An arrow pointing right, on the same 7 x 5 grid so arrows and fish are the same size.
ARROW_ROWS = ['....#..', '.....#.', '#######', '.....#.', '....#..']
ARROW_COLORS = {'#': '#e6e1e3'}  # the site's pale ink (PALE in colors.ts)


def draw(rows, colors, flip=False):
    w, h = len(rows[0]), len(rows)
    img = Image.new('RGBA', (w * SCALE, h * SCALE), (0, 0, 0, 0))
    px = img.load()
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch == '.':
                continue
            col = (w - 1 - i) if flip else i
            rgb = tuple(int(colors[ch][k:k + 2], 16) for k in (1, 3, 5))
            for y in range(j * SCALE, (j + 1) * SCALE):
                for x in range(col * SCALE, (col + 1) * SCALE):
                    px[x, y] = rgb + (255,)
    return img


def main():
    os.makedirs(OUT, exist_ok=True)
    draw(FISH_ROWS, FISH_COLORS).save(os.path.join(OUT, 'fish_right.png'))
    draw(FISH_ROWS, FISH_COLORS, flip=True).save(os.path.join(OUT, 'fish_left.png'))
    draw(ARROW_ROWS, ARROW_COLORS).save(os.path.join(OUT, 'arrow_right.png'))
    draw(ARROW_ROWS, ARROW_COLORS, flip=True).save(os.path.join(OUT, 'arrow_left.png'))
    print('wrote 4 images to', os.path.normpath(OUT))


if __name__ == '__main__':
    main()
