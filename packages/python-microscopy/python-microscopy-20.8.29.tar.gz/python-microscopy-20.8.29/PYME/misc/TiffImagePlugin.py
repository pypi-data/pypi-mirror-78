#
# The Python Imaging Library.
# $Id$
#
# TIFF file handling
#
# TIFF is a flexible, if somewhat aged, image file format originally
# defined by Aldus.  Although TIFF supports a wide variety of pixel
# layouts and compression methods, the name doesn't really stand for
# "thousands of incompatible file formats," it just feels that way.
#
# To read TIFF data from a stream, the stream must be seekable.  For
# progressive decoding, make sure to use TIFF files where the tag
# directory is placed first in the file.
#
# History:
# 1995-09-01 fl   Created
# 1996-05-04 fl   Handle JPEGTABLES tag
# 1996-05-18 fl   Fixed COLORMAP support
# 1997-01-05 fl   Fixed PREDICTOR support
# 1997-08-27 fl   Added support for rational tags (from Perry Stoll)
# 1998-01-10 fl   Fixed seek/tell (from Jan Blom)
# 1998-07-15 fl   Use private names for internal variables
# 1999-06-13 fl   Rewritten for PIL 1.0 (1.0)
# 2000-10-11 fl   Additional fixes for Python 2.0 (1.1)
# 2001-04-17 fl   Fixed rewind support (seek to frame 0) (1.2)
# 2001-05-12 fl   Added write support for more tags (from Greg Couch) (1.3)
# 2001-12-18 fl   Added workaround for broken Matrox library
# 2002-01-18 fl   Don't mess up if photometric tag is missing (D. Alan Stewart)
# 2003-05-19 fl   Check FILLORDER tag
# 2003-09-26 fl   Added RGBa support
# 2004-02-24 fl   Added DPI support; fixed rational write support
# 2005-02-07 fl   Added workaround for broken Corel Draw 10 files
# 2006-01-09 fl   Added support for float/double tags (from Russell Nelson)
#
# Copyright (c) 1997-2006 by Secret Labs AB.  All rights reserved.
# Copyright (c) 1995-1997 by Fredrik Lundh
#
# See the README file for information on usage and redistribution.
#

__version__ = "1.3.5"

# try:
#     import Image, ImageFile
#     import ImagePalette
# except ImportError: #Have Pillow rather than PIL

from PIL import Image, ImageFile, ImagePalette

import array, string, sys

try:
    if sys.byteorder == "little":
        byteorder = "II"
    else:
        byteorder = "MM"
except AttributeError:
    if ord(array.array("i",[1]).tostring()[0]):
        byteorder = "II"
    else:
        byteorder = "MM"

#
# --------------------------------------------------------------------
# Read TIFF files

def il16(c,o=0):
    return ord(c[o]) + (ord(c[o+1])<<8)
def il32(c,o=0):
    return ord(c[o]) + (ord(c[o+1])<<8) + (ord(c[o+2])<<16) + (ord(c[o+3])<<24)
def ol16(i):
    return chr(i&255) + chr(i>>8&255)
def ol32(i):
    return chr(i&255) + chr(i>>8&255) + chr(i>>16&255) + chr(i>>24&255)

def ib16(c,o=0):
    return ord(c[o+1]) + (ord(c[o])<<8)
def ib32(c,o=0):
    return ord(c[o+3]) + (ord(c[o+2])<<8) + (ord(c[o+1])<<16) + (ord(c[o])<<24)
def ob16(i):
    return chr(i>>8&255) + chr(i&255)
def ob32(i):
    return chr(i>>24&255) + chr(i>>16&255) + chr(i>>8&255) + chr(i&255)

