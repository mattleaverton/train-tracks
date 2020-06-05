from typing import List

import pygame
import pygame.freetype

from tracks.bezier import Track, Rotate
from tracks.vector import Vector

SCREEN_DIMENSIONS = (800, 800)


def draw_grid() -> pygame.Surface:
    background = pygame.Surface(SCREEN_DIMENSIONS)
    background = background.convert()
    # background.fill([200, 200, 200])
    background.fill([30, 30, 30])

    for x in range(background.get_width()):
        if x == 0:
            continue
        pygame.draw.line(background, grid_color, (x * step[0], 0), (x * step[0], SCREEN_DIMENSIONS[0]), 1)

    for y in range(background.get_height()):
        if y == 0:
            continue
        pygame.draw.line(background, grid_color, (0, y * step[1]), (background.get_width(), y * step[1]), 1)

    return background


def draw_point(point: Vector, dim=(10, 10)):
    point_center = ((point.x * step[0]) - dim[0] / 2.,
                    (SCREEN_DIMENSIONS[0] - (point.y * step[1])) - dim[1] / 2.)
    # pygame.draw.rect(Screen(), color, pygame.Rect(point_center[0], point_center[1], dim[0], dim[1]))
    return pygame.Rect(point_center[0], point_center[1], dim[0], dim[1])


def draw_track(tracks: List[Track]) -> pygame.Surface:
    track = pygame.Surface(SCREEN_DIMENSIONS, pygame.SRCALPHA, 32)
    track = track.convert_alpha()
    rects = []
    for cv in tracks:
        rects.extend(draw_curve(cv))
    for r in rects:
        pygame.draw.rect(track, (255, 0, 0), r)

    return track


def draw_curve(curve: Track, handles: bool = True):
    steps = curve.precision
    timestep = 1.0 / steps

    # if handles:
    #     for point in curve.handles:
    #         draw_point(point, (255, 0, 0))

    rects = []
    for stp in range(steps):
        if stp == 0:
            continue
        rects.append(draw_point(curve.get_point(timestep * stp), dim=(2, 2)))
    return rects


class Train(object):
    def __init__(self):
        pass


if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_DIMENSIONS)

    grid_dimensions = (10, 10)
    step = (screen.get_width() / grid_dimensions[0], screen.get_height() / grid_dimensions[1])
    grid_color = (50, 50, 50)

    clock = pygame.time.Clock()

    curves = [
        Track((2, 4), "angle", Rotate.deg_0),
        # Track((2, 4), "straight", Rotate.deg_0),
        Track((3, 4), "straight", Rotate.deg_90),
        Track((4, 4), "straight", Rotate.deg_90),
        Track((5, 5), "angle", Rotate.deg_180, reverse=True),
        Track((6, 6), "angle", Rotate.deg_0),
        Track((7, 6), "angle", Rotate.deg_90),
        Track((7, 5), "straight", Rotate.deg_180),
        Track((7, 4), "straight", Rotate.deg_180),
        Track((7, 3), "straight", Rotate.deg_180),
        Track((7, 2), "angle", Rotate.deg_180),
        Track((6, 2), "straight", Rotate.deg_270),
        Track((5, 2), "straight", Rotate.deg_270),
        Track((4, 2), "straight", Rotate.deg_270),
        Track((3, 2), "straight", Rotate.deg_270),
        Track((2, 2), "angle", Rotate.deg_270),
        Track((2, 3), "straight", Rotate.deg_0),
    ]

    grid = draw_grid()
    tracks = draw_track(curves)
    grid.blit(tracks, (0, 0))
    screen.blit(grid, (0, 0))

    # train_color = (0, 0, 0)
    # train_color = (255, 255, 255)
    # train_color = (255, 0, 0)  # red
    # train_color = (0, 255, 0)  # green
    train_color = (0, 0, 255)  # blue
    # train_color = (255, 192, 203)  # pink
    # train_color = (255, 165, 0)  # orange
    # train_color = (128, 0, 128)  # purple
    # train_color = (255, 255, 0)  # yellow
    dt = 0
    pos = 0.0
    speed = 3.0
    active_curve = 0
    done = False

    tr = draw_point(curves[active_curve].get_point(pos), dim=(25, 25))
    pygame.draw.rect(screen, train_color, tr)
    pygame.display.flip()

    while not done:
        screen.blit(grid, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        pos += speed * (dt / 1000.0)
        if pos >= 1.0:
            pos = 0.0
            active_curve += 1
            if active_curve >= len(curves):
                active_curve = 0
        screen.blit(grid, tr, tr)
        tr = draw_point(curves[active_curve].get_point(pos), dim=(25, 25))
        pygame.draw.rect(screen, train_color, tr)
        pygame.display.flip()
        dt = clock.tick(60)
