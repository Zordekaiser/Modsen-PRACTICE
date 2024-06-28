import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, Button, Label, Scale, HORIZONTAL, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def choose_directory():
    """
    Открывает диалог для выбора директории с изображениями.
    Загружает изображения из выбранной директории.
    """
    global dir_path
    dir_path = filedialog.askdirectory()
    if dir_path:
        try:
            load_images()
        except Exception as e:
            messagebox.showerror("Ошибка загрузки изображений", str(e))

def load_images():
    """
    Загружает изображения из выбранной директории и сохраняет их в глобальный список `images`.
    Рассматриваются только файлы с расширениями 'png', 'jpg', 'jpeg', 'bmp', 'gif'.
    """
    global images, img_paths, current_image_index, formats
    images = []
    img_paths = []
    formats = []
    current_image_index = 0
    try:
        for file_name in os.listdir(dir_path):
            if file_name.lower().endswith(('png', 'jpg', 'jpeg', 'bmp', 'gif')):
                img_path = os.path.join(dir_path, file_name)
                ext = file_name.split('.')[-1].lower()
                img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
                if img is None:
                    raise ValueError(f"Не удалось загрузить изображение: {img_path}")
                if ext in ['jpg', 'jpeg', 'bmp']:
                    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                images.append(img)
                img_paths.append(img_path)
                formats.append(ext)
        if not images:
            raise ValueError("Нет подходящих изображений в выбранной директории.")
        show_image()
    except Exception as e:
        messagebox.showerror("Ошибка загрузки изображений", str(e))

def show_image():
    """
    Отображает текущее изображение в интерфейсе.
    Применяет вращение и отражение к изображению, если они были заданы.
    """
    global current_image, canvas
    try:
        img = images[current_image_index].copy()
        current_image = img
        if 'rotate' in globals():
            angle = rotate.get()
            (h, w) = img.shape[:2]
            M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1)
            img = cv2.warpAffine(img, M, (w, h))
        if 'flip' in globals():
            flip_value = flip.get()
            if flip_value == 1:
                img = cv2.flip(img, 0)
            elif flip_value == 2:
                img = cv2.flip(img, 1)
            elif flip_value == 3:
                img = cv2.flip(img, -1)

        fig, ax = plt.subplots()
        if img.shape[-1] == 4 and formats[current_image_index] == 'png':  # Если PNG с альфа-каналом
            rgba = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)  # Преобразуем формат для Matplotlib
            ax.imshow(rgba)
        else:
            ax.imshow(img)
        ax.axis('off')
        if canvas is not None:
            canvas.get_tk_widget().grid_forget()
        canvas = FigureCanvasTkAgg(fig, master=window)
        canvas.get_tk_widget().grid(row=1, columnspan=4)
        canvas.draw()
    except Exception as e:
        messagebox.showerror("Ошибка отображения изображения", str(e))

def save_image():
    """
    Сохраняет текущее изображение в выбранную директорию.
    Применяет вращение и отражение к изображению перед сохранением, если они были заданы.
    """
    global save_dir
    try:
        if current_image is not None:
            if save_dir == '':
                save_dir = filedialog.askdirectory(title="Выберите директорию для сохранения")
            if save_dir:
                ext = formats[current_image_index]
                save_path = os.path.join(save_dir, f'edited_{os.path.basename(img_paths[current_image_index])}')
                img_to_save = current_image.copy()

                # Применяем поворот и отражение, если они были изменены
                if 'rotate' in globals():
                    angle = rotate.get()
                    (h, w) = img_to_save.shape[:2]
                    M = cv2.getRotationMatrix2D((w/2, h/2), angle, 1)
                    img_to_save = cv2.warpAffine(img_to_save, M, (w, h))

                if 'flip' in globals():
                    flip_value = flip.get()
                    if flip_value == 1:
                        img_to_save = cv2.flip(img_to_save, 0)
                    elif flip_value == 2:
                        img_to_save = cv2.flip(img_to_save, 1)
                    elif flip_value == 3:
                        img_to_save = cv2.flip(img_to_save, -1)

                # Сохраняем изображение
                if ext in ['jpg', 'jpeg', 'bmp']:
                    cv2.imwrite(save_path, cv2.cvtColor(img_to_save, cv2.COLOR_RGB2BGR), [int(cv2.IMWRITE_JPEG_QUALITY), 95])
                elif ext == 'png':
                    if img_to_save.shape[-1] == 4:  # Если изображение с альфа-каналом (PNG)
                        cv2.imwrite(save_path, img_to_save)
                    else:
                        cv2.imwrite(save_path, cv2.cvtColor(img_to_save, cv2.COLOR_RGB2BGR), [int(cv2.IMWRITE_PNG_COMPRESSION), 3])
    except Exception as e:
        messagebox.showerror("Ошибка сохранения изображения", str(e))

