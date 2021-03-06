"python wrappers for the vision library"

import ctypes

VISION = None

try:
    VISION = ctypes.cdll.LoadLibrary("./build/libvision.so")
except OSError:
    pass

try:
    VISION = ctypes.cdll.LoadLibrary("./build/libvision.dylib")
except OSError:
    pass

try:
    VISION = ctypes.cdll.LoadLibrary("./build/libvision.dll")
except OSError:
    pass

if VISION is None:
    raise OSError

YELLOW = ctypes.c_ubyte.in_dll(VISION, "YELLOW").value
RED = ctypes.c_ubyte.in_dll(VISION, "RED").value
ERROR = ctypes.c_ubyte.in_dll(VISION, "ERROR").value

class CTriangle(ctypes.Structure):
    "ctypes wrapper for Triangle struct in vision"
    pass

class CTriangleIterator(ctypes.Structure):
    "ctypes wrapper for opaque TriangleIterator"
    pass


HASNEXT = VISION.hasNext
HASNEXT.argtypes = [ctypes.POINTER(CTriangleIterator)]
HASNEXT.restype = ctypes.c_bool

NEXT = VISION.next
NEXT.argtypes = [ctypes.POINTER(CTriangleIterator)]
NEXT.restype = ctypes.POINTER(CTriangle)

GETTRIANGLES = VISION.getTriangles
GETTRIANGLES.argtypes = []
GETTRIANGLES.restype = ctypes.POINTER(CTriangleIterator)

DELETEITER = VISION.deleteTriangleIterator
DELETEITER.argtypes = [ctypes.POINTER(CTriangleIterator)]
DELETEITER.restype = None

CHECKCOLOR = VISION.vision_check_color
CHECKCOLOR.argtypes = []
CHECKCOLOR.restype = ctypes.c_ubyte

GETX = VISION.getX
GETX.argtypes = [ctypes.POINTER(CTriangle)]
GETX.restype = ctypes.c_float

GETY = VISION.getY
GETY.argtypes = [ctypes.POINTER(CTriangle)]
GETY.restype = ctypes.c_float

GETZ = VISION.getZ
GETZ.argtypes = [ctypes.POINTER(CTriangle)]
GETZ.restype = ctypes.c_float

GETCOLOR = VISION.getColor
GETCOLOR.argtypes = [ctypes.POINTER(CTriangle)]
GETCOLOR.restype = ctypes.c_ubyte

GETHORIZ = VISION.getHorizontal
GETHORIZ.argtypes = [ctypes.POINTER(CTriangle)]
GETHORIZ.restype = ctypes.c_bool

TAKEPIC = VISION.vision_write_picture
TAKEPIC.argtypes = []
TAKEPIC.restype = None

class Triangle(object):
    "python triangle class"

    def __init__(self, ctriangleref):
        "initialize from CTriangle"
        self.xpos = GETX(ctriangleref)
        self.ypos = GETY(ctriangleref)
        self.zpos = GETZ(ctriangleref)
        self.color = GETCOLOR(ctriangleref)
        self.horizontal = GETHORIZ(ctriangleref)

def get_triangles():
    "Iterator over all triangles as Python object.."
    iterator = GETTRIANGLES()
    while HASNEXT(iterator):
        yield Triangle(NEXT(iterator))

    DELETEITER(iterator)

def check_color():
    "wrap c checkcolor funtion"
    return CHECKCOLOR().value

def take_and_save_picture():
    "take picture and save it to current working directory"
    TAKEPIC()
