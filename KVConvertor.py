#!/usr/bin/python
#
##############################################################################
# Current Status: Beta!
# Purpose:
# 1. Using Class definitions condense the amount of code
#      required to obtain information from source video files
#      (Currently copies settings such as Frame Rate, Aspect, etc
#      from source video, but this will be fixed)
# 2. Make the script/program more conformative to coding standards
# 3. Testing recently added Logging and Config read/write
##############################################################################

##############################################################################
# Imports
##############################################################################
import sys
import os
import subprocess
import linecache
import string
import shutil
import time
import logging
from collections import deque
from pymediainfo import MediaInfo
from configobj import ConfigObj

##############################################################################
# Setting Global Variables.
##############################################################################

#=============================================================================
# Only used when user runs into any issues with converting a
# file and is requested to change it for support purposes.
# 0 = No , 1 = Yes
#=============================================================================
tsIssue = 1
dontClr = 0
addPause = 1

#=============================================================================
# User Variables
#=============================================================================
# Do not mess this up! Refer to the wiki for more information
cfgDir = ('/home/hakugin/VidConversion/KVC/Linux_Primary_x86')
config = ConfigObj('%s/user.cfg' % cfgDir, indent_type='    ')

#=============================================================================
# Filename/File Variables.
#=============================================================================
wList = sys.argv[1:]
fName = 0
WD = 0
bName = 0
eXtsn = 0
kDual = 0
sAudio = 0
burnSub = 0
delTemp = 0

yes = set(['yes','y','ye','yup','yeah','yep'])
no = set(['no','n','nope','nah'])
fs = set(['f','fs','full','fscreen','fullscreen','4:3','1.333'])
ws = set(['w','ws','wide','wscreen','widescreen','16:9','1.777'])

#=============================================================================
# Assigning Values from Input Streams
#=============================================================================
vContainer = 0
vCount = 0
aCount = 0
sCount = 0
tCount = 0
v1 = 0
v2 = 0
a1 = 0
a2 = 0
s1 = 0
s2 = 0

#=============================================================================
# Variables for output/comparison
#=============================================================================
v1o = 0
a1o = 0
a2o = 0

#=============================================================================
# Error Counts (Not used yet!)
#=============================================================================
vError = 0
aError = 0
sError = 0

#=============================================================================
# Log Handler (work in progress)
#=============================================================================
# Set logging to file
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s: %(levelname)s: %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='%s/KVConvertor.log' % cfgDir,
                    filemode='w')

# messages to console, INFO and higher to sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
# simpler format for console
formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
# user the format for displaying on the console
console.setFormatter(formatter)
# add handler to root logger
logging.getLogger('').addHandler(console)

logger1 = logging.getLogger('KVC.Configuration')
logger2 = logging.getLogger('KVC.Detection')
logger3 = logging.getLogger('KVC.Conversion')


#=============================================================================
# Setting how messages will be displayed, and other definitions.
#=============================================================================
def message(msg):
    print '#' * 70
    print '%s' % msg
    print '#' * 70

def message2(msg3):
    print '+' * 70
    print '%s' % msg3

def message3(msg4):
    print '%s' % msg4

def message4(msg6):
    print '%s' % msg6
    print '-' * 70

def usage():
    print 'Video repacker script'
    print
    print '  Usage: [script] [video1] [video2] [etc].'
    print

def ts_pause():
    if addPause != 0:
        raw_input('\n Process paused, press ENTER to continue \n')
    else:
        pass

def ts_clear():
    if dontClr != 0:
        pass
    else:
        subprocess.call('clear')

def del_temp():
    if usrDelTemp != 0:
        subprocess.call(['rm', '-r', '%s/Temp' % WD])
    else:
        pass

##############################################################################
# Beginning of test classes.
# Provides a different approach to storing information about
# the source videos being converted.
##############################################################################

#=============================================================================
# Video
#=============================================================================
class vInfo:
    def __init__(self, ID, CDC, FRT, DA, WD, HT, DRA, BRM, BR, LNG, FMT):
        self.ID = ID
        self.Codec = CDC
        self.FRate = FRT
        self.DisAsp = DA
        self.Width = WD
        self.Height = HT
        self.Duration = DRA
        self.BRmode = BRM
        self.BRate = BR
        self.Lang = LNG
        self.Format = FMT

