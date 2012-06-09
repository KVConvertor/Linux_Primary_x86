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
##############################################################################

##############################################################################
# Imports
##############################################################################
import sys, os, subprocess, linecache, string, shutil, time
from collections import deque
from pymediainfo import MediaInfo

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
# General
usrSwapAud = 0
usrDelTemp = 1

#=============================================================================
# Filename/File Variables.
#=============================================================================
wlist = sys.argv[1:]
Fname = 0
WD = 0
Bname = 0
Extsn = 0

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
# Error Counts (Not used yet!)
#=============================================================================
vError = 0
aError = 0
sError = 0

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
        raw_input('Process paused, press ENTER to continue')
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

##############################################################################
# Start the process of getting source video information
##############################################################################
def get_video_info():
    global Fname, WD, Bname, Extsn, v1, v2, a1, a2, s1, s2
    global vCount, aCount, sCount, vContainer
    WD = os.path.dirname('%s' % Fname)
    Bname = Fname[(len(WD)+1):-4]
    Extsn = Fname[-4:]
    os.chdir('%s' % WD)
    ts_clear()
    message('Obtaining video information. Please wait...')
    print
    mInfo = MediaInfo.parse('%s' % Fname)
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
    message4('%s' % Bname)
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

    ts_pause()
    var_reset()

