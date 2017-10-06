# Colour alternate pixels in two colours
# Copyright (C) Liz Lyon <@lizzipfish>
# Released under the terms of the GNU General Public License version 3

import cubehelper

maxTicks = 9

class Pattern(object):
    def init(self):
        self.double_buffer = True
        self.colors = [cubehelper.random_color(),cubehelper.random_color()]
        self.tickCount = 0
        return 0.6
    def tick(self):
        self.cube.clear()
        self.tickCount += 1
        mod = self.tickCount % 2

        for y in range(0, self.cube.size):
            for z in range(0, self.cube.size):
                for x in range(0, self.cube.size):
                    if x % 2 == mod and y % 2 == mod and z % 2 == mod:
                        self.cube.set_pixel((x, y, z), self.colors[mod])

        if self.tickCount > maxTicks:
            raise StopIteration