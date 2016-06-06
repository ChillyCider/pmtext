# Instruction opcodes
_CHAR    = 0
_NEWLINE = 1
_FONT    = 2
_COLOR   = 3
_SHAKE   = 4
_WAIT    = 5
_CUSTOM  = 6

class Graph:
    def __init__(self, default_font):
        self.instructions = []
        self.default_font = default_font

    def string(self, s):
        '''Adds a string of characters to the passage.'''
        for c in s:
            self.instructions.append((_CHAR, c))

    def draw(self, dst, x, y):
        '''Draw the passage.'''
        cursor_x = x
        cursor_y = y
        font = self.default_font
        color = (255, 255, 255)
        shake = None
        char_index = 0 # For shake effects

        for op in self.instructions:
            if op[0] == _CHAR:
                # The character we need to draw
                ch = op[1]

                # Offset by shake
                off_x, off_y = 0, 0
                if shake:
                    off_x, off_y = shake(char_index)

                # Draw it
                font.draw_glyph(dst, cursor_x+off_x, cursor_y+off_y, color, ch)

                # Advance the cursor
                cursor_x += font.get_glyph_width(ch)
                char_index += 1
            elif op[0] == _NEWLINE:
                cursor_x = x
                cursor_y += font.get_linesize()
            elif op[0] == _FONT:
                font = op[1]
            elif op[0] == _COLOR:
                color = (op[1], op[2], op[3])
            elif op[0] == _SHAKE:
                shake = op[1]

    def newline(self):
        '''Add a newline to the passage.'''
        self.instructions.append((_NEWLINE,))

    def font(self, font):
        '''Use a new font for this part of the passage.'''
        self.instructions.append((_FONT, font))

    def color(self, r, g, b):
        '''Use a new color for this part of the passage.'''
        self.instructions.append((_COLOR, r, g, b))

    def shake(self, func):
        '''Use a shake function for this part of the passage.'''
        self.instructions.append((_SHAKE, func))

class Typewriter:
    '''Wraps around a Graph, throttling character output.'''
    def __init__(self, view):
        self.view = view
        self.queue = []

    def slow_string(self, delay, s):
        '''Queue up a slow string of characters.'''
        for c in s:
            self.wait(delay)
            self.string(c)

    def string(self, s):
        '''Queue up a string of characters.'''
        for c in s:
            self.queue.append((_CHAR, c))

    def draw(self, dst, x, y):
        '''Draw the graph somewhere.'''
        self.view.draw(dst, x, y)

    def newline(self):
        '''Queue up a newline.'''
        self.queue.append((_NEWLINE,))

    def font(self, surface_list):
        '''Queue up a font change.'''
        self.queue.append((_FONT, surface_list))

    def color(self, r, g, b):
        '''Queue up a color change.'''
        self.queue.append((_COLOR, r, g, b))

    def shake(self, func):
        '''Queue up a shake-function change.'''
        self.queue.append((_SHAKE, func))

    def pulse(self):
        '''Executes the queue up to the first printed character.'''
        while self.queue:
            op = self.queue.pop(0)

            if op[0] == _CHAR:
                self.view.string(op[1])
                break
            elif op[0] == _NEWLINE:
                self.view.newline()
            elif op[0] == _FONT:
                self.view.font(op[1])
            elif op[0] == _COLOR:
                self.view.color(op[1], op[2], op[3])
            elif op[0] == _SHAKE:
                self.view.shake(op[1])
            elif op[0] == _WAIT:
                break
            elif op[0] == _CUSTOM:
                op[1]()

    def flush(self):
        '''Flush the whole queue.'''
        while self.queue:
            self.pulse()

    def wait(self, n):
        '''Queue up a delay.'''
        for _ in xrange(n):
            self.queue.append((_WAIT,))

    def custom(self, func):
        '''Queue up a custom function call.'''
        self.queue.append((_CUSTOM, func))
