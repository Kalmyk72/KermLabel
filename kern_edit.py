import tkinter as tk
import json
from tkinter import filedialog
from PIL import Image, ImageTk

class ImageCanvas(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        #Привязка действий к кнопкам
        self.bind("<MouseWheel>", self.zoom)
        self.bind("<ButtonPress-2>", self.scroll_start)
        self.bind("<B2-Motion>", self.scroll_move)
        self.bind("<Button-1>", self.draw_rect)
        self.bind("<Motion>", self.mouse_position)
        #Пустые шаблоны изображений изначальное и превращенное в tk формат
        self.image = None
        self.image_tk = None
        # шаг приближения
        self.scale = 0.5
        #путь файла
        self.file_path = ''
        #пред параметры изображения при приближении
        self.new_width = 0
        self.new_height = 0
        self.resized_image = None
        #Координаты мыши
        self.mouse_x = 0
        self.mouse_y = 0
        #пред параметры прямоугольников
        self.rect_coords = []
        self.rectangles = {}
        self.rect_counter = 1

 # Открытие фото с диска
    def open_image(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            image = Image.open(self.file_path)
            self.image = image
            self.show_image()

#функция отображения на холсте с изменнием размера.
    def show_image(self):
        if self.image:
            width, height = self.image.size
            self.new_width = int(width * self.scale)
            self.new_height = int(height * self.scale)
            self.resized_image = self.image.resize((self.new_width, self.new_height))
            self.image_tk = ImageTk.PhotoImage(self.resized_image)

            self.config(scrollregion=(0, 0, width, height))
            self.create_image(0, 0, anchor=tk.NW, image=self.image_tk)


#Функция приближения
    def zoom(self, event):
        if event.delta > 0:
            self.scale *= 1.1
        else:
            self.scale /= 1.1
        self.show_image()

    def scroll_start(self, event):
        self.scan_mark(event.x, event.y)

    def scroll_move(self, event):
        self.scan_dragto(event.x, event.y, gain=1)

#функция рисования прямоугольника по координатам
    def draw_rect(self, event):
        #расчет координат вершины с учетом приближения
        x = int(event.x / self.scale)
        y = int(event.y / self.scale)

        if len(self.rect_coords) == 0:
            self.rect_coords.append((x, y))
        elif len(self.rect_coords) == 1:
            x0, y0 = self.rect_coords[0]
            x1, y1 = x, y
            rect_id = self.create_rectangle(x0 * self.scale, y0 * self.scale, x1 * self.scale, y1 * self.scale, outline="red")
            rect_data = {
                "x": x0,
                "y": y0,
                "width": x1 - x0,
                "height": y1 - y0
            }
            self.rectangles[self.rect_counter] = rect_data
            self.rect_counter += 1
            self.rect_coords.clear()
# Регистрация положения координат мыши
    def mouse_position(self, event):
        x = int(event.x / self.scale)
        y = int(event.y / self.scale)
        self.mouse_x = x
        self.mouse_y = y
# Сохранение прямоугольников в json
    def save_rectangles_to_json(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w") as file:
                json.dump(self.rectangles, file)

def main():
    root = tk.Tk()
    root.title("Image Editor")

    #инициализирование холста
    image_canvas = ImageCanvas(root)
    image_canvas.pack(fill=tk.BOTH, expand=True)

 #Инициализироване меню
    menu_bar = tk.Menu(root)
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label="Open Image", command=image_canvas.open_image)
    file_menu.add_command(label="Save Rectangles to JSON", command=image_canvas.save_rectangles_to_json)

    menu_bar.add_cascade(label="File", menu=file_menu)

    root.config(menu=menu_bar)
    root.mainloop()

if __name__ == "__main__":
    main()
