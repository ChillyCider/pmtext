import pygame

class BitmapFont:
    def __init__(self, surface, glyph_rects):
        self.surface = surface
        self.glyph_rects = glyph_rects
    def draw_glyph(self, dst, x, y, color, ch):
        index = ord(ch) - ord(' ')

        old_color = self.surface.get_palette_at(1)
        self.surface.set_palette_at(1, color)

        dst.blit(self.surface, (x, y), self.glyph_rects[index])

        self.surface.set_palette_at(1, old_color)
    def get_linesize(self):
        return self.glyph_rects[0].h
    def get_glyph_width(self, ch):
        index = ord(ch) - ord(' ')
        return self.glyph_rects[index].w

class TTF:
    def __init__(self, name, size):
        self.pg_font = pygame.font.Font(name, size)
        self.cached_chars = {}
    def draw_glyph(self, dst, x, y, color, ch):
        # Make a quick integer key for this glyph: 0xRRGGBB + (ch<<24)
        key = (color[0]<<16) | (color[1]<<8) | color[2]
        key |= ord(ch) << 24

        # Cache it
        if key not in self.cached_chars:
            self.cached_chars[key] = self.pg_font.render(ch, True, color)

        # Draw it
        surf = self.cached_chars[key]
        dst.blit(surf, (x, y))
    def get_linesize(self):
        return self.pg_font.get_linesize()
    def get_glyph_width(self, ch):
        return self.pg_font.metrics(ch)[0][4]