# a few tag names, just to make the code below a bit more readable
IMAGEWIDTH = 256
IMAGELENGTH = 257
BITSPERSAMPLE = 258
COMPRESSION = 259
PHOTOMETRIC_INTERPRETATION = 262
FILLORDER = 266
IMAGEDESCRIPTION = 270
STRIPOFFSETS = 273
SAMPLESPERPIXEL = 277
ROWSPERSTRIP = 278
STRIPBYTECOUNTS = 279
X_RESOLUTION = 282
Y_RESOLUTION = 283
PLANAR_CONFIGURATION = 284
RESOLUTION_UNIT = 296
SOFTWARE = 305
DATE_TIME = 306
ARTIST = 315
PREDICTOR = 317
COLORMAP = 320
TILEOFFSETS = 324 #seb
EXTRASAMPLES = 338
SAMPLEFORMAT = 339
JPEGTABLES = 347
COPYRIGHT = 33432
IPTC_NAA_CHUNK = 33723 # newsphoto properties
PHOTOSHOP_CHUNK = 34377 # photoshop properties

COMPRESSION_INFO = {
    # Compression => pil compression name
    1: "raw",
    2: "tiff_ccitt",
    3: "group3",
    4: "group4",
    5: "tiff_lzw",
    6: "tiff_jpeg", # obsolete
    7: "jpeg",
    32771: "tiff_raw_16", # 16-bit padding
    32773: "packbits"
}

