''' stores all file's path in game '''
import sys
import os
from enum import Enum

class File_Path():
    ''' Path Enums '''
    resources = "./Resources"

    # Fonts
    fonts = resources + '/Fonts'
    freesansbold = fonts + '/freesansbold.ttf'
    jetlinkbold1 = fonts + '/JT1-09U.ttF'
    msjenghei = fonts + '/msjhbd.ttc'

    # Images
    images = resources + '/Images'
    two_pre = images + '/2p_pre.png'
    background = images + '/BackgroundIce.png'
    backgroundintro = images + '/BackgroundIntro.png'
    blackhole = images + '/blackhole.png'
    cloud = images + '/Cloudstairs.png'
    normal = images + '/Generalstairs_2.jpg'
    lckung = images + '/lckung.png'
    smlu = images + '/smlu.jpg'
    sting = images + '/Stingstairs.png'
    kungright1 = images + '/小傑側面_右收步.png'
    kungright2 = images + '/小傑側面_右跨步.png'
    kungleft1 = images + '/小傑側面_左收步.png'
    kungleft2 = images + '/小傑側面_左跨步.png'
    kungfront = images + '/小傑正面.png'
    smluright1 = images + '/小銘側面_右收步.png'
    smluright2 = images + '/小銘側面_右跨步.png'
    smluleft1 = images + '/小銘側面_左收步.png'
    smluleft2 = images + '/小銘側面_左跨步.png'
    smlufront = images + '/小銘正面.png'

    # Sound
    sound = resources + '/Sound'
    hurtsound = sound + '/短慘叫.wav'
    deathsound = sound + '/長慘叫.wav'

    config = 'config.json'

def init():
    ''' If using pyinstaller, appends temp file location to file paths'''
    if hasattr(sys, '_MEIPASS'):
        base = sys._MEIPASS
        for path in File_Path.__dict__:
            if '_' != path[0] and path != 'config':
                setattr(File_Path, path, base + File_Path.__dict__[path][1:]) # error is fixed by pyinstaller

