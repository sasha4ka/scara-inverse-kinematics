# Inverse kinematics for SCARA robotic arm

## Tech stack:
- Python 3.12
- Pygame
- The built-in math module

## Algorithm:
1. We need to find the intersection of two circles: $$x^2+y^2=F^2  \tag 1$$ $$(x-target_x)^2+(y-target_y)^2=S^2 \tag 2$$
2. In general there are 2 intersections on the radical axis (except in the case when $|target| = F + S$, then there is only 1 solution)
3. By subtracting (1) and (2) we get the radical axis equation: $$ target_x \cdot x + target_y \cdot y = c$$ where $$ c = \frac {F^2 + d^2 - S^2} {2}$$ $$ d ^ 2 = |target|^2 = target_x ^2 + target_y ^ 2 $$
4. Points have coordinates: $$ x = \frac {c \cdot target_x \pm target_y \cdot \sqrt {F^2d^2-c^2}} {d^2}$$ $$ y = \frac {c \cdot target_y \mp target_x \cdot \sqrt {F^2d^2-c^2}} {d^2}$$
5. For x, we take the plus sign if $target_x > 0$, and the minus sign otherwise 