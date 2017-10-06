import cubehelper
import random
import math

def rainbow(iter,step):
    def compo(pattArray,angle):
        for num in pattArray["high"]:
            if (angle >= num[0]) and (angle <= num[1]):
                comp = 1.0

        for num in pattArray["low"]:
            if (angle >= num[0]) and (angle <= num[1]):
                comp = 0.0

        for num in pattArray["up"]:
            if (angle >= num[0]) and (angle <= num[1]):
                comp = (angle - num[0])/(num[1]-num[0]+0.0)

        for num in pattArray["down"]:
            if (angle >= num[0]) and (angle <= num[1]):
                comp = (num[1] - angle)/(num[1]-num[0]+0.0)

        return comp

    angle = (iter*step)%360

    b = {
    "high": [[180, 299]],
    "low":  [[0, 119]],
    "up": [[120, 179]],
    "down": [[300, 359]]
    }

    r = { 
    "high": [[300, 359], [0, 59]], 
    "low": [[120, 239]], 
    "up": [[240, 299]], 
    "down": [[60, 119]] 
    }

    g = {
    "high": [[60, 179]],
    "low": [[240, 359]],
    "up": [[0, 59]],
    "down": [[180, 239]]
    }

    return (compo(r,angle), compo(g,angle), compo(b,angle))

class Pattern(object):
    def init(self):
        self.iter = 1
        self.delta = 1
        self.sinwidth = 0.3
        self.color = cubehelper.random_color()
        self.prevColor = cubehelper.random_color()
        
        return 1.0/16

    def tick(self):
        self.cube.clear()
        color = cubehelper.mix_color(self.prevColor, self.color, (math.sin(self.sinwidth*self.iter) + 1 )/2)
        ran = random.randrange(100)

        for x in range(0, self.cube.size):
            for y in range(0, self.cube.size):
                z = math.floor(math.sin(self.sinwidth*(self.iter+(x+y)))*3.2+4)
                self.cube.set_pixel((x, y, int(z)), rainbow(self.iter+x, 10))

        self.iter += self.delta
        if (math.sin(self.sinwidth*self.iter)+1)/2 < 0.1:
            self.prevColor = self.color
            self.color = cubehelper.random_color()

        raise StopIteration