OPEN_INFO = {
    # (ByteOrder, PhotoInterpretation, SampleFormat, FillOrder, BitsPerSample,
    #  ExtraSamples) => mode, rawmode 
    ('l', 0, 1, 1, (1,), ()): ("1", "1;I"),
    ('l', 0, 1, 2, (1,), ()): ("1", "1;IR"),
    ('l', 0, 1, 1, (8,), ()): ("L", "L;I"),
    ('l', 0, 1, 2, (8,), ()): ("L", "L;IR"),
    ('l', 1, 1, 1, (1,), ()): ("1", "1"),
    ('l', 1, 1, 2, (1,), ()): ("1", "1;R"),
    ('l', 1, 1, 1, (8,), ()): ("L", "L"),
    ('l', 1, 1, 1, (8,8), (2,)): ("LA", "LA"),
    ('l', 1, 1, 2, (8,), ()): ("L", "L;R"),
    ('l', 1, 1, 1, (16,), ()): ("I;16", "I;16"),
    ('l', 1, 2, 1, (16,), ()): ("I;16S", "I;16S"),
    ('l', 1, 2, 1, (32,), ()): ("I", "I;32S"),
    ('l', 1, 3, 1, (32,), ()): ("F", "F;32F"),
    ('l', 2, 1, 1, (8,8,8), ()): ("RGB", "RGB"),
    ('l', 2, 1, 1, (8,8,0), ()): ("RGB", "RGB"),#seb -- found in LSM(Zeiss) files
    #('l', 2, 1, 1, (16,16,16), ()): ("RGB", "RGB"),#seb -- found in LSM(Zeiss) files
    ('l', 2, 1, 2, (8,8,8), ()): ("RGB", "RGB;R"),
    ('l', 2, 1, 1, (8,8,8,8), (0,)): ("RGBX", "RGBX"),
    ('l', 2, 1, 1, (8,8,8,8), (1,)): ("RGBA", "RGBa"),
    ('l', 2, 1, 1, (8,8,8,8), (2,)): ("RGBA", "RGBA"),
    ('l', 2, 1, 1, (8,8,8,8), (999,)): ("RGBA", "RGBA"), # corel draw 10
    ('l', 3, 1, 1, (1,), ()): ("P", "P;1"),
    ('l', 3, 1, 2, (1,), ()): ("P", "P;1R"),
    ('l', 3, 1, 1, (2,), ()): ("P", "P;2"),
    ('l', 3, 1, 2, (2,), ()): ("P", "P;2R"),
    ('l', 3, 1, 1, (4,), ()): ("P", "P;4"),
    ('l', 3, 1, 2, (4,), ()): ("P", "P;4R"),
    ('l', 3, 1, 1, (8,), ()): ("P", "P"),
    ('l', 3, 1, 1, (8,8), (2,)): ("PA", "PA"),
    ('l', 3, 1, 2, (8,), ()): ("P", "P;R"),
    ('l', 5, 1, 1, (8,8,8,8), ()): ("CMYK", "CMYK"),
    ('l', 6, 1, 1, (8,8,8), ()): ("YCbCr", "YCbCr"),
    ('l', 8, 1, 1, (8,8,8), ()): ("LAB", "LAB"),
   
    ('b', 0, 1, 1, (1,), ()): ("1", "1;I"),
    ('b', 0, 1, 2, (1,), ()): ("1", "1;IR"),
    ('b', 0, 1, 1, (8,), ()): ("L", "L;I"),
    ('b', 0, 1, 2, (8,), ()): ("L", "L;IR"),
    ('b', 1, 1, 1, (1,), ()): ("1", "1"),
    ('b', 1, 1, 2, (1,), ()): ("1", "1;R"),
    ('b', 1, 1, 1, (8,), ()): ("L", "L"),
    ('b', 1, 1, 1, (8,8), (2,)): ("LA", "LA"),
    ('b', 1, 1, 2, (8,), ()): ("L", "L;R"),
    ('b', 1, 1, 1, (16,), ()): ("I;16B", "I;16B"),
    ('b', 1, 2, 1, (16,), ()): ("I;16BS", "I;16BS"),
    ('b', 1, 2, 1, (32,), ()): ("I;32BS", "I;32BS"),
    ('b', 1, 3, 1, (32,), ()): ("F;32BF", "F;32BF"),
    ('b', 2, 1, 1, (8,8,8), ()): ("RGB", "RGB"),
    ('b', 2, 1, 2, (8,8,8), ()): ("RGB", "RGB;R"),
    ('b', 2, 1, 1, (8,8,8,8), (0,)): ("RGBX", "RGBX"),
    ('b', 2, 1, 1, (8,8,8,8), (1,)): ("RGBA", "RGBa"),
    ('b', 2, 1, 1, (8,8,8,8), (2,)): ("RGBA", "RGBA"),
    ('b', 2, 1, 1, (8,8,8,8), (999,)): ("RGBA", "RGBA"), # corel draw 10
    ('b', 3, 1, 1, (1,), ()): ("P", "P;1"),
    ('b', 3, 1, 2, (1,), ()): ("P", "P;1R"),
    ('b', 3, 1, 1, (2,), ()): ("P", "P;2"),
    ('b', 3, 1, 2, (2,), ()): ("P", "P;2R"),
    ('b', 3, 1, 1, (4,), ()): ("P", "P;4"),
    ('b', 3, 1, 2, (4,), ()): ("P", "P;4R"),
    ('b', 3, 1, 1, (8,), ()): ("P", "P"),
    ('b', 3, 1, 1, (8,8), (2,)): ("PA", "PA"),
    ('b', 3, 1, 2, (8,), ()): ("P", "P;R"),
    ('b', 5, 1, 1, (8,8,8,8), ()): ("CMYK", "CMYK"),
    ('b', 6, 1, 1, (8,8,8), ()): ("YCbCr", "YCbCr"),
    ('b', 8, 1, 1, (8,8,8), ()): ("LAB", "LAB"),
   
}

PREFIXES = ["MM\000\052", "II\052\000", "II\xBC\000"]
PREFIX_TO_BYTEORDER = {"MM":"b", "II":"l"}
BYTEORDER_TO_PREFIX = {"b":"MM", "l":"II"}
def _accept(prefix):
    return prefix[:4] in PREFIXES

##
# Wrapper for TIFF IFDs.

