from pyxpdf.includes.CharTypes cimport Unicode
from pyxpdf.includes.Dict cimport Dict
from pyxpdf.includes.Page cimport PDFRectangle
from pyxpdf.includes.TextString cimport TextString

cdef inline bytes _chars(object s):
    if isinstance(s, unicode):
        # encode to the specific encoding used inside of the module
        s = (<unicode>s).encode('UTF-8')
    return s

cdef inline bytes _utf8_bytes(object s):
    if isinstance(s, unicode):
        # encode to the specific encoding used inside of the module
        s = (<unicode>s).encode('UTF-8')
    return s

cdef inline bytes _utf32_bytes(object s):
    if type(s) is unicode:
        # encode to the specific encoding used inside of the module
        s = (<unicode>s).encode('UTF-32')
    elif isinstance(s, unicode):
        # We know from the above that 's' can only be a subtype here.
        s = unicode(s).encode('UTF-32')
    else:
        raise TypeError("Could not convert to utf-32 bytes.")
    return s

cdef inline GString* to_GString(object s):
    return new GString(_chars(s))

cdef inline object GString_to_unicode(GString *gstr):
    if gstr is not NULL:
        return gstr.getCString()[:gstr.getLength()].decode("UTF-8", errors='ignore')
    else:
        return ""

cdef inline GBool_to_bool(GBool b):
    return True if b == gTrue else False

cdef inline GBool to_GBool(pyb):
    return gTrue if pyb else gFalse


cdef inline PDFRectangle_to_tuple(PDFRectangle *rect):
    cdef tuple rect_tp 
    rect_tp = (rect.x1, rect.y1, rect.x2, rect.y2)
    return rect_tp

cdef int utf32_to_Unicode_vector(text, vector[Unicode]& vec) except -1:
    cdef bytes by = _utf32_bytes(text)
    cdef char* ch = by

    cdef size_t l_bytes = len(by)
    cdef size_t l_utf32 = (l_bytes//4) - 1

    vec.resize(l_utf32)  # Not including BOM

    # print(f"{l_bytes}")
    # print(f"Loop - {list(range(4, l_bytes, 4))}")
    cdef size_t i
    for i in range(4, l_bytes, 4):
        vec[(i//4) - 1] = deref(<Unicode*>(&ch[i]))
        #print(f"{(i/4) - 1} - {vec[(i/4) - 1]}")
    return 0


cdef dict Dict_to_pydict(Dict* xdict, dict pydict = {}):
    cdef Object obj
    cdef const char* key
    if xdict != NULL:
        for i in range(xdict.getLength()):
            key = xdict.getKey(i)
            if xdict.lookup(key, &obj, 0).isString() == gTrue:
                pydict[key.decode('UTF-8')] = GString_to_unicode(obj.getString())
            elif xdict.lookup(key, &obj, 0).isNum() == gTrue:
                pydict[key.decode('UTF-8')] = obj.getNum()
            obj.free()
    return pydict

# cdef object TextString_to_unicode(TextString* text_str):
#    return GString_to_unicode(text_str.toPDFTextString())

cdef TextString* to_TextString(tstr):
    cdef:
        unique_ptr[GString] gstr
        TextString* text_string
    gstr.reset(to_GString(tstr))
    text_string = new TextString(gstr.get())
    return text_string

cdef void append_to_cpp_string(void *stream, const char *text, int length):
    (<string*>stream)[0] += string(text, length)


cdef bint c_readable(char *file_path):
    cdef:
        cstdio.FILE *_fp
        bint readable = False
    _fp = cstdio.fopen(file_path, 'r')
    if _fp != NULL:
        cstdio.fclose(_fp)
        readable = True
    return readable