##############################################################################
# Reset Variables
##############################################################################
def var_reset():
    global Fname, WD, Bname, Extsn, vContainer, vCount
    global aCount, sCount, tCount, v1, v2, a1, a2, s1, s2
    Fname = WD = Bname = Extsn = vContainer = vCount = 0
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
    shutil.copy('%s' % Fname, '%s/Temp/%s%s' % (WD, Bname, Extsn))
    ts_clear()
    ts_pause()
    message('Finished copying. Starting Subtitle Extraction')
    os.chdir('%s/Temp' % WD)
    if sCount != None:
        if vContainer == 'Matroska':
            if s2 != 0:
                subprocess.call(['mkvextract', 'tracks',
                '%s%s' % (Bname, Extsn),
                '%s:%s_sub1.tmp' % (s1.ID, Bname),
                '%s:%s_sub2.tmp' % (s2.ID, Bname)])
                if s1.Format == 'UTF-8':
                    shutil.copy('%s_sub1.tmp' % Bname,
                    '%s/Completed/%s.srt' % (WD, Bname))
                else:
                    shutil.copy('%s_sub1.tmp' % Bname,
                    '%s/Completed/%s.%s' % (WD, Bname, s1.Format))
                if s2.Format == 'UTF-8':
                    shutil.copy('%s_sub2.tmp' % Bname,
                    '%s/Completed/%s.srt' % (WD, Bname))
                else:
                    shutil.copy('%s_sub2.tmp' % Bname,
                    '%s/Completed/%s.%s' % (WD, Bname, s2.Format))
            else:
                subprocess.call(['mkvextract', 'tracks',
                '%s%s' % (Bname, Extsn),
                '%s:%s_sub.tmp' % (s1.ID, Bname)])
                if s1.Format == 'UTF-8':
                    shutil.copy('%s_sub1.tmp' % Bname,
                    '%s/Completed/%s.srt' % (WD, Bname))
                else:
                    shutil.copy('%s_sub1.tmp' % Bname,
                    '%s/Completed/%s.%s' % (WD, Bname, s1.Format))
        elif vContainer == 'OGG':
            subprocess.call(['ogmdemux', '--output', '%s' % Bname,
            '-na', '-nv', '%s%s' % (Bname, Extsn)])
            subprocess.call(['cp', '%s-t*.*' % Bname,
            '%s/Completed/' % WD])
        else:
            message2('Sadly we cannot extract subtitles from this video')
            message4('at this time. Please try again after the next update.')
    else:
        print 'No Subtitles Found in this video'
    ts_clear()

    message('Moving onto Video')
    if int(vCount) == 1:
        subprocess.call(['ffmpeg', '-i', '%s%s' % (Bname, Extsn), '-an',
        '-vtag', 'XVID', '-vcodec', 'libxvid', '-b', '%s' % v1.BRate,
        '-s', '%sx%s' % (v1.Width, v1.Height), '-pass', '1', '-passlogfile',
        '%s' % Bname, '-aspect', '%s' % v1.DisAsp, '%s_pass1.avi' % Bname])
    else:
        print 'Unsupported number of video tracks'
    ts_pause()
    ts_clear()

    message('Proceeding with Audio now')
    if int(aCount) >= 1:
        subprocess.call(['ffmpeg', '-i', '%s%s' % (Bname, Extsn), '-vn',
        '-acodec', 'libmp3lame', '-ab', '%s' % a1.BRate, '-ar',
        '%s' % a1.Sample, '-ac', '%s' % a1.Channels, '-atag', 'MP3',
        '%s_temp(%s.%s).mp3' % (Bname, a1.ID, a1.Lang)])
        if a2 != 0 and a2 != None:
            subprocess.call(['ffmpeg', '-i', '%s%s' % (Bname, Extsn), '-vn',
            '-acodec', 'libmp3lame', '-ab', '%s' % a2.BRate, '-ar',
            '%s' % a2.Sample, '-ac', '%s' % a2.Channels, '-atag', 'MP3',
            '%s_temp(%s.%s).mp3' % (Bname, a2.ID, a2.Lang)])
        else:
            pass
    else:
        print 'Unsupported number of audio tracks/no audio found'
    ts_pause()
    ts_clear()

    message('Extraction done. Beginning the muxing process.')
    if int(aCount) == 1:
        subprocess.call(['ffmpeg', '-i', '%s_pass1.avi' % Bname, '-vcodec',
        'copy', '-i', '%s_temp(%s.%s).mp3' % (Bname, a1.ID, a1.Lang),
        '-acodec', 'copy', '-ab', '%s' % a1.BRate, '-ar', '%s' % a1.Sample,
        '-ac', '%s' % a1.Channels, '%s[completed].avi' % Bname])
        ts_pause()
        ts_clear()

    elif int(aCount) == 2:
        if SwapAudio == 0:
            subprocess.call(['ffmpeg', '-i', '%s_pass1.avi' % Bname,
            '-vcodec', 'copy', '-i',
            '%s_temp(%s.%s).mp3' % (Bname, a2.ID, a2.Lang),
            '-acodec', 'libmp3lame', '-alang', '%s' % a2.Lang,
            '%s_pass2.avi' % Bname])
            ts_pause()

            subprocess.call(['ffmpeg', '-i', '%s_pass2.avi' % Bname,
            '-vcodec', 'copy', '-i',
            '%s_temp(%s.%s).mp3' % (Bname, a1.ID, a1.Lang),
            '-acodec', 'libmp3lame', '%s[completed].avi' % Bname, '-acodec',
            'libmp3lame', '-newaudio'])
            ts_pause()
            ts_clear()

        elif SwapAudio == 1:
            subprocess.call(['ffmpeg', '-i', '%s_pass1.avi' % Bname,
            '-vcodec', 'copy', '-i',
            '%s_temp(%s.%s).mp3' % (Bname, a1.ID, a1.Lang),
            '-acodec', 'libmp3lame', '-alang', '%s' % a1.Lang,
            '%s/Temp/%s_pass2.avi' % Bname])
            ts_pause()

            subprocess.call(['ffmpeg', '-i', '%s_pass2.avi' % (WD, Bname),
            '-vcodec', 'copy', '-i',
            '%s_temp(%s.%s).mp3' % (Bname, a2.ID, a2.Lang),
            '-acodec', 'libmp3lame', '%s[completed].avi' % (Bname), '-acodec',
            'libmp3lame', '-newaudio'])
            ts_pause()
            ts_clear()
        else:
            pass
    else:
        print 'Unsupported number of Audio tracks'

    message2('Video conversion complete. Moving completed file(s) to:')
    message4('%s/Completed' % WD)
    shutil.copy('%s/Temp/%s[completed].avi' % (WD, Bname),
    '%s/Completed/%s.avi' % (WD, Bname))
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
    usage()
    raw_input('Please press \'ENTER\' to exit')
else:
    Fname = sys.argv[1]
    for Fname in wlist:
        get_video_info()
    ts_clear()
    message('It seems the queue is empty, stopping program.')
    print
    raw_input('Please press \'ENTER\' to exit')