class ImageFileDirectory:

    # represents a TIFF tag directory.  to speed things up,
    # we don't decode tags unless they're asked for.

    def __init__(self, prefix="II"):
        self.prefix = prefix[:2]
        if self.prefix == "MM":
            self.i16, self.i32 = ib16, ib32
            self.o16, self.o32 = ob16, ob32
        elif self.prefix == "II":
            self.i16, self.i32 = il16, il32
            self.o16, self.o32 = ol16, ol32
        else:
            raise SyntaxError("not a TIFF IFD")
        self.byteorder = PREFIX_TO_BYTEORDER[self.prefix]
        self.reset()

    def reset(self):
        self.tags = {}
        self.tagdata = {}
        self.next = None

    # dictionary API (sort of)

    def keys(self):
        return self.tagdata.keys() + self.tags.keys()

    def items(self):
        items = self.tags.items()
        for tag in self.tagdata.keys():
            items.append((tag, self[tag]))
        return items

    def __len__(self):
        return len(self.tagdata) + len(self.tags)

    def __getitem__(self, tag):
        try:
            return self.tags[tag]
        except KeyError:
            type, data = self.tagdata[tag] # unpack on the fly
            size, handler = self.load_dispatch[type]
            self.tags[tag] = data = handler(self, data)
            del self.tagdata[tag]
            return data

    def get(self, tag, default=None):
        try:
            return self[tag]
        except KeyError:
            return default

    def getscalar(self, tag, default=None):
        try:
            value = self[tag]
            if len(value) != 1:
                if tag == SAMPLEFORMAT:
                    # work around broken (?) matrox library
                    # (from Ted Wright, via Bob Klimek)
                    raise KeyError # use default
                raise ValueError("not a scalar")
            return value[0]
        except KeyError:
            if default is None:
                raise
            return default

    def has_key(self, tag):
        return self.tags.has_key(tag) or self.tagdata.has_key(tag)

    def __setitem__(self, tag, value):
        if type(value) is not type(()):
            value = (value,)
        self.tags[tag] = value

    # load primitives

    load_dispatch = {}

    def load_byte(self, data):
        l = []
        for i in range(len(data)):
            l.append(ord(data[i]))
        return tuple(l)
    load_dispatch[1] = (1, load_byte)

    def load_string(self, data):
        if data[-1:] == '\0':
            data = data[:-1]
        return data
    load_dispatch[2] = (1, load_string)

    def load_short(self, data):
        l = []
        for i in range(0, len(data), 2):
            l.append(self.i16(data, i))
        return tuple(l)
    load_dispatch[3] = (2, load_short)

    def load_long(self, data):
        l = []
        for i in range(0, len(data), 4):
            l.append(self.i32(data, i))
        return tuple(l)
    load_dispatch[4] = (4, load_long)

    def load_rational(self, data):
        l = []
        for i in range(0, len(data), 8):
            l.append((self.i32(data, i), self.i32(data, i+4)))
        return tuple(l)
    load_dispatch[5] = (8, load_rational)

    def load_float(self, data):
        a = array.array("f", data)
        if self.prefix != byteorder:
            a.byteswap()
        return tuple(a)
    load_dispatch[11] = (4, load_float)

    def load_double(self, data):
        a = array.array("d", data)
        if self.prefix != byteorder:
            a.byteswap()
        return tuple(a)
    load_dispatch[12] = (8, load_double)

    def load_undefined(self, data):
        # Untyped data
        return data
    load_dispatch[7] = (1, load_undefined)

    def load(self, fp):
        # load tag dictionary

        self.reset()

        i16 = self.i16
        i32 = self.i32

        for i in range(i16(fp.read(2))):

            ifd = fp.read(12)

            tag, typ = i16(ifd), i16(ifd, 2)

            if Image.DEBUG:
                import TiffTags
                tagname = TiffTags.TAGS.get(tag, "unknown")
                typname = TiffTags.TYPES.get(typ, "unknown")
                print("tag: %s (%d)" % (tagname, tag))
                print("- type: %s (%d)" % (typname, typ))

            try:
                dispatch = self.load_dispatch[typ]
            except KeyError:
                if Image.DEBUG:
                    print("- unsupported type", typ)
                continue # ignore unsupported type

            size, handler = dispatch

            size = size * i32(ifd, 4)

            # Get and expand tag value
            if size > 4:
                here = fp.tell()
                fp.seek(i32(ifd, 8))
                data = ImageFile._safe_read(fp, size)
                fp.seek(here)
            else:
                data = ifd[8:8+size]

            if len(data) != size:
                raise IOError("not enough data")

            self.tagdata[tag] = typ, data

            if Image.DEBUG:
                if tag in (COLORMAP, IPTC_NAA_CHUNK, PHOTOSHOP_CHUNK):
                    print("- value: <table: %d bytes>" % size)
                else:
                    print("- value:", self[tag])

        self.next = i32(fp.read(4))

    # save primitives

    def save(self, fp):

        o16 = self.o16
        o32 = self.o32

        fp.write(o16(len(self.tags)))

        # always write in ascending tag order
        tags = self.tags.items()
        tags.sort()

        directory = []
        append = directory.append

        offset = fp.tell() + len(self.tags) * 12 + 4

        stripoffsets = None

        # pass 1: convert tags to binary format
        for tag, value in tags:

            if Image.DEBUG:
                import TiffTags
                tagname = TiffTags.TAGS.get(tag, "unknown")
                print("save: %s (%d)" % (tagname, tag))
                print("- value:", value)

            if type(value[0]) is type(""):
                # string data
                typ = 2
                data = value = string.join(value, "\0") + "\0"

            else:
                # integer data
                if tag == STRIPOFFSETS:
                    stripoffsets = len(directory)
                    typ = 4 # to avoid catch-22
                elif tag in (X_RESOLUTION, Y_RESOLUTION):
                    # identify rational data fields
                    typ = 5
                else:
                    typ = 3
                    for v in value:
                        if v >= 65536:
                            typ = 4
                if typ == 3:
                    data = string.join(map(o16, value), "")
                else:
                    data = string.join(map(o32, value), "")

            # figure out if data fits into the directory
            if len(data) == 4:
                append((tag, typ, len(value), data, ""))
            elif len(data) < 4:
                append((tag, typ, len(value), data + (4-len(data))*"\0", ""))
            else:
                count = len(value)
                if typ == 5:
                    count = count / 2        # adjust for rational data field
                append((tag, typ, count, o32(offset), data))
                offset = offset + len(data)
                if offset & 1:
                    offset = offset + 1 # word padding

        # update strip offset data to point beyond auxiliary data
        if stripoffsets is not None:
            tag, typ, count, value, data = directory[stripoffsets]
            assert not data, "multistrip support not yet implemented"
            value = o32(self.i32(value) + offset)
            directory[stripoffsets] = tag, typ, count, value, data

        # pass 2: write directory to file
        for tag, typ, count, value, data in directory:
            if Image.DEBUG > 1:
                print(tag, typ, count, repr(value), repr(data))
            fp.write(o16(tag) + o16(typ) + o32(count) + value)
        fp.write("\0\0\0\0") # end of directory

        # pass 3: write auxiliary data to file
        for tag, typ, count, value, data in directory:
            fp.write(data)
            if len(data) & 1:
                fp.write("\0")

        return offset

##
# Image plugin for TIFF files.

class TiffImageFile(ImageFile.ImageFile):

    format = "TIFF"
    format_description = "Adobe TIFF"

    def _open(self):
        "Open the first image in a TIFF file"

        # Header
        ifh = self.fp.read(8)

        if ifh[:4] not in PREFIXES:
            raise SyntaxError("not a TIFF file")

        # image file directory (tag dictionary)
        self.tag = self.ifd = ImageFileDirectory(ifh[:2])

        # setup frame pointers
        self.__first = self.__next = self.ifd.i32(ifh, 4)
        self.__frame = -1
        self.__fp = self.fp

        # and load the first frame
        self._seek(0)

    def seek(self, frame):
        "Select a given frame as current image"

        if frame < 0:
            frame = 0
        self._seek(frame)

    def tell(self):
        "Return the current frame number"

        return self._tell()

    def _seek(self, frame):

        self.fp = self.__fp
        if frame < self.__frame:
            # rewind file
            self.__frame = -1
            self.__next = self.__first
        while self.__frame < frame:
            if not self.__next:
                raise EOFError("no more images in TIFF file")
            self.fp.seek(self.__next)
            self.tag.load(self.fp)
            self.__next = self.tag.next
            self.__frame = self.__frame + 1
        self._setup()

    def _tell(self):

        return self.__frame

    def _decoder(self, rawmode, layer):
        "Setup decoder contexts"

        args = None
        if rawmode == "RGB" and self._planar_configuration == 2:
            rawmode = rawmode[layer]
        compression = self._compression
        if compression == "raw":
            args = (rawmode, 0, 1)
        elif compression == "jpeg":
            args = rawmode, ""
            if self.tag.has_key(JPEGTABLES):
                # Hack to handle abbreviated JPEG headers
                self.tile_prefix = self.tag[JPEGTABLES]
        elif compression == "packbits":
            args = rawmode
        elif compression == "tiff_lzw":
            args = rawmode
            if self.tag.has_key(317):
                # Section 14: Differencing Predictor
                self.decoderconfig = (self.tag[PREDICTOR][0],)

        return args

    def _setup(self):
        "Setup this image object based on current tags"

        if self.tag.has_key(0xBC01):
            raise IOError("Windows Media Photo files not yet supported")

        getscalar = self.tag.getscalar

        # extract relevant tags
        self._compression = COMPRESSION_INFO[getscalar(COMPRESSION, 1)]
        self._planar_configuration = getscalar(PLANAR_CONFIGURATION, 1)

        # photometric is a required tag, but not everyone is reading
        # the specification
        photo = getscalar(PHOTOMETRIC_INTERPRETATION, 0)

        fillorder = getscalar(FILLORDER, 1)

        if Image.DEBUG:
            print("*** Summary ***")
            print("- compression:", self._compression)
            print("- photometric_interpretation:", photo)
            print("- planar_configuration:", self._planar_configuration)
            print("- fill_order:", fillorder)

        # size
        xsize = getscalar(IMAGEWIDTH)
        ysize = getscalar(IMAGELENGTH)
        self.size = xsize, ysize

        if Image.DEBUG:
            print("- size:", self.size)

        format = getscalar(SAMPLEFORMAT, 1)

        # mode: check photometric interpretation and bits per pixel
        key = (
            self.tag.byteorder, photo, format, fillorder,
            self.tag.get(BITSPERSAMPLE, (1,)),
            self.tag.get(EXTRASAMPLES, ())
            )
        if Image.DEBUG:
            print("format key:", key)
        try:
            self.mode, rawmode = OPEN_INFO[key]
        except KeyError:
            if Image.DEBUG:
                print("- unsupported format")
            raise SyntaxError("unknown pixel mode")

        if Image.DEBUG:
            print("- raw mode:", rawmode)
            print("- pil mode:", self.mode)

        self.info["compression"] = self._compression

        xdpi = getscalar(X_RESOLUTION, (1, 1))
        ydpi = getscalar(Y_RESOLUTION, (1, 1))

        if xdpi and ydpi:
            xdpi = xdpi[0] / (xdpi[1] or 1)
            ydpi = ydpi[0] / (ydpi[1] or 1)
            unit = getscalar(RESOLUTION_UNIT, 1)
            if unit == 1:
                self.info["aspect"] = xdpi, ydpi
            elif unit == 2:
                self.info["dpi"] = xdpi, ydpi
            elif unit == 3:
                self.info["dpi"] = (xdpi*.39370079, ydpi*.39370079)

        # build tile descriptors
        x = y = l = 0
        self.tile = []
        if self.tag.has_key(STRIPOFFSETS):
            # striped image
            h = getscalar(ROWSPERSTRIP, ysize)
            w = self.size[0]
            a = None
            for o in self.tag[STRIPOFFSETS]:
                if not a:
                    a = self._decoder(rawmode, l)
                self.tile.append(
                    (self._compression,
                    (0, min(y, ysize), w, min(y+h, ysize)),
                    o, a))
                y = y + h
                if y >= self.size[1]:
                    x = y = 0
                    l = l + 1
                    a = None
        elif self.tag.has_key(TILEOFFSETS):
            # tiled image
            w = getscalar(322)
            h = getscalar(323)
            a = None
            for o in self.tag[TILEOFFSETS]:
                if not a:
                    a = self._decoder(rawmode, l)
                # FIXME: this doesn't work if the image size
                # is not a multiple of the tile size...
                self.tile.append(
                    (self._compression,
                    (x, y, x+w, y+h),
                    o, a))
                x = x + w
                if x >= self.size[0]:
                    x, y = 0, y + h
                    if y >= self.size[1]:
                        x = y = 0
                        l = l + 1
                        a = None
        else:
            if Image.DEBUG:
                print("- unsupported data organization")
            raise SyntaxError("unknown data organization")

        # fixup palette descriptor
        
        if self.mode == "P":
            #seb
            try:
                palette = map(lambda a: chr(a // 256), self.tag[COLORMAP])
            except KeyError:
                pass # seb HACK !! for some Zeiss LSM files
                palette = map(lambda a: chr(a // 256), range(256))
            self.palette = ImagePalette.raw("RGB;L", string.join(palette, ""))
            #orig:
            #palette = map(lambda a: chr(a // 256), self.tag[COLORMAP])
            #self.palette = ImagePalette.raw("RGB;L", string.join(palette, ""))
#
# --------------------------------------------------------------------
# Write TIFF files

# little endian is default except for image modes with explict big endian byte-order

SAVE_INFO = {
    # mode => rawmode, byteorder, photometrics, sampleformat, bitspersample, extra
    "1": ("1", 'l', 1, 1, (1,), None),
    "L": ("L", 'l', 1, 1, (8,), None),
    "LA": ("LA", 'l', 1, 1, (8,8), 2),
    "P": ("P", 'l', 3, 1, (8,), None),
    "PA": ("PA", 'l', 3, 1, (8,8), 2),
    "I": ("I;32S", 'l', 1, 2, (32,), None),
    "I;16": ("I;16", 'l', 1, 1, (16,), None),
    "I;16S": ("I;16S", 'l', 1, 2, (16,), None),
    "F": ("F;32F", 'l', 1, 3, (32,), None),
    "RGB": ("RGB", 'l', 2, 1, (8,8,8), None),
    "RGBX": ("RGBX", 'l', 2, 1, (8,8,8,8), 0),
    "RGBA": ("RGBA", 'l', 2, 1, (8,8,8,8), 2),
    "CMYK": ("CMYK", 'l', 5, 1, (8,8,8,8), None),
    "YCbCr": ("YCbCr", 'l', 6, 1, (8,8,8), None),
    "LAB": ("LAB", 'l', 8, 1, (8,8,8), None),
   
    "I;32BS": ("I;32BS", 'b', 1, 2, (32,), None),
    "I;16B": ("I;16B", 'b', 1, 1, (16,), None),
    "I;16BS": ("I;16BS", 'b', 1, 2, (16,), None),
    "F;32BF": ("F;32BF", 'b', 1, 3, (32,), None),
}

def _cvt_res(value):
    # convert value to TIFF rational number -- (numerator, denominator)
    if type(value) in (type([]), type(())):
        assert(len(value) % 2 == 0)
        return value
    if type(value) == type(1):
        return (value, 1)
    value = float(value)
    return (int(value * 65536), 65536)

def _save(im, fp, filename):

    try:
        rawmode, byteorder, photo, format, bits, extra = SAVE_INFO[im.mode]
    except KeyError:
        raise IOError("cannot write mode %s as TIFF" % im.mode)

    ifd = ImageFileDirectory(BYTEORDER_TO_PREFIX[byteorder])

    #seb -- multi-page -- added `if`
    if fp.tell() == 0:
        # tiff header (write via IFD to get everything right)
        # PIL always starts the first IFD at offset 8
        fp.write(ifd.prefix + ifd.o16(42) + ifd.o32(8))
        #seb debug  print "DEBUG: 000", fp.tell()

    ifd[IMAGEWIDTH] = im.size[0]
    ifd[IMAGELENGTH] = im.size[1]

    # additions written by Greg Couch, gregc@cgl.ucsf.edu
    # inspired by image-sig posting from Kevin Cazabon, kcazabon@home.com
    if hasattr(im, 'tag'):
        # preserve tags from original TIFF image file
        for key in (RESOLUTION_UNIT, X_RESOLUTION, Y_RESOLUTION):
            if im.tag.tagdata.has_key(key):
                ifd[key] = im.tag.tagdata.get(key)
    if im.encoderinfo.has_key("description"):
        ifd[IMAGEDESCRIPTION] = im.encoderinfo["description"]
    if im.encoderinfo.has_key("resolution"):
        ifd[X_RESOLUTION] = ifd[Y_RESOLUTION] \
                                = _cvt_res(im.encoderinfo["resolution"])
    if im.encoderinfo.has_key("x resolution"):
        ifd[X_RESOLUTION] = _cvt_res(im.encoderinfo["x resolution"])
    if im.encoderinfo.has_key("y resolution"):
        ifd[Y_RESOLUTION] = _cvt_res(im.encoderinfo["y resolution"])
    if im.encoderinfo.has_key("resolution unit"):
        unit = im.encoderinfo["resolution unit"]
        if unit == "inch":
            ifd[RESOLUTION_UNIT] = 2
        elif unit == "cm" or unit == "centimeter":
            ifd[RESOLUTION_UNIT] = 3
        else:
            ifd[RESOLUTION_UNIT] = 1
    if im.encoderinfo.has_key("software"):
        ifd[SOFTWARE] = im.encoderinfo["software"]
    if im.encoderinfo.has_key("date time"):
        ifd[DATE_TIME] = im.encoderinfo["date time"]
    if im.encoderinfo.has_key("artist"):
        ifd[ARTIST] = im.encoderinfo["artist"]
    if im.encoderinfo.has_key("copyright"):
        ifd[COPYRIGHT] = im.encoderinfo["copyright"]

    dpi = im.encoderinfo.get("dpi")
    if dpi:
        ifd[RESOLUTION_UNIT] = 2
        ifd[X_RESOLUTION] = _cvt_res(dpi[0])
        ifd[Y_RESOLUTION] = _cvt_res(dpi[1])

    if bits != (1,):
        ifd[BITSPERSAMPLE] = bits
        if len(bits) != 1:
            ifd[SAMPLESPERPIXEL] = len(bits)
    if extra is not None:
        ifd[EXTRASAMPLES] = extra
    if format != 1:
        ifd[SAMPLEFORMAT] = format

    ifd[PHOTOMETRIC_INTERPRETATION] = photo

    if im.mode == "P":
        lut = im.im.getpalette("RGB", "RGB;L")
        ifd[COLORMAP] = tuple(map(lambda v: ord(v) * 256, lut))

    # data orientation
    stride = len(bits) * ((im.size[0]*bits[0]+7)/8)
    ifd[ROWSPERSTRIP] = im.size[1]
    ifd[STRIPBYTECOUNTS] = stride * im.size[1]
    ifd[STRIPOFFSETS] = 0 # this is adjusted by IFD writer
    ifd[COMPRESSION] = 1 # no compression

    offset = ifd.save(fp)

    ImageFile._save(im, fp, [
        ("raw", (0,0)+im.size, offset, (rawmode, stride, 1))
        ])


    #seb -- multi-page -- 
    if im.encoderinfo.has_key("_debug_multipage"):
        #just to access o32 and o16 (using correct byte order)
        im._debug_multipage = ifd

#
# --------------------------------------------------------------------
# Register

Image.register_open("TIFF", TiffImageFile, _accept)
Image.register_save("TIFF", _save)

Image.register_extension("TIFF", ".tif")
Image.register_extension("TIFF", ".tiff")

Image.register_mime("TIFF", "image/tiff")