#=============================================================================
# Audio
#=============================================================================
class aInfo:
    def __init__(self, ID, CDC, SMP, CHN, BRM, BR, DRA, LNG):
        self.ID = ID
        self.Codec = CDC
        self.Sample = SMP
        self.Channels = CHN
        self.BRmode = BRM
        self.BRate = BR
        self.Duration = DRA
        self.Lang = LNG

#=============================================================================
# Subtitles
#=============================================================================
class sInfo:
    def __init__(self, ID, CDC, LNG):
        self.ID = ID
        self.Format = CDC
        self.Lang = LNG

#=============================================================================
# Creating the user configuration file
#=============================================================================
def create_config():
    global config
    config['General'] = {}
    while True:
        config['General']['Keep Dual Audio'] = raw_input('Do you want to keep '
            'both audio tracks if they exist?\n   [Y]es or [N]o:\n')
        if config['General']['Keep Dual Audio'] in yes:
            subprocess.call('clear')
            break
        elif config['General']['Keep Dual Audio'] in no:
            subprocess.call('clear')
            break
        else:
            subprocess.call('clear')
            logger1.info('Invalid response, please respond with yes or no'
                '\n Error: KD')
    while True:
        config['General']['Swap Audio'] = raw_input('Would you like to swap '
            'audio track?\n   [Y]es or [N]o:\n')
        if config['General']['Swap Audio'] in yes:
            subprocess.call('clear')
            break
        elif config['General']['Swap Audio'] in no:
            subprocess.call('clear')
            break
        else:
            subprocess.call('clear')
            logger1.info('Invalid response, please respond with yes or no'
                '\n Error: SA')
    while True:
        config['General']['Burn Subtitles'] = raw_input('Shall we add any '
            'subtitles in permanently?\n   [Y]es or [N]o:\n')
        if config['General']['Burn Subtitles'] in yes:
            subprocess.call('clear')
            break
        elif config['General']['Burn Subtitles'] in no:
            subprocess.call('clear')
            break
        else:
            subprocess.call('clear')
            logger1.info('Invalid response, please respond with yes or no'
                 '\n Error: BS')
    while True:
        config['General']['Delete Temp'] = raw_input('Do you want to remove any '
            'temporary files created?\n   [Y]es or [N]o:\n')
        if config['General']['Delete Temp'] in yes:
            subprocess.call('clear')
            break
        elif config['General']['Delete Temp'] in no:
            subprocess.call('clear')
            break
        else:
            subprocess.call('clear')
            logger1.info('Invalid response, please respond with yes or no'
                 '\n Error: DT')

    config['Video'] = {}
    config['Video']['Aspect Ratio'] = raw_input('Please select '
        'your desired Aspect Ratio:\n Options: '
        '1 = Fullscreen, 2 = Widescreen\n')
    config['Video']['Width'] = raw_input('What would you like '
        'the video width to be?:\n')
    config['Video']['Height'] = raw_input('What should we set '
        'for the video height?:\n')
    config['Video']['Bit Rate'] = raw_input('And what will the '
        'Bit Rate of the output be?: (Optional)\n')
    config['Video']['Frame Rate'] = raw_input('What shall the '
        'frame rate be? (Optional):\n')

    config['Audio 1'] = {}
    config['Audio 1']['Sample Rate'] = raw_input('Please specify '
        'the output audio sample rate for track 1:\n')
    config['Audio 1']['Channels'] = raw_input('How many Audio '
        'channels for the first track?:\n')
    config['Audio 1']['Bit Rate'] = raw_input('And finally, what '
        'will be the first audio tracks bit rate?\n')

    config['Audio 2'] = {}
    config['Audio 2']['Sample Rate'] = raw_input('Please specify '
        'the output audio sample rate for track 2:\n')
    config['Audio 2']['Channels'] = raw_input('How many Audio '
        'channels for the second track?:\n')
    config['Audio 2']['Bit Rate'] = raw_input('And finally, what '
        'will be the second audio tracks bit rate?\n')

    config.initial_comment = ('#' * 79, '#',
        '# This is your basic configuration please do not manually edit'
        ' this file.',
        'If you wish to change something simply run this program in'
        ' terminal without',
        'any arguments.', '#', '#' * 79, '')

    config.final_comment = ('', '#' * 79, '#',
        '# Brought to you by Hakugin and Gildor if you have any questions,'
        'comments,',
        '# or concerns feel free to let us know on GitHub!',
        '# <https://github.com/KVC-Video-Convertor/universal-convertor>',
        '#', '#' * 79)

    config.write()

    read_config()


