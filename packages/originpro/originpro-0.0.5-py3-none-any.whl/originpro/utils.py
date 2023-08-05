"""
originpro
A package for interacting with Origin software via Python.
Copyright (c) 2020 OriginLab Corporation
"""
from .config import po, oext
import os


def lt_float(formula):
    """
    get the result of a LabTalk expression
    
    Parameters:
        formula (str): any LaTalk expression
        
    Examples:
        #Origin Julian days value
        >>>op.lt_float('date(1/2/2020)')
        #get Origin version number
        >>>op.lt_float('@V')
    
    See Also:
        get_lt_str, lt_int
    """
    return po.LT_evaluate(formula)
    
def lt_int(formula):
    """
    get the result of a LabTalk expression as int, see lt_float()
    
    Examples:
        >>> op.lt_int('color("green")')
        
    See Also:
        get_lt_str, lt_float
    """
    return int(lt_float(formula))

def get_lt_str(vname):
    """
    return a LabTalk string variable value. To get LabTalk numeric values, use lt_int or lt_float
    
    Examples:
        #AppData path for the installed Origin
        >>> op.get_lt_str('%@Y')
    See Also:
        lt_int, lt_float
    """
    return po.LT_get_str(vname)

def ocolor(rgb):
    """
    convert color to Origin's internal OColor
    
    Parameters:
        rgb: names or index of colors supported in Origin. Unlike in LabTalk which has one-based, it is zero-based here
                      name          index    (Red, Green, Blue)
                      'Black'           0       000,000,000
                      'Red'             1       255,000,000
                      'Green'           2       000,255,000
                      'Blue'            3       000,000,255
                      'Cyan'            4       000,255,255
                      'Magenta'         5       255,000,255
                      'Yellow'          6       255,255,000
                      'Dark Yellow'     7       128,128,000
                      'Navy'            8       000,000,128
                      'Purple'          9       128,000,128
                      'Wine'            10      128,000,000
                      'Olive'           11      000,128,000
                      'Dark Cyan'       12      000,128,128
                      'Royal'           13      000,000,160
                      'Orange'          14      255,128,000
                      'Violet'          15      128,000,255
                      'Pink'            16      255,000,128
                      'White'           17      255,255,255
                      'LT Gray'         18      192,192,192
                      'Gray'            19      128,128,128
                      'LT Yellow'       20      255,255,128
                      'LT Cyan'         21      128,255,255
                      'LT Magenta'      22      255,128,255
                      'Dark Gray'       23      064,064,064
             it can be in formmat as well, for example, '#f00' for red.
             when the input is a tuple, it should be
             if rgb is tuple of intergers between 0 and 255, the color is set by RGB (Red, Green, Blue).
    
    Returns:
        (int) OColor
    """
    if isinstance(rgb, str):
        orgb = lt_int(f'color({rgb})')-1
    elif isinstance(rgb, int):
        orgb = rgb
    elif isinstance(rgb, (list, tuple)):
        r, g, b = rgb
        orgb = lt_int(f'color({int(r)}, {int(g)}, {int(b)})')
    else:
        raise ValueError(f'the color value of {rgb} cannot be recognized.')
 
    return orgb