def next_image():
    """
    Отображает следующее изображение в списке.
    """
    global current_image_index
    try:
        if images and current_image_index < len(images) - 1:
            current_image_index += 1
            show_image()
    except Exception as e:
        messagebox.showerror("Ошибка переключения изображения", str(e))

def prev_image():
    """
    Отображает предыдущее изображение в списке.
    """
    global current_image_index
    try:
        if images and current_image_index > 0:
            current_image_index -= 1
            show_image()
    except Exception as e:
        messagebox.showerror("Ошибка переключения изображения", str(e))

def crop_image():
    """
    Вырезает выбранную область текущего изображения.
    Отображает диалоговое окно для выбора области вырезки.
    """
    global current_image
    try:
        # Переконвертируем изображение обратно в BGR для cv2
        if current_image.shape[-1] == 4:  # Если изображение с альфа-каналом (PNG)
            img_bgr = current_image
        else:
            img_bgr = cv2.cvtColor(current_image, cv2.COLOR_RGB2BGR)
        
        if 'rotate' in globals():
            angle = rotate.get()
            (h, w) = img_bgr.shape[:2]
            M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1)
            img_bgr = cv2.warpAffine(img_bgr, M, (w, h))

        if 'flip' in globals():
            flip_value = flip.get()
            if flip_value == 1:
                img_bgr = cv2.flip(img_bgr, 0)
            elif flip_value == 2:
                img_bgr = cv2.flip(img_bgr, 1)
            elif flip_value == 3:
                img_bgr = cv2.flip(img_bgr, -1)

        # Задаем размеры окна для вырезки
        win_name = "Выделите область"
        cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)  # Устанавливаем нормальный размер окна
        cv2.resizeWindow(win_name, 800, 600)  # Устанавливаем начальный размер окна
        r = cv2.selectROI(win_name, img_bgr, fromCenter=False, showCrosshair=False)
        cv2.destroyWindow(win_name)
        x, y, w, h = map(int, r)
        current_image = current_image[y:y+h, x:x+w]
        images[current_image_index] = current_image
        show_image()
    except Exception as e:
        messagebox.showerror("Ошибка вырезки изображения", str(e))

# Создание основного окна
window = Tk()
window.title('Image Viewer')

dir_path = ''
save_dir = ''
images = []
img_paths = []
formats = []
current_image_index = 0
current_image = None
canvas = None

# Кнопки управления
btn_choose_dir = Button(window, text="Выбрать директорию", command=choose_directory)
btn_choose_dir.grid(row=0, column=0)

btn_prev = Button(window, text="Предыдущее", command=prev_image)
btn_prev.grid(row=0, column=1)

btn_next = Button(window, text="Следующее", command=next_image)
btn_next.grid(row=0, column=2)

btn_save = Button(window, text="Сохранить", command=save_image)
btn_save.grid(row=0, column=3)

btn_crop = Button(window, text="Вырезать", command=crop_image)
btn_crop.grid(row=0, column=4)

# Ползунок для поворота
rotate_label = Label(window, text="Поворот:")
rotate_label.grid(row=3, column=0)
rotate = Scale(window, from_=0, to=360, orient=HORIZONTAL, length=300, command=lambda x: show_image())
rotate.set(0)
rotate.grid(row=3, column=1)

# Ползунок для отражения
flip_label = Label(window, text="Отражение:")
flip_label.grid(row=4, column=0)
flip = Scale(window, from_=0, to=3, orient=HORIZONTAL, length=300, command=lambda x: show_image())
flip.set(0)
flip.grid(row=4, column=1)

window.mainloop()
