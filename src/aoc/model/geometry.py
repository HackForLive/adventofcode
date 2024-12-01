from pydantic import BaseModel


class Point2D(BaseModel):
    """
    Represents point using cartesian coordinates of two-dimensional space
    """
    x: int
    y: int

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.x == other.x and
            self.y == other.y
        )

    def __add__(self, o):
        return Point2D(x=self.x+o.x, y=self.y + o.y)


class Point3D(BaseModel):
    """
    Represents point using cartesian coordinates of three-dimensional space
    """
    x: int
    y: int
    z: int

    def __repr__(self):
        return f"P({self.x}, {self.y}, {self.z})"

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __eq__(self, other):
        return (
            self.__class__ == other.__class__ and
            self.x == other.x and
            self.y == other.y and
            self.z == other.z
        )
