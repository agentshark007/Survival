import pygame
from enum import Enum


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

            mx, my = pygame.mouse.get_pos()
            ox, oy = self._get_anchor_offset()
            self.mousex = mx - ox
            self.mousey = -(my - oy)

            self.update()
            self.draw()
            pygame.display.flip()

        pygame.quit()
        pygame.mixer.quit()

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
