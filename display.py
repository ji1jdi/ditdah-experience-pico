import ssd1306

class Display:
    def __init__(self, oled):
        self._oled = oled

    def show(self, character):
        self._oled.fill(0)
        self._oled_text_scaled(character, 32, 8, 8)
        self._oled.show()

    # This code is adapted from code introduced on the following URL:
    # https://github.com/orgs/micropython/discussions/16382
    def _oled_text_scaled(self, text, x, y, scale, character_width=8, character_height=8):
        # temporary buffer for the text
        width = character_width * len(text)
        height = character_height
        temp_buf = bytearray(width * height)
        temp_fb = ssd1306.framebuf.FrameBuffer(temp_buf, width, height, ssd1306.framebuf.MONO_VLSB)

        # write text to the temporary framebuffer
        temp_fb.text(text, 0, 0, 1)

        # scale and write to the display
        for i in range(width):
            for j in range(height):
                pixel = temp_fb.pixel(i, j)
                if pixel:  # If the pixel is set, draw a larger rectangle
                    self._oled.fill_rect(x + i * scale, y + j * scale, scale, scale, 1)
