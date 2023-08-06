# built in libraries
import string

# tamcolors libraries
from .tam_buffer import TAMBuffer
from . import io_tam
from tamcolors.tam_c import _win_tam as io


"""
WinIO
draws out to windows terminal
gets ASCII key input from windows terminal
color mode 2
color mode 16
"""


class WinIOError(Exception):
    pass


class WinIO(io_tam.SingletonIO):
    def __init__(self):
        """
        info: makes WinIO object
        """
        self.__buffer = TAMBuffer(0, 0, " ", 1, 1)
        self.__last_frame = TAMBuffer(0, 0, " ", 1, 1)
        self.__windows_keys = self.get_key_dict()
        super().__init__()

    @classmethod
    def able_to_execute(cls):
        """
        info: will see if environment supported by WinIO
        :return: bool
        """
        if io is not None:
            return io._init_default_color() == 1
        return False

    def draw(self, tam_buffer):
        """
        info: will draw tam buffer to terminal
        :param tam_buffer: TAMBuffer
        :return:
        """

        if self.__buffer.get_dimensions() != io._get_dimension():
            self.clear()
            io._show_console_cursor(False)
            self.__buffer.set_dimensions_and_clear(*io._get_dimension())
            self.__last_frame = None

        super().draw(tam_buffer)

    def _draw_2(self, tam_buffer):
        """
        info: will draw tam buffer to terminal in mode 2
        :param tam_buffer: TAMBuffer
        :return:
        """
        # checks if buffer needs to be updated
        if " " != self.__buffer.get_defaults()[0] or self.__buffer.get_defaults()[1:] != tam_buffer.get_defaults()[1:]:
            # buffer defaults changed
            self.__buffer.set_defaults_and_clear(" ", *tam_buffer.get_defaults()[1:])

        # draw onto WinIO buffer
        self._draw_onto(self.__buffer, tam_buffer)

        # draw WinIO buffer to terminal
        self._print(0, 0, "".join(self.__buffer.get_raw_buffers()[0]), *self._processes_special_color(*tam_buffer.get_defaults()[1:]))

    def _draw_16(self, tam_buffer):
        """
        info: will draw tam buffer to terminal in mode 16
        :param tam_buffer: TAMBuffer
        :return:
        """
        # checks if buffer needs to be updated
        if "." != self.__buffer.get_defaults()[0] or self.__buffer.get_defaults()[2] != tam_buffer.get_defaults()[2]:
            # buffer defaults changed
            background = tam_buffer.get_defaults()[2]
            self.__buffer.set_defaults_and_clear(".", background, background)
            self.__last_frame = None

        # draw onto WinIO buffer
        self._draw_onto(self.__buffer, tam_buffer)

        """
        A block is a string or spots that 
        all share the same colors
        """
        start = None
        width = self.__buffer.get_dimensions()[0]
        length = 0
        this_foreground, this_background = None, None
        char_buffer, foreground_buffer, background_buffer = self.__buffer.get_raw_buffers()
        for spot, char, foreground, background in zip(range(len(self.__buffer)),
                                                      char_buffer,
                                                      foreground_buffer,
                                                      background_buffer):
            foreground, background = self._processes_special_color(foreground, background)
            # no block has benn made
            if start is None:
                # last frame buffer is not None
                if self.__last_frame is not None:
                    # spot has not change
                    if (char, foreground, background) == self.__last_frame.get_from_raw_spot(spot):
                        continue
                # make block
                start = spot
                this_foreground, this_background = foreground, background
                length = 1
            # spot has same colors as block
            elif (this_foreground == foreground or " " == char) and this_background == background:
                # add to block
                length += 1
            # spot does not have same colors as block
            else:
                # draw block to terminal
                self._print(start % width,
                            start//width,
                            "".join(char_buffer[start:start + length]),
                            this_foreground, this_background)
                # start new block
                this_foreground, this_background = foreground, background
                start = spot
                length = 1
                # last frame buffer is not None
                if self.__last_frame is not None:
                    # spot has not change
                    if (char, foreground, background) == self.__last_frame.get_from_raw_spot(spot):
                        # remove new block
                        start = None
                        length = 0

        if start is not None:
            # draw last block
            self._print(start % width, start//width, "".join(char_buffer[start:start + length]),
                        this_foreground, this_background)

        # update last frame
        if self.__last_frame is None:
            # last frame is not made
            self.__last_frame = self.__buffer.copy()
        else:
            # draw tam_buffer onto last frame
            self._draw_onto(self.__last_frame, tam_buffer)

    def start(self):
        """
        info: will setup terminal to be used
        :return:
        """
        self.clear()
        io._show_console_cursor(False)

    def done(self):
        """
        info: will reset terminal
        :return:
        """
        self.__buffer = TAMBuffer(0, 0, " ", 1, 1)
        self.__last_frame = TAMBuffer(0, 0, " ", 1, 1)

        io._set_cursor_info(0, 0, io._get_default_color())
        self.clear()
        io._show_console_cursor(True)

    def get_key(self):
        """
        info: will get single key input or return False
        :return: str or False
        """
        key_bytes = []
        key_byte = io._get_key()
        while key_byte != -1:
            key_bytes.append(key_byte)
            key_byte = io._get_key()

        if len(key_bytes) != 0:
            return self.__windows_keys.get(";".join([str(key_byte) for key_byte in key_bytes]), False)

        return False

    def get_dimensions(self):
        """
        info: will get teh terminal dimensions
        :return: (int, int)
        """
        return io._get_dimension()

    @staticmethod
    def get_key_dict():
        """
        info: makes a dict mapping key codes to key
        :return: dict
        """
        normal_key = string.digits + string.ascii_letters + "`-=[]\\;',./~!@#$%^&*()_+{}|:\"<>?"
        windows_keys = {str(ord(key)): (key, "NORMAL") for key in normal_key}

        for f_key in range(1, 10):
            windows_keys["0;{0}".format(58 + f_key)] = ("F{0}".format(f_key), "SPECIAL")
            windows_keys["0;{0}".format(83 + f_key)] = ("F{0}_SHIFT".format(f_key), "SPECIAL")

        code_224 = [[72, "UP"], [80, "DOWN"], [75, "LEFT"], [77, "RIGHT"], [83, "DELETE"],
                    [134, "F12"], [136, "F12_SHIFT"]]

        for code, key in code_224:
            windows_keys["224;{0}".format(code)] = (key, "SPECIAL")

        windows_keys["9"] = ("\t", "WHITESPACE")
        windows_keys["13"] = ("\n", "WHITESPACE")
        windows_keys["32"] = (" ", "WHITESPACE")

        windows_keys["8"] = ("BACKSPACE", "SPECIAL")
        windows_keys["27"] = ("ESCAPE", "SPECIAL")

        return windows_keys

    def printc(self, output, color, flush, stderr):
        """
        info: will print out user output with color
        :param output: str
        :param color: tuple: (int, int)
        :param flush: boolean
        :param stderr: boolean
        :return: None
        """
        default_color = io._get_default_color()
        color = self._processes_special_color(*color)
        io._set_console_color((color[0] % 16) + (color[1] % 16) * 16)
        self._write_to_output_stream(output, flush, stderr)
        io._set_console_color(default_color)

    def inputc(self, output, color):
        """
        info: will get user input with color
        :param output: str
        :param color: tuple: (int, int)
        :return: str
        """
        default_color = io._get_default_color()
        color = self._processes_special_color(*color)
        io._set_console_color((color[0] % 16) + (color[1] % 16)*16)
        ret = input(output)
        io._set_console_color(default_color)
        return ret

    def clear(self):
        """
        info: will clear the screen
        :return:
        """
        io._clear()

    def get_color(self, spot):
        """
        info: will get the color value
        :param spot: int
        :return: tuple: (int, int, int)
        """
        return io._get_rgb_color(spot)

    def set_color(self, spot, color):
        """
        info: sets a color value
        :param spot: int: 0 - 15
        :param color: tuple: (int, int, int)
        :return: None
        """
        super().set_color(spot, color)
        io._set_rgb_color(spot, *color)
        self.__last_frame = None

    @classmethod
    def _print(cls, x, y, output, foreground_color, background_color):
        """
        info: will print to terminal
        :param x: int
        :param y: int
        :param output: str
        :param foreground_color: int
        :param background_color: int
        :return:
        """
        io._set_cursor_info(x, y, (foreground_color % 16) + (background_color % 16)*16)
        cls._write_to_output_stream(output, True, False)

    @staticmethod
    def _processes_special_color(foreground_color, background_color):
        """
        info: will processes special colors
        -1 and -2 will become the default terminal color
        :param foreground_color: int
        :param background_color: int
        :return: tuple: (int, int)
        """
        if foreground_color in (-1, -2) or background_color in (-1, -2):
            default_color = io._get_default_color()
            default_background_color = default_color//16
            default_foreground_color = default_color - default_background_color*16

            if foreground_color in (-1, -2):
                foreground_color = default_foreground_color
            if background_color in (-1, -2):
                background_color = default_background_color

        return foreground_color, background_color
