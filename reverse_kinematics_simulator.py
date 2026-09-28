import math

import pygame

# -----------------------------
#           SETTINGS
# -----------------------------

# window parameters
OFFSET = 50
SCALE = 0.5

# physics parameters
FIRST_ARM = 400
SECOND_ARM = 400
WORKSPACE = FIRST_ARM + SECOND_ARM
BASE_POINT = (WORKSPACE, WORKSPACE + OFFSET)

# colors
JOINTS_COLOR = (33, 158, 163)
ARMS_COLOR = (149, 202, 204)
BG_COLOR = (232, 232, 232)
ARM_RANGE_COLOR = (181, 181, 181)


def scale_point(
    p: tuple[int | float, int | float], rev: bool = False
) -> tuple[int, int]:
    scale = 1 / SCALE if rev else SCALE
    return (int(p[0] * scale), int(p[1] * scale))


def draw(points: list[tuple[int, int]], surf: pygame.Surface):
    points = [scale_point(p) for p in points]

    pygame.draw.line(surf, ARMS_COLOR, points[0], points[1], 2)
    pygame.draw.line(surf, ARMS_COLOR, points[1], points[2], 2)

    pygame.draw.circle(surf, JOINTS_COLOR, points[0], 10)
    pygame.draw.circle(surf, JOINTS_COLOR, points[1], 8)
    pygame.draw.circle(surf, JOINTS_COLOR, points[2], 8)


def calculate(
    base: tuple[int, int], target: tuple[int, int]
) -> tuple[list[tuple[int, int]], tuple[float, float]] | None:
    offset = (target[0] - base[0], target[1] - base[1])

    d2 = offset[0] * offset[0] + offset[1] * offset[1]
    c = 0.5 * (FIRST_ARM * FIRST_ARM + d2 - SECOND_ARM * SECOND_ARM)

    sq = FIRST_ARM * FIRST_ARM * d2 - c * c

    if sq < 0:
        return None

    if sq == 0:
        x = c * offset[0] / d2
        y = c * offset[1] / d2
        angle = math.atan2(x, -y) / math.pi * 180
        return [base, (int(x) + base[0], int(y) + base[1]), target], (angle, angle)

    sqrt = math.sqrt(sq)

    if offset[0] > 0:
        x = (c * offset[0] + offset[1] * sqrt) / d2
        y = (c * offset[1] - offset[0] * sqrt) / d2
    else:
        x = (c * offset[0] - offset[1] * sqrt) / d2
        y = (c * offset[1] + offset[0] * sqrt) / d2

    alpha = math.atan2(x, -y) / math.pi * 180
    teta = math.atan2(offset[0] - x, y - offset[1]) / math.pi * 180 - alpha

    return [base, (int(x) + base[0], int(y) + base[1]), target], (alpha, teta)


pygame.display.init()
pygame.font.init()

target = (WORKSPACE, OFFSET)
timer = pygame.time.Clock()
font = pygame.font.Font(None, 30)

window = pygame.display.set_mode(scale_point((2 * WORKSPACE, WORKSPACE + OFFSET)))
pygame.display.set_caption("SCARA reverse kinematics")

run = True
while run:
    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                run = False
            case _:
                pass
    if pygame.mouse.get_pressed()[0]:
        target = scale_point(pygame.mouse.get_pos(), rev=True)

        offset = (target[0] - BASE_POINT[0], target[1] - BASE_POINT[1])
        d2 = offset[0] * offset[0] + offset[1] * offset[1]

        if d2 > (FIRST_ARM + SECOND_ARM) * (FIRST_ARM + SECOND_ARM):
            angle = math.atan2(-offset[1], offset[0])
            target = (
                BASE_POINT[0] + (FIRST_ARM + SECOND_ARM - 3) * math.cos(angle),
                BASE_POINT[1] - (FIRST_ARM + SECOND_ARM - 3) * math.sin(angle),
            )

    res = calculate(BASE_POINT, target)

    window.fill(BG_COLOR)
    pygame.draw.circle(
        window,
        ARM_RANGE_COLOR,
        scale_point(BASE_POINT),
        (FIRST_ARM + SECOND_ARM) * SCALE,
    )

    if not res:
        title = "could not resolve"
        pygame.draw.circle(window, JOINTS_COLOR, scale_point(BASE_POINT), 10)
        pygame.draw.circle(window, JOINTS_COLOR, scale_point(target), 8)
    else:
        points, (alpha, teta) = res
        title = f"{alpha=:.1f}    {teta=:.1f}"
        draw(points, window)

    rendered = font.render(title, 1, (0, 0, 0))
    pos = ((WORKSPACE - rendered.get_width()) / 2, 0)
    window.blit(rendered, scale_point(pos))

    pygame.display.flip()
    timer.tick(40)
