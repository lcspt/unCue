# from github.com/Theldus/cue_to_flac.py

import os
import shutil


class split():
    def __init__(self):
        
        self.cue_file = r'D:\test\1997 The Drop\Brian Eno - The Drop (HNCD1479).cue'
        self.path = os.path.split(self.cue_file)[0]
        self.outfiles = []
        
    def split(self):

        d = open(self.cue_file).read().splitlines()
        
        general = {}
        
        tracks = []
        outfiles = []
        
        current_file = None
        
        for line in d:
            if line.startswith('REM GENRE '):
                general['genre'] = ' '.join(line.split(' ')[2:])
            if line.startswith('REM DATE '):
                general['date'] = ' '.join(line.split(' ')[2:])
            if line.startswith('PERFORMER '):
                general['artist'] = ' '.join(line.split(' ')[1:]).replace('"', '')
            if line.startswith('TITLE '):
                general['album'] = ' '.join(line.split(' ')[1:]).replace('"', '')
            if line.startswith('FILE '):
                current_file = os.path.join(self.path, ' '.join(line.split(' ')[1:-1]).replace('"', ''))
            
            if line.startswith('  TRACK '):
                track = general.copy()
                track['track'] = int(line.strip().split(' ')[1], 10)
        
                tracks.append(track)
        
            if line.startswith('    TITLE '):
                tracks[-1]['title'] = ' '.join(line.strip().split(' ')[1:]).replace('"', '')
            if line.startswith('    PERFORMER '):
                tracks[-1]['artist'] = ' '.join(line.strip().split(' ')[1:]).replace('"', '')
            if line.startswith('    INDEX 01 '):
                t = list(map(int, ' '.join(line.strip().split(' ')[2:]).replace('"', '').split(':')))
                tracks[-1]['start'] = 60 * t[0] + t[1] + t[2] / 100.0
        
        for i in range(len(tracks)):
            if i != len(tracks) - 1:
                tracks[i]['duration'] = tracks[i + 1]['start'] - tracks[i]['start']
        
        for track in tracks:
            metadata = {
                'artist': track['artist'],
                'title': track['title'],
                'album': track['album'],
                'track': str(track['track']) + '/' + str(len(tracks))
            }
        
            if 'genre' in track:
                metadata['genre'] = track['genre']
            if 'date' in track:
                metadata['date'] = track['date']
        
            cmd = 'ffmpeg'
            cmd += ' -i "%s"' % current_file
            cmd += ' -ss %.2d:%.2d:%.2d' % (track['start'] / 60 / 60, track['start'] / 60 % 60, int(track['start'] % 60))
        
            if 'duration' in track:
                cmd += ' -t %.2d:%.2d:%.2d' % (track['duration'] / 60 / 60, track['duration'] / 60 % 60, int(track['duration'] % 60))
        
            cmd += ' ' + ' '.join('-metadata %s="%s"' % (k, v) for (k, v) in metadata.items())
            #outfile = ' \"' + os.path.join(self.path, "%s - %.2d - %s - %s.flac" % (track['album'], track['track'],track['artist'], track['title'])) + '\"'
            outfile = "%s - %.2d - %s - %s.flac" % (track['album'], track['track'],track['artist'], track['title'])
            cmd +=  ' \"' + os.path.join(self.path, outfile) + '\"'
            self.outfiles.append(outfile)
            os.system (cmd)
        

    def moveFiles(self):
        newDir = 'files'
        to_directory = os.path.join(self.path, newDir)
        print(to_directory)
        if not os.path.exists(to_directory):
            os.makedirs(to_directory)
        print('check ' +self.path)
        print(self.outfiles)
        for filename in os.scandir(self.path):
            print(filename.name)
            if (filename.name in  self.outfiles):
                source = os.path.join(self.path, filename
                dest = shutil.move(source, to_directory)
                print(f"Moved {filename} to {dest}")

splitter = split()
splitter.split()
splitter.moveFiles()
