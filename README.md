# pmtext

This package draws text in the style of the game Paper Mario.  It
supports coloring and jittering text.  The code is mostly decoupled from
pygame, and pygame is actually unnecessary if you're OK with writing
your own font class.  So, if you want this kind of functionality in your
OpenGL app, go for it!  Glyph drawing classes are ridiculously short
(see util_pygame.py for an example).

So, how do you use `pmtext`?

There are two important modules.

    import pmtext.para        # General stuff
    import pmtext.util_pygame # Pygame-specific stuff

I'll show you how to use them.  Grab a cool font from dafont.com and
make sure it's in the TTF format.  Then, plop in into the same folder
as your Python code.  Let's write a script:

    import pygame
    import pmtext.para
    import pmtext.util_pygame

    # Initialize Pygame
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.font.init()

    # pmtext font
    font = pmtext.util_pygame.TTF('FONT_NAME.ttf', 12)

This script loads a font, but does nothing.  Let's fix that.

    # Continued from above
    p = pmtext.para.Graph(font)

    p.color(0, 0, 0)
    p.string('Hello ')
    p.color(255, 0, 0)
    p.string('world')
    p.color(0, 0, 0)
    p.string('.')

You now have a paragraph that can be drawn on any Pygame surface.  I
like to draw text onto the window, for everyone to see.  Let's do that.

    # Draw a white background
    screen.fill((255, 255, 255))

    # Draw a paragraph
    p.draw(screen, 0, 0)

    # Update the window
    pygame.display.flip()

    # Wait a bit
    pygame.time.wait(2000)

Now run the script.  You should see some cool text.

That's almost all there is.  Read on if you want a typewriter effect
or glyph jittering.

## Typewriter Effect

That is, text that appears over time.  The typewriter effect can be
added by wrapping a `pmtext.para.Graph` in a `pmtext.para.Typewriter`.

    p = pmtext.para.Graph(font)
    t = pmtext.para.Typewriter(p)

    # Queue up some content for the typewriter
    t.color(0, 0, 0)
    t.string('Hello world.')
    t.newline()
    t.wait(10)
    t.string('Are you flat?')

Then, every frame, send the typewriter a `pulse` message before
drawing.

    t.pulse()
    t.draw(screen, 0, 0)

## Jittery glyphs

This is an absolute MUST for an RPG.  Well, not really, but it
adds new dimensions to dialogue and can come in handy.  What
you've gotta do is write a function that returns some kind of
offset for the glyph to be drawn at.

    import random

    # The current frame/step of the game.
    # Increment every time you call pygame.display.flip()
    game_frame = 0

    def jitter(char_index):
        '''Angry text motion.'''
        x = random.randint(0, 1)
        y = random.randint(0, 1)
        return x, y

    def singsong(char_index):
        '''Happy text motion.'''
        x = math.cos(float(game_frame + char_index) / 2)
        y = math.sin(float(game_frame + char_index) / 2)
        return x, y

    p = pmtext.para.Graph()

    p.shake(jitter)
    p.string('Hello ')

    p.shake(singsong)
    p.string('World')

    p.shake(None)
    p.string('!  Now back to normal.')

The shake functions always take one argument, char_index, which
is the current character index in the paragraph.

## License

The `pmtext` module is licensed under the WTFPL.  You can use it
for whatever you want.
