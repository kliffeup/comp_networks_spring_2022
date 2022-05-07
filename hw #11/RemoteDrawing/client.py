from io import BytesIO
from requests import post, Response
from tkinter import Canvas, Menu, Tk
from typing import Optional

from PIL import Image


class Point:
    def __init__(self, x: Optional[int] = None, y: Optional[int] = None):
        self.x = x
        self.y = y


class DrawingApp:
    width = 500
    height = 400
    color_fg = 'black'
    color_bg = 'white'
    pen_width = 5

    url = 'http://127.0.0.1:5000'
    headers = {'content-type': 'image/jpeg'}

    def __init__(self, master: Optional[Tk] = None) -> None:
        self.master = master
        self.cur_pos = None

        self.draw_widgets()

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

    def paint(self, position: Point) -> None:
        if self.cur_pos:
            self.canvas.create_line(
                self.cur_pos.x,
                self.cur_pos.y,
                position.x,
                position.y,
                width=self.pen_width,
                fill=self.color_fg,
                capstyle='round',
                smooth=True,
            )

        self.cur_pos = position
        self.save_canvas()
        self.post_canvas()

    def reset(self, position: Point) -> None:
        self.cur_pos = None
        self.save_canvas()
        self.post_canvas()

    def clear(self) -> None:
        self.canvas.delete('all')
        self.save_canvas()
        self.post_canvas()

    def draw_widgets(self) -> None:
        self.canvas = Canvas(
            self.master,
            width=self.width,
            height=self.height,
            bg=self.color_bg
        )

        self.canvas.pack(fill='both', expand=True)

        menu = Menu(self.master)
        self.master.config(menu=menu)

        file_menu = Menu(menu)
        option_menu = Menu(menu)
        menu.add_cascade(label='Options', menu=option_menu)
        option_menu.add_command(label='Clear Canvas', command=self.clear)
        option_menu.add_command(label='Exit', command=self.master.destroy)

    def save_canvas(self) -> None:
        postscript = self.canvas.postscript(colormode='color')
        image = Image.open(BytesIO(postscript.encode('utf-8')))
        image.save_canvas('temp/canvas.jpg')

    def post_canvas(self) -> Response:
        image = open('temp/canvas.jpg', 'rb').read()
        response = post(self.url, data=image, headers=self.headers)
        return response


if __name__ == '__main__':
    root = Tk()
    DrawingApp(root)
    root.title('Application')
    root.mainloop()
