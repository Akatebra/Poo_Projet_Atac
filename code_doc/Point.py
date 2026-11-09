class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def toStr(self):
        return f"{self.x},{self.y}"


if __name__ == "__main__":
    p = Point(2.337306, 48.849319)
    print(p.toStr())