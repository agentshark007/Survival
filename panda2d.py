import pygame
from enum import Enum

class Key(Enum):
    # Letters
    A = pygame.K_a
    B = pygame.K_b
    C = pygame.K_c
    D = pygame.K_d
    E = pygame.K_e
    F = pygame.K_f
    G = pygame.K_g
    H = pygame.K_h
    I = pygame.K_i
    J = pygame.K_j
    K = pygame.K_k
    L = pygame.K_l
    M = pygame.K_m
    N = pygame.K_n
    O = pygame.K_o
    P = pygame.K_p
    Q = pygame.K_q
    R = pygame.K_r
    S = pygame.K_s
    T = pygame.K_t
    U = pygame.K_u
    V = pygame.K_v
    W = pygame.K_w
    X = pygame.K_x
    Y = pygame.K_y
    Z = pygame.K_z
    # Numbers
    NUM_0 = pygame.K_0
    NUM_1 = pygame.K_1
    NUM_2 = pygame.K_2
    NUM_3 = pygame.K_3
    NUM_4 = pygame.K_4
    NUM_5 = pygame.K_5
    NUM_6 = pygame.K_6
    NUM_7 = pygame.K_7
    NUM_8 = pygame.K_8
    NUM_9 = pygame.K_9
    # Function keys
    F1 = pygame.K_F1
    F2 = pygame.K_F2
    F3 = pygame.K_F3
    F4 = pygame.K_F4
    F5 = pygame.K_F5
    F6 = pygame.K_F6
    F7 = pygame.K_F7
    F8 = pygame.K_F8
    F9 = pygame.K_F9
    F10 = pygame.K_F10
    F11 = pygame.K_F11
    F12 = pygame.K_F12
    # Arrows
    LEFT = pygame.K_LEFT
    RIGHT = pygame.K_RIGHT
    UP = pygame.K_UP
    DOWN = pygame.K_DOWN
    # Modifiers
    LSHIFT = pygame.K_LSHIFT
    RSHIFT = pygame.K_RSHIFT
    LCTRL = pygame.K_LCTRL
    RCTRL = pygame.K_RCTRL
    LALT = pygame.K_LALT
    RALT = pygame.K_RALT
    LSUPER = pygame.K_LSUPER
    RSUPER = pygame.K_RSUPER
    # Other common keys
    SPACE = pygame.K_SPACE
    RETURN = pygame.K_RETURN
    ENTER = pygame.K_RETURN
    ESCAPE = pygame.K_ESCAPE
    TAB = pygame.K_TAB
    BACKSPACE = pygame.K_BACKSPACE
    CAPSLOCK = pygame.K_CAPSLOCK
    INSERT = pygame.K_INSERT
    DELETE = pygame.K_DELETE
    HOME = pygame.K_HOME
    END = pygame.K_END
    PAGEUP = pygame.K_PAGEUP
    PAGEDOWN = pygame.K_PAGEDOWN
    # Symbols
    MINUS = pygame.K_MINUS
    EQUALS = pygame.K_EQUALS
    LEFTBRACKET = pygame.K_LEFTBRACKET
    RIGHTBRACKET = pygame.K_RIGHTBRACKET
    BACKSLASH = pygame.K_BACKSLASH
    SEMICOLON = pygame.K_SEMICOLON
    APOSTROPHE = pygame.K_QUOTE
    GRAVE = pygame.K_BACKQUOTE
    COMMA = pygame.K_COMMA
    PERIOD = pygame.K_PERIOD
    SLASH = pygame.K_SLASH
    # Keypad
    KP0 = pygame.K_KP0
    KP1 = pygame.K_KP1
    KP2 = pygame.K_KP2
    KP3 = pygame.K_KP3
    KP4 = pygame.K_KP4
    KP5 = pygame.K_KP5
    KP6 = pygame.K_KP6
    KP7 = pygame.K_KP7
    KP8 = pygame.K_KP8
    KP9 = pygame.K_KP9
    KP_PERIOD = pygame.K_KP_PERIOD
    KP_DIVIDE = pygame.K_KP_DIVIDE
    KP_MULTIPLY = pygame.K_KP_MULTIPLY
    KP_MINUS = pygame.K_KP_MINUS
    KP_PLUS = pygame.K_KP_PLUS
    KP_ENTER = pygame.K_KP_ENTER
    KP_EQUALS = pygame.K_KP_EQUALS

class Color:
    """RGBA color with 0=transparent, 100=opaque for alpha."""

    def __init__(self, r: int, g: int, b: int, a: float = 100):
        self.r = max(0, min(255, r))
        self.g = max(0, min(255, g))
        self.b = max(0, min(255, b))
        self.a = max(0, min(255, int(a * 255 / 100)))

    def to_tuple(self):
        return (self.r, self.g, self.b, self.a)


class Image:
    """Wrapper for loading images."""

    def __init__(self, path: str):
        try:
            self.surface = pygame.image.load(path).convert_alpha()
        except Exception as e:
            print(f"Failed to load image '{path}': {e}")
            self.surface = pygame.Surface((1, 1), pygame.SRCALPHA)


class Sound:
    """Wrapper for loading sounds."""

    def __init__(self, path: str):
        try:
            self.sound = pygame.mixer.Sound(path)
        except Exception as e:
            print(f"Failed to load sound '{path}': {e}")
            self.sound = None


class Resizable(Enum):
    NONE = "none"
    WIDTH = "width"
    HEIGHT = "height"
    BOTH = "both"
    ASPECT = "aspect"


class Anchor(Enum):
    CENTER = "center"
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    TOPLEFT = "topleft"
    TOPRIGHT = "topright"
    BOTTOMLEFT = "bottomleft"
    BOTTOMRIGHT = "bottomright"