#=============================================================================
# Read the user config file.
#=============================================================================
def read_config():
    global kDual, sAudio, burnSub, delTemp, v1o, a1o, a2o

    v1o = vInfo(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
    a1o = aInfo(0, 0, 0, 0, 0, 0, 0, 0)
    a2o = aInfo(0, 0, 0, 0, 0, 0, 0, 0)

    kDual = config['General']['Keep Dual Audio']
    sAudio = config['General']['Swap Audio']
    burnSub = config['General']['Burn Subtitles']
    delTemp = config['General']['Delete Temp']

    v1o.DisAsp = config['Video']['Aspect Ratio']
    v1o.Width = config['Video']['Width']
    v1o.Height = config['Video']['Height']
    v1o.BRate = config['Video']['Bit Rate']
    v1o.FRate = config['Video']['Frame Rate']

    a1o.Sample = config['Audio 1']['Sample Rate']
    a1o.Channels = config['Audio 1']['Channels']
    a1o.BRate = config['Audio 1']['Bit Rate']

    a2o.Sample = config['Audio 2']['Sample Rate']
    a2o.Channels = config['Audio 2']['Channels']
    a2o.BRate = config['Audio 2']['Bit Rate']

    if len(sys.argv) < 2:
        print_info()
    else:
        get_video_info()


##############################################################################
# Start the process of getting source video information
##############################################################################
def get_video_info():
    global fName, WD, bName, eXtsn, v1, v2, a1, a2, s1, s2
    global vCount, aCount, sCount, vContainer
    WD = os.path.dirname('%s' % fName)
    bName = fName[(len(WD)+1):-4]
    eXtsn = fName[-4:]
    os.chdir('%s' % WD)
    ts_clear()
    message('Obtaining video information. Please wait...')
    print
    mInfo = MediaInfo.parse('%s' % fName)
    for track in mInfo.tracks:
        if track.track_type == 'General':
            vCount = track.count_of_video_streams
            aCount = track.count_of_audio_streams
            sCount = track.count_of_text_streams
            vContainer = track.codec
            if sCount != '1' and sCount != '2':
                tCount = int(vCount)+int(aCount)
            else:
                tCount = int(vCount)+int(aCount)+int(sCount)
        else:
            pass

        if track.track_id == 0:
            if track.track_type == 'Video':
                v1 = vInfo(0, '%s' % track.codec_family,
                    '%s' % track.frame_rate, '%s' % track.display_aspect_ratio,
                    '%s' % track.width, '%s' % track.height,
                    '%s' % track.duration, '%s' % track.bit_rate_mode,
                    '%s' % track.bit_rate, '%s' % track.language,
                    '%s' % track.format)
            elif track.track_type == 'Audio':
                a1 = aInfo(0,  '%s' % track.codec_family,
                    '%s' % track.sampling_rate, '%s' % track.channel_s,
                    '%s' % track.bit_rate_mode, '%s' % track.bit_rate,
                    '%s' % track.duration, '%s' % track.language)
            elif track.track_type == 'Text':
                s1 = sInfo(0, '%s' % track.format, '%s' % track.language)
            else:
                pass
        else:
            pass

        if track.track_id == 1:
            if track.track_type == 'Video' and v1 == 0:
                v1 = vInfo(1, '%s' % track.codec_family,
                    '%s' % track.frame_rate, '%s' % track.display_aspect_ratio,
                    '%s' % track.width, '%s' % track.height,
                    '%s' % track.duration, '%s' % track.bit_rate_mode,
                    '%s' % track.bit_rate, '%s' % track.language,
                    '%s' % track.format)
            elif track.track_type == 'Video' and v1 != 0:
                v2 = vInfo(1, '%s' % track.codec_family,
                    '%s' % track.frame_rate, '%s' % track.display_aspect_ratio,
                    '%s' % track.width, '%s' % track.height,
                    '%s' % track.duration, '%s' % track.bit_rate_mode,
                    '%s' % track.bit_rate, '%s' % track.language,
                    '%s' % track.format)
            elif track.track_type == 'Audio' and a1 == 0:
                a1 = aInfo(1,  '%s' % track.codec_family,
                    '%s' % track.sampling_rate, '%s' % track.channel_s,
                    '%s' % track.bit_rate_mode, '%s' % track.bit_rate,
                    '%s' % track.duration, '%s' % track.language)
            elif track.track_type == 'Audio' and a1 != 0:
                a2 = aInfo(1,  '%s' % track.codec_family,
                    '%s' % track.sampling_rate, '%s' % track.channel_s,
                    '%s' % track.bit_rate_mode, '%s' % track.bit_rate,
                    '%s' % track.duration, '%s' % track.language)
            elif track.track_type == 'Text' and s1 == 0:
                s1 = sInfo(1, '%s' % track.format, '%s' % track.language)
            elif track.track_type == 'Text' and s1 != 0:
                s2 = sInfo(1, '%s' % track.format, '%s' % track.language)
            else:
                pass
        else:
            pass

        if track.track_id == 2:
            if track.track_type == 'Video' and v1 == 0:
                v1 = vInfo(2, '%s' % track.codec_family,
                    '%s' % track.frame_rate, '%s' % track.display_aspect_ratio,
                    '%s' % track.width, '%s' % track.height,
                    '%s' % track.duration, '%s' % track.bit_rate_mode,
                    '%s' % track.bit_rate, '%s' % track.language,
                    '%s' % track.format)
            elif track.track_type == 'Video' and v1 != 0:
                v2 = vInfo(2, '%s' % track.codec_family,
                    '%s' % track.frame_rate, '%s' % track.display_aspect_ratio,
                    '%s' % track.width, '%s' % track.height,
                    '%s' % track.duration, '%s' % track.bit_rate_mode,
                    '%s' % track.bit_rate, '%s' % track.language,
                    '%s' % track.format)
            elif track.track_type == 'Audio' and a1 == 0:
                a1 = aInfo(2,  '%s' % track.codec_family,
                    '%s' % track.sampling_rate, '%s' % track.channel_s,
                    '%s' % track.bit_rate_mode, '%s' % track.bit_rate,
                    '%s' % track.duration, '%s' % track.language)
            elif track.track_type == 'Audio' and a1 != 0:
                a2 = aInfo(2,  '%s' % track.codec_family,
                    '%s' % track.sampling_rate, '%s' % track.channel_s,
                    '%s' % track.bit_rate_mode, '%s' % track.bit_rate,
                    '%s' % track.duration, '%s' % track.language)
            elif track.track_type == 'Text' and s1 == 0:
                s1 = sInfo(2, '%s' % track.format, '%s' % track.language)
            elif track.track_type == 'Text' and s1 != 0:
                s2 = sInfo(2, '%s' % track.format, '%s' % track.language)
            else:
                pass
        else:
            pass

        if track.track_id == 3:
            if track.track_type == 'Video' and v1 == 0:
                v1 = vInfo(3, '%s' % track.codec_family,
                    '%s' % track.frame_rate, '%s' % track.display_aspect_ratio,
                    '%s' % track.width, '%s' % track.height,
                    '%s' % track.duration, '%s' % track.bit_rate_mode,
                    '%s' % track.bit_rate, '%s' % track.language,
                    '%s' % track.format)
            elif track.track_type == 'Video' and v1 != 0:
                v2 = vInfo(3, '%s' % track.codec_family,
                    '%s' % track.frame_rate, '%s' % track.display_aspect_ratio,
                    '%s' % track.width, '%s' % track.height,
                    '%s' % track.duration, '%s' % track.bit_rate_mode,
                    '%s' % track.bit_rate, '%s' % track.language,
                    '%s' % track.format)
            elif track.track_type == 'Audio' and a1 == 0:
                a1 = aInfo(3,  '%s' % track.codec_family,
                    '%s' % track.sampling_rate, '%s' % track.channel_s,
                    '%s' % track.bit_rate_mode, '%s' % track.bit_rate,
                    '%s' % track.duration, '%s' % track.language)
            elif track.track_type == 'Audio' and a1 != 0:
                a2 = aInfo(3,  '%s' % track.codec_family,
                    '%s' % track.sampling_rate, '%s' % track.channel_s,
                    '%s' % track.bit_rate_mode, '%s' % track.bit_rate,
                    '%s' % track.duration, '%s' % track.language)
            elif track.track_type == 'Text' and s1 == 0:
                s1 = sInfo(3, '%s' % track.format, '%s' % track.language)
            elif track.track_type == 'Text' and s1 != 0:
                s2 = sInfo(3, '%s' % track.format, '%s' % track.language)
            else:
                pass
        else:
            pass

        if track.track_id == 4:
            if track.track_type == 'Video' and v1 == 0:
                v1 = vInfo(4, '%s' % track.codec_family,
                    '%s' % track.frame_rate, '%s' % track.display_aspect_ratio,
                    '%s' % track.width, '%s' % track.height,
                    '%s' % track.duration, '%s' % track.bit_rate_mode,
                    '%s' % track.bit_rate, '%s' % track.language,
                    '%s' % track.format)
            elif track.track_type == 'Video' and v1 != 0:
                v2 = vInfo(4, '%s' % track.codec_family,
                    '%s' % track.frame_rate, '%s' % track.display_aspect_ratio,
                    '%s' % track.width, '%s' % track.height,
                    '%s' % track.duration, '%s' % track.bit_rate_mode,
                    '%s' % track.bit_rate, '%s' % track.language,
                    '%s' % track.format)
            elif track.track_type == 'Audio' and a1 == 0:
                a1 = aInfo(4,  '%s' % track.codec_family,
                    '%s' % track.sampling_rate, '%s' % track.channel_s,
                    '%s' % track.bit_rate_mode, '%s' % track.bit_rate,
                    '%s' % track.duration, '%s' % track.language)
            elif track.track_type == 'Audio' and a1 != 0:
                a2 = aInfo(4,  '%s' % track.codec_family,
                    '%s' % track.sampling_rate, '%s' % track.channel_s,
                    '%s' % track.bit_rate_mode, '%s' % track.bit_rate,
                    '%s' % track.duration, '%s' % track.language)
            elif track.track_type == 'Text' and s1 == 0:
                s1 = sInfo(4, '%s' % track.format, '%s' % track.language)
            elif track.track_type == 'Text' and s1 != 0:
                s2 = sInfo(4, '%s' % track.format, '%s' % track.language)
            else:
                pass
        else:
            pass

        if track.track_id == 5:
            if track.track_type == 'Video' and v1 == 0:
                v1 = vInfo(5, '%s' % track.codec_family,
                    '%s' % track.frame_rate, '%s' % track.display_aspect_ratio,
                    '%s' % track.width, '%s' % track.height,
                    '%s' % track.duration, '%s' % track.bit_rate_mode,
                    '%s' % track.bit_rate, '%s' % track.language,
                    '%s' % track.format)
            elif track.track_type == 'Video' and v1 != 0:
                v2 = vInfo(5, '%s' % track.codec_family,
                    '%s' % track.frame_rate, '%s' % track.display_aspect_ratio,
                    '%s' % track.width, '%s' % track.height,
                    '%s' % track.duration, '%s' % track.bit_rate_mode,
                    '%s' % track.bit_rate, '%s' % track.language,
                    '%s' % track.format)
            elif track.track_type == 'Audio' and a1 == 0:
                a1 = aInfo(5,  '%s' % track.codec_family,
                    '%s' % track.sampling_rate, '%s' % track.channel_s,
                    '%s' % track.bit_rate_mode, '%s' % track.bit_rate,
                    '%s' % track.duration, '%s' % track.language)
            elif track.track_type == 'Audio' and a1 != 0:
                a2 = aInfo(5,  '%s' % track.codec_family,
                    '%s' % track.sampling_rate, '%s' % track.channel_s,
                    '%s' % track.bit_rate_mode, '%s' % track.bit_rate,
                    '%s' % track.duration, '%s' % track.language)
            elif track.track_type == 'Text' and s1 == 0:
                s1 = sInfo(5, '%s' % track.format, '%s' % track.language)
            elif track.track_type == 'Text' and s1 != 0:
                s2 = sInfo(5, '%s' % track.format, '%s' % track.language)
            else:
                pass
        else:
            pass

    if tsIssue != 0:
        print_info()
    else:
        start_convert()

##############################################################################
# Added for Troubleshooting purposes
# Still need to output information to a file.
##############################################################################
def print_info():
    message2('Information from:')
    message4('%s' % bName)
    print 
    print 'Container Type    :', vContainer
    if v1 != 0:
        print 'Video track ID    :', v1.ID
        print 'Codec             :', v1.Codec
        print 'Frame Rate        :', v1.FRate
        print 'Aspect            :', v1.DisAsp
        print 'Width             :', v1.Width
        print 'Height            :', v1.Height
        print 'Duration          :', v1.Duration
        print 'Bit Rate Mode     :', v1.BRmode
        print 'Bit Rate          :', v1.BRate
        print 'Language          :', v1.Lang
        print 'Format            :', v1.Format
        print
    else:
        pass

    if v2 != 0:
        print 'Video track ID    :', v2.ID
        print 'Codec             :', v2.Codec
        print 'Frame Rate        :', v2.FRate
        print 'Aspect            :', v2.DisAsp
        print 'Width             :', v2.Width
        print 'Height            :', v2.Height
        print 'Duration          :', v2.Duration
        print 'Bit Rate Mode     :', v2.BRmode
        print 'Bit Rate          :', v2.BRate
        print 'Language          :', v2.Lang
        print 'Format            :', v2.Format
        print
    else:
        pass

    if a1 != 0:
        print 'Audio Track ID    :', a1.ID
        print 'Codec             :', a1.Codec
        print 'Sample            :', a1.Sample
        print 'Channels          :', a1.Channels
        print 'Bit Rate Mode     :', a1.BRmode
        print 'Bite Rate         :', a1.BRate
        print 'Duration          :', a1.Duration
        print 'Language          :', a1.Lang
        print
    else:
        pass

    if a2 != 0:
        print 'Audio Track ID    :', a2.ID
        print 'Codec             :', a2.Codec
        print 'Sample            :', a2.Sample
        print 'Channels          :', a2.Channels
        print 'Bit Rate Mode     :', a2.BRmode
        print 'Bite Rate         :', a2.BRate
        print 'Duration          :', a2.Duration
        print 'Language          :', a2.Lang
        print
    else:
        pass

    if s1 != 0:
        print 'Subtitle Track ID :', s1.ID
        print 'Format            :', s1.Format
        print 'Language          :', s1.Lang
        print
    else:
        pass

    if s2 != 0:
        print 'Subtitle Track ID :', s2.ID
        print 'Format            :', s2.Format
        print 'Language          :', s2.Lang
        print
    else:
        pass

    ts_clear()
    ts_pause()

    print config.filename

    ts_clear()
    ts_pause()

    print 'Keeping Both Audio Tracks?:', kDual
    print 'Swap the Audio Track?:', sAudio
    print 'Permanently add subtitles?:', burnSub
    print 'Remove temporary files when complete?:', delTemp

    print 'Video Aspect Ratio:', v1o.DisAsp
    print 'Video Width:', v1o.Width
    print 'Video Height:', v1o.Height
    print 'Video Bit Rate:', v1o.BRate
    print 'Video Frame Rate:', v1o.FRate

    print 'Audio 1 Sample Rate:', a1o.Sample
    print 'Audio 1 Channel count:', a1o.Channels
    print 'Audio 1 Bit Rate:', a1o.BRate

    print 'Audio 2 Sample Rate:', a2o.Sample
    print 'Audio 2 Channel count:', a2o.Channels
    print 'Audio 2 Bit Rate:', a2o.BRate

    ts_pause()
    var_reset()

##############################################################################
# Reset Variables
##############################################################################
def var_reset():
    global fName, WD, bName, eXtsn, vContainer, vCount
    global aCount, sCount, tCount, v1, v2, a1, a2, s1, s2
    fName = WD = bName = eXtsn = vContainer = vCount = 0
    aCount = sCount = tCount = v1 = v2 = a1 = a2 = s1 = s2 = 0

##############################################################################
# Begin the conversion definitions
##############################################################################
def start_convert():
    os.chdir('%s' % WD)
    ts_clear()
    message2('Copying original into:')
    message4('%s/Temp' % WD)
    subprocess.call(['mkdir', '-p', '%s/Temp' % WD])
    subprocess.call(['mkdir', '-p', '%s/Completed' % WD])
    shutil.copy('%s' % fName, '%s/Temp/%s%s' % (WD, bName, eXtsn))
    ts_clear()
    ts_pause()
    message('Finished copying. Starting Subtitle Extraction')
    os.chdir('%s/Temp' % WD)
    if sCount != None:
        if vContainer == 'Matroska':
            if s2 != 0:
                subprocess.call(['mkvextract', 'tracks',
                '%s%s' % (bName, eXtsn),
                '%s:%s_sub1.tmp' % (s1.ID, bName),
                '%s:%s_sub2.tmp' % (s2.ID, bName)])
                if s1.Format == 'UTF-8':
                    shutil.copy('%s_sub1.tmp' % bName,
                    '%s/Completed/%s.srt' % (WD, bName))
                else:
                    shutil.copy('%s_sub1.tmp' % bName,
                    '%s/Completed/%s.%s' % (WD, bName, s1.Format))
                if s2.Format == 'UTF-8':
                    shutil.copy('%s_sub2.tmp' % bName,
                    '%s/Completed/%s.srt' % (WD, bName))
                else:
                    shutil.copy('%s_sub2.tmp' % bName,
                    '%s/Completed/%s.%s' % (WD, bName, s2.Format))
            else:
                subprocess.call(['mkvextract', 'tracks',
                '%s%s' % (bName, eXtsn),
                '%s:%s_sub.tmp' % (s1.ID, bName)])
                if s1.Format == 'UTF-8':
                    shutil.copy('%s_sub1.tmp' % bName,
                    '%s/Completed/%s.srt' % (WD, bName))
                else:
                    shutil.copy('%s_sub1.tmp' % bName,
                    '%s/Completed/%s.%s' % (WD, bName, s1.Format))
        elif vContainer == 'OGG':
            subprocess.call(['ogmdemux', '--output', '%s' % bName,
            '-na', '-nv', '%s%s' % (bName, eXtsn)])
            subprocess.call(['cp', '%s-t*.*' % bName,
            '%s/Completed/' % WD])
        else:
            message2('Sadly we cannot extract subtitles from this video')
            message4('at this time. Please try again after the next update.')
    else:
        print 'No Subtitles Found in this video'
    ts_clear()

    message('Moving onto Video')
    if int(vCount) == 1:
        subprocess.call(['ffmpeg', '-i', '%s%s' % (bName, eXtsn), '-an',
        '-vtag', 'XVID', '-vcodec', 'libxvid', '-b', '%s' % v1.BRate,
        '-s', '%sx%s' % (v1.Width, v1.Height), '-pass', '1', '-passlogfile',
        '%s' % bName, '-aspect', '%s' % v1.DisAsp, '%s_pass1.avi' % bName])
    else:
        print 'Unsupported number of video tracks'
    ts_pause()
    ts_clear()

    message('Proceeding with Audio now')
    if int(aCount) >= 1:
        subprocess.call(['ffmpeg', '-i', '%s%s' % (bName, eXtsn), '-vn',
        '-acodec', 'libmp3lame', '-ab', '%s' % a1.BRate, '-ar',
        '%s' % a1.Sample, '-ac', '%s' % a1.Channels, '-atag', 'MP3',
        '%s_temp(%s.%s).mp3' % (bName, a1.ID, a1.Lang)])
        if a2 != 0 and a2 != None:
            subprocess.call(['ffmpeg', '-i', '%s%s' % (bName, eXtsn), '-vn',
            '-acodec', 'libmp3lame', '-ab', '%s' % a2.BRate, '-ar',
            '%s' % a2.Sample, '-ac', '%s' % a2.Channels, '-atag', 'MP3',
            '%s_temp(%s.%s).mp3' % (bName, a2.ID, a2.Lang)])
        else:
            pass
    else:
        print 'Unsupported number of audio tracks/no audio found'
    ts_pause()
    ts_clear()

    message('Extraction done. Beginning the muxing process.')
    if int(aCount) == 1:
        subprocess.call(['ffmpeg', '-i', '%s_pass1.avi' % bName, '-vcodec',
        'copy', '-i', '%s_temp(%s.%s).mp3' % (bName, a1.ID, a1.Lang),
        '-acodec', 'copy', '-ab', '%s' % a1.BRate, '-ar', '%s' % a1.Sample,
        '-ac', '%s' % a1.Channels, '%s[completed].avi' % bName])
        ts_pause()
        ts_clear()

    elif int(aCount) == 2:
        if SwapAudio == 0:
            subprocess.call(['ffmpeg', '-i', '%s_pass1.avi' % bName,
            '-vcodec', 'copy', '-i',
            '%s_temp(%s.%s).mp3' % (bName, a2.ID, a2.Lang),
            '-acodec', 'libmp3lame', '-alang', '%s' % a2.Lang,
            '%s_pass2.avi' % bName])
            ts_pause()

            subprocess.call(['ffmpeg', '-i', '%s_pass2.avi' % bName,
            '-vcodec', 'copy', '-i',
            '%s_temp(%s.%s).mp3' % (bName, a1.ID, a1.Lang),
            '-acodec', 'libmp3lame', '%s[completed].avi' % bName, '-acodec',
            'libmp3lame', '-newaudio'])
            ts_pause()
            ts_clear()

        elif SwapAudio == 1:
            subprocess.call(['ffmpeg', '-i', '%s_pass1.avi' % bName,
            '-vcodec', 'copy', '-i',
            '%s_temp(%s.%s).mp3' % (bName, a1.ID, a1.Lang),
            '-acodec', 'libmp3lame', '-alang', '%s' % a1.Lang,
            '%s/Temp/%s_pass2.avi' % bName])
            ts_pause()

            subprocess.call(['ffmpeg', '-i', '%s_pass2.avi' % (WD, bName),
            '-vcodec', 'copy', '-i',
            '%s_temp(%s.%s).mp3' % (bName, a2.ID, a2.Lang),
            '-acodec', 'libmp3lame', '%s[completed].avi' % (bName), '-acodec',
            'libmp3lame', '-newaudio'])
            ts_pause()
            ts_clear()
        else:
            pass
    else:
        print 'Unsupported number of Audio tracks'

    message2('Video conversion complete. Moving completed file(s) to:')
    message4('%s/Completed' % WD)
    shutil.copy('%s/Temp/%s[completed].avi' % (WD, bName),
    '%s/Completed/%s.avi' % (WD, bName))
    ts_pause()
    ts_clear()
    del_temp()

    message2('Copy complete, if there are more videos in the queue')
    message4('the next one will start converting in about 5 seconds')
    time.sleep(5)
    var_reset()

##############################################################################
# This section actually starts everything
##############################################################################
if len(sys.argv) < 2:
    try:
        with open('%s/user.cfg' % cfgDir) as f:
            ts_clear()
            logger1.info('User configuration not found.')
            while True:
                ts_clear()
                print
                resetPrompt = raw_input('Would you like to run through the '
                              'configuration again?\n Yes or No\n').lower()
                if resetPrompt in yes:
                    create_config()
                    break
                elif resetPrompt in no:
                    ts_clear()
                    usage()
                    break
                else:
                    subprocess.call('clear')
                    print
                    print 'I\'m sorry, I do not understand your response'
                    print 'Please try again.. '
    except IOError as e:
        logger1.warning('File containing user settings does not exist,\n'
                        'this will be corrected.')    
        create_config()

else:
    fName = sys.argv[1]
    for fName in wList:
        try:
            with open('%s/user.cfg' % cfgDir) as f:
                read_config()
        except IOError as e:
            logger1.warning('File containing user settings does not exist,\n'
                        'this will be corrected.')    
            create_config()
            read_config()

    ts_clear()
    message('It seems the queue is empty, stopping program.')
    print
    raw_input('Please press \'ENTER\' to exit')
