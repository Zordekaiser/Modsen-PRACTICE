import unittest
from unittest.mock import patch, MagicMock
import os
import cv2
import numpy as np
import main  # Убедитесь, что 'main' находится в той же директории

class TestImageViewer(unittest.TestCase):

    def setUp(self):
        self.test_dir = "test_images"
        os.makedirs(self.test_dir, exist_ok=True)
        self.test_image_path = os.path.join(self.test_dir, "test_image.png")
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        cv2.imwrite(self.test_image_path, test_image)
        main.dir_path = self.test_dir

    def tearDown(self):
        if os.path.exists(self.test_image_path):
            os.remove(self.test_image_path)
        if os.path.exists(self.test_dir):
            os.rmdir(self.test_dir)
        main.images = []
        main.img_paths = []
        main.current_image_index = 0
        main.current_image = None

    def test_load_images(self):
        main.load_images()
        self.assertTrue(len(main.images) > 0, "Изображения не были загружены")

    def test_next_image(self):
        main.load_images()
        if len(main.images) > 1:
            main.next_image()
            self.assertEqual(main.current_image_index, 1, "Следующее изображение не отображено")
        else:
            self.assertEqual(main.current_image_index, 0, "Нет второго изображения для отображения")

    def test_prev_image(self):
        main.load_images()
        if len(main.images) > 1:
            main.next_image()
            main.prev_image()
            self.assertEqual(main.current_image_index, 0, "Предыдущее изображение не отображено")
        else:
            self.assertEqual(main.current_image_index, 0, "Нет второго изображения для отображения")

    @patch('main.show_image')
    def test_show_image(self, mock_show_image):
        main.load_images()
        main.show_image()
        self.assertTrue(mock_show_image.called, "Функция отображения изображения не была вызвана")



if __name__ == "__main__":
    unittest.main()
