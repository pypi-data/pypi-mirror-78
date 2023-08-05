oext=False
try:
    import PyOrigin as po
except ImportError:
    import OriginExt
    po = OriginExt.Application()
    oext = True