class PandaWindow:
    """Base window class with anchor-based coordinates."""

    def __init__(
        self,
        width: int = 800,
        height: int = 600,
        title: str = "Panda2D Window",
        resizable: Resizable = Resizable.NONE,
        anchor: Anchor = Anchor.CENTER,
    ):
        pygame.init()
        try:
            pygame.mixer.init()
        except Exception:
            pass

        self.width = width
        self.height = height
        self.title = title
        self.resizable = resizable
        self.anchor = anchor
        self._flags = pygame.RESIZABLE if resizable != Resizable.NONE else 0
        self._base_width = width
        self._base_height = height

        self.screen = pygame.display.set_mode((width, height), self._flags)
        pygame.display.set_caption(title)
        self.clock = pygame.time.Clock()
        self.running = False
        self.mousex = 0
        self.mousey = 0
        self.deltatime = 0.0
        self._fonts = {}
        self.mousedownprimary = False
        self.mousedownmiddle = False
        self.mousedownsecondary = False

    def start(self):
        self.running = True
        self.initialize()

        while self.running:
            self.deltatime = self.clock.tick(60) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.VIDEORESIZE:
                    self._handle_resize(event.w, event.h)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.mousedownprimary = True
                    elif event.button == 2:
                        self.mousedownmiddle = True
                    elif event.button == 3:
                        self.mousedownsecondary = True
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        self.mousedownprimary = False
                    elif event.button == 2:
                        self.mousedownmiddle = False
                    elif event.button == 3:
                        self.mousedownsecondary = False

            mx, my = pygame.mouse.get_pos()
            ox, oy = self._get_anchor_offset()
            self.mousex = mx - ox
            self.mousey = -(my - oy)

            self.update()
            self.draw()
            pygame.display.flip()

        pygame.quit()
        pygame.mixer.quit()
    def keydown(self, key: 'Key') -> bool:
        """Returns True if the specified Key enum is currently pressed down."""
        keys = pygame.key.get_pressed()
        return keys[key.value]

    def _handle_resize(self, w: int, h: int):
        if self.resizable == Resizable.NONE:
            return
        elif self.resizable == Resizable.WIDTH:
            h = self.height
        elif self.resizable == Resizable.HEIGHT:
            w = self.width
        elif self.resizable == Resizable.ASPECT:
            ratio = self._base_width / self._base_height
            if w / h > ratio:
                w = int(h * ratio)
            else:
                h = int(w / ratio)

        self.width, self.height = w, h
        self.screen = pygame.display.set_mode((w, h), self._flags)

    def _get_anchor_offset(self) -> tuple[int, int]:
        mapping = {
            Anchor.CENTER: (self.width // 2, self.height // 2),
            Anchor.TOP: (self.width // 2, 0),
            Anchor.BOTTOM: (self.width // 2, self.height),
            Anchor.LEFT: (0, self.height // 2),
            Anchor.RIGHT: (self.width, self.height // 2),
            Anchor.TOPLEFT: (0, 0),
            Anchor.TOPRIGHT: (self.width, 0),
            Anchor.BOTTOMLEFT: (0, self.height),
            Anchor.BOTTOMRIGHT: (self.width, self.height),
        }
        return mapping.get(self.anchor, (self.width // 2, self.height // 2))

    def _to_screen(self, x: float, y: float) -> tuple[int, int]:
        ox, oy = self._get_anchor_offset()
        return int(ox + x), int(oy - y)

    def _rect_from_points(self, ax: float, ay: float, bx: float, by: float) -> pygame.Rect:
        x1, y1 = self._to_screen(ax, ay)
        x2, y2 = self._to_screen(bx, by)
        left = min(x1, x2)
        top = min(y1, y2)
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        return pygame.Rect(left, top, width, height)

    def _get_anchor_pos(self, x: float, y: float, w: int, h: int, anchor: Anchor) -> tuple[int, int]:
        sx, sy = self._to_screen(x, y)
        offsets = {
            Anchor.CENTER: (sx - w // 2, sy - h // 2),
            Anchor.TOP: (sx - w // 2, sy - h),
            Anchor.BOTTOM: (sx - w // 2, sy),
            Anchor.LEFT: (sx, sy - h // 2),
            Anchor.RIGHT: (sx - w, sy - h // 2),
            Anchor.TOPLEFT: (sx, sy - h),
            Anchor.TOPRIGHT: (sx - w, sy - h),
            Anchor.BOTTOMLEFT: (sx, sy),
            Anchor.BOTTOMRIGHT: (sx - w, sy),
        }
        return offsets.get(anchor, (sx - w // 2, sy - h // 2))

    # ----------------- Override in subclasses -----------------
    def initialize(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    # ----------------- Drawing Helpers -----------------
    def clear(self, color: Color = Color(255, 255, 255)):
        if color.a == 255:
            self.screen.fill(color.to_tuple())
        else:
            temp = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            temp.fill(color.to_tuple())
            self.screen.blit(temp, (0, 0))

    def fill_rect(self, ax, ay, bx, by, color: Color, outline_thickness=0, outline_color: Color = None):
        rect = self._rect_from_points(ax, ay, bx, by)
        if color.a == 255:
            pygame.draw.rect(self.screen, color.to_tuple(), rect)
        else:
            temp = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pygame.draw.rect(temp, color.to_tuple(), pygame.Rect(0, 0, rect.width, rect.height))
            self.screen.blit(temp, (rect.left, rect.top))
        if outline_thickness > 0 and outline_color:
            pygame.draw.rect(self.screen, outline_color.to_tuple(), rect, outline_thickness)

    def draw_rect(self, ax, ay, bx, by, outline_thickness=1, outline_color: Color = None):
        rect = self._rect_from_points(ax, ay, bx, by)
        pygame.draw.rect(self.screen, outline_color.to_tuple() if outline_color else (0, 0, 0), rect, outline_thickness)

    def fill_circle(self, x, y, width, height, color: Color, outline_thickness=0, outline_color: Color = None):
        sx, sy = self._to_screen(x, y)
        temp = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.ellipse(temp, color.to_tuple(), pygame.Rect(0, 0, width, height))
        if outline_thickness > 0 and outline_color:
            pygame.draw.ellipse(temp, outline_color.to_tuple(), pygame.Rect(0, 0, width, height), outline_thickness)
        self.screen.blit(temp, (sx - width // 2, sy - height // 2))

    def draw_circle(self, x, y, width, height, outline_thickness=1, outline_color: Color = None):
        sx, sy = self._to_screen(x, y)
        temp = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.ellipse(temp, outline_color.to_tuple() if outline_color else (0, 0, 0),
                            pygame.Rect(0, 0, width, height), outline_thickness)
        self.screen.blit(temp, (sx - width // 2, sy - height // 2))

    def fill_polygon(self, xlist, ylist, color: Color, outline_thickness=0, outline_color: Color = None):
        points = [self._to_screen(x, y) for x, y in zip(xlist, ylist)]
        xs, ys = zip(*points)
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        temp = pygame.Surface((max_x - min_x + 1, max_y - min_y + 1), pygame.SRCALPHA)
        shifted_points = [(px - min_x, py - min_y) for px, py in points]
        pygame.draw.polygon(temp, color.to_tuple(), shifted_points)
        if outline_thickness > 0 and outline_color:
            pygame.draw.polygon(temp, outline_color.to_tuple(), shifted_points, outline_thickness)
        self.screen.blit(temp, (min_x, min_y))

    def draw_polygon(self, xlist, ylist, outline_thickness=1, outline_color: Color = None):
        points = [self._to_screen(x, y) for x, y in zip(xlist, ylist)]
        pygame.draw.polygon(self.screen, outline_color.to_tuple() if outline_color else (0, 0, 0), points, outline_thickness)

    def draw_line(self, x1, y1, x2, y2, color: Color, thickness=1):
        if color.a == 255:
            pygame.draw.line(self.screen, color.to_tuple(), self._to_screen(x1, y1), self._to_screen(x2, y2), thickness)
        else:
            x1s, y1s = self._to_screen(x1, y1)
            x2s, y2s = self._to_screen(x2, y2)
            temp_width = abs(x2s - x1s) + thickness*2
            temp_height = abs(y2s - y1s) + thickness*2
            temp = pygame.Surface((temp_width, temp_height), pygame.SRCALPHA)
            pygame.draw.line(temp, color.to_tuple(), 
                             (x1s - min(x1s, x2s) + thickness, y1s - min(y1s, y2s) + thickness),
                             (x2s - min(x1s, x2s) + thickness, y2s - min(y1s, y2s) + thickness),
                             thickness)
            self.screen.blit(temp, (min(x1s, x2s) - thickness, min(y1s, y2s) - thickness))

    def draw_text(self, text, x, y, font_name=None, font_size=24, color: Color = None, anchor=Anchor.CENTER):
        font_key = (font_name, font_size)
        if font_key not in self._fonts:
            self._fonts[font_key] = pygame.font.SysFont(font_name, font_size)
        surf = self._fonts[font_key].render(text, True, color.to_tuple() if color else (0, 0, 0))
        px, py = self._get_anchor_pos(x, y, surf.get_width(), surf.get_height(), anchor)
        self.screen.blit(surf, (px, py))

    def draw_image(self, image: Image, x, y, anchor=Anchor.CENTER, xscale=1.0, yscale=1.0, outline_thickness=0, outline_color: Color = None):
        img = pygame.transform.scale(image.surface, (int(image.surface.get_width() * xscale),
                                                     int(image.surface.get_height() * yscale)))
        px, py = self._get_anchor_pos(x, y, img.get_width(), img.get_height(), anchor)
        self.screen.blit(img, (px, py))
        if outline_thickness > 0 and outline_color:
            rect = pygame.Rect(px, py, img.get_width(), img.get_height())
            pygame.draw.rect(self.screen, outline_color.to_tuple(), rect, outline_thickness)

    def play_sound(self, sound: Sound):
        if sound.sound:
            sound.sound.play()