def to_rgb(orgb):
    """
    convert an Origin OColor to r, g, b
    
    Parameters:
        orgb(int): OColor from Origin's internal value
        
    Returns:
        (tuple) r,g,b
    """
    rgb = lt_int(f'ocolor2rgb({orgb})')
    return int(rgb%256), int(rgb//256%256), int(rgb//256//256%256)

def get_file_ext(fname):
    R"""
    Given a full path file name, return the file extension.

    Parameters:
        fname (str): Full path file name

    Returns:
        (str) File extension

    Examples:
        ext = op.get_file_ext('C:\path\to\somefile.dat')
    """
    if len(fname) == 0:
        return ''
    return os.path.splitext(fname)[1]

def get_file_parts(fname):
    R"""
    Given a full path file name, return the path, file name, and extension as a Python list object.

    Parameters:
        fname (str): Full path file name

    Returns:
        (list) Contains path, file name, and extension

    Examples:
        parts = op.get_file_parts('C:\path\to\somefile.dat')
    """
    if len(fname) == 0:
        return ['','','']
    path,filename = os.path.split(fname)
    ff,ee = os.path.splitext(filename)
    return [path, ff, ee]


def last_backslash(fpath, action):
    """
    Add or trim a backslash to/from a path string.

    Parameters:
        fpath (str): Path
        action (str): Either 'a' for add backslash or 't' for trim backslash

    Returns:
        (str) Path either with added backslash or without trimmed backslash

    Examples:
        >>>op.last_backslash(op.path(), 't')
    """

    if len(fpath) < 3:
        raise ValueError('invalid file path')
    if not action in ['a', 't']:
        raise ValueError('invalid action')

    last_char = fpath[-1]
    if action == 'a':
        if last_char == '\\':
            return fpath
        return fpath + '\\'
    else:
        assert action == 't'
        if not last_char == '\\':
            return fpath
        return fpath[:-1]


def path(type = 'u'):
    """
    Returns one of the Origin pre-defned paths: User Files folder, Origin EXe folder, project folder, Project attached file folder.

    Parameters:
        type (str): 'u'(User Files folder), 'e'(Origin Exe folder), 'p'(project folder), 'a'(Attached file folder),
                    'c'(Learning Center)

    Returns:
        (str) Contains folder path

    Examples:
        uff = op.path()
        op.open(op.path('c')+ r'Graphing\Trellis Plots - Box Charts.opju')
    """
    if type == 'p':
        return get_lt_str('%X')
    if type == 'c':
        return get_lt_str('%@D') + 'Central\\'
    if type == 'a':
        return get_lt_str('SYSTEM.PATH.PROJECTATTACHEDFILESPATH$')
    path_types = {
        'u':po.APPPATH_USER if oext else po.PATHTYPE_USER,
        'e':po.APPPATH_PROGRAM if oext else po.PATHTYPE_SYSTEM,
        }
    otype = path_types.get(type, None)
    if otype is None:
        raise ValueError('Invalid path type')

    fnpath = po.Path if oext else po.GetPath
    return fnpath(otype)

def wait(type = 'r', sec=0):
    """
    Wait for recalculation to finish or a specified number of seconds.

    Parameters:
        type (str): Either 'r' to wait for recalculation to finish or 's' to wait for specified seconds
        sec (float): Number of seconds to wait is 's' specified for type

    Returns:
        None

    Examples:
        op.wait()#wait for Origin to update all the recalculations
        op.wait('s', 0.2)#gives 0.2 sec for graphs to finish updating
    """
    if type=='r':
        po.LT_execute('run -p au')
    elif type == 's':
        po.LT_execute(f'sec -p {sec}')
    else:
        raise ValueError('must be r or s')

def file_dialog(type, title=''):
    """
    open a file dialog to pick a single file
    Parameters:
        type (str): 'i' for image, 't' for text, 'o' for origin, or a file extension like '*.png'
    
    Returns:
        if user cancel, an empty str, otherwise the selected file path
    Examples:
        fn=op.file_dialog('o')
        fn=op.file_dialog('*.png;*.jpg;*.bmp')
    """
    if not isinstance(type, str) or len(type)==0:
        raise ValueError('type must be specified')
    if type.find('*') >= 0:
        gg = type
    else:
        types = {'i': 'cvImageImp','t': 'ASCIIEXP','o':'OriginImport'}
        gg = types[type]
        
    po.LT_execute(f'__fname_for_py$="";dlgfile fname:=__fname_for_py group:="{gg}" title:="{title}"');
    fname=get_lt_str('__fname_for_py$');
    po.LT_execute('del -vs __fname_for_py$');
    return fname

def origin_class(name):
    if not oext:
        name = 'CPy' + name
    return getattr(po, name)

def active_obj(name):
    activeobj = getattr(po, 'Active' + name)
    return activeobj if oext else activeobj()

def make_DataRange(*args, rows=None):
    ranges = origin_class('DataRange')()
    subs = []
    subrows = None

    def addonerange():
        if subs:
            nonlocal subrows
            if subrows is None and rows is not None:
                subrows = rows
            r1 = 0; r2 = -1
            if subrows:
                r1, r2 = subrows
                r1 -= 1; r2 -= 1
            for sub in subs:
                stype = sub[0]
                col = sub[1]
                ncol = col.GetIndex()
                if isinstance(col, origin_class('MatrixObject')):
                    ranges.AddMatrix(col.GetParent(), ncol)
                else:
                    ranges.Add(stype, col.GetParent(), r1, ncol, r2, ncol)
            ranges.Add("S", None, 0, 0, 0, 0)
            subs.clear()
            subrows = None

    numargs = len(args)
    i = 0
    while i < numargs:
        desig = args[i].upper()
        if desig in ('X', 'Y', 'Z'):
            i += 1
            subs.append((desig, args[i]))
        elif desig == 'S':
            addonerange()
        elif desig == 'ROWS':
            i += 1
            subrows = args[i]
        i += 1
    addonerange()

    return ranges
