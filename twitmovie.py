#!/usr/bin/python
import sys,re,os,shutil, json
import subprocess
import argparse, fnmatch

TMPFILE='tmp.srt'

parser = argparse.ArgumentParser(description='')
parser.add_argument('movie', metavar='MOVIE', type=str,
                    help='The movie to convert')
parser.add_argument('-o', '--out', metavar='OUTFILE', dest='outfile', action='store', type=str,
                    help='destination file. Defaults to MOVIE-twitter.mp4')
parser.add_argument('-y', '--force', dest='overwrite', action='store_true',
                    help='Overwrite OUTFILE if it exists, without prompting')
parser.add_argument('-n', '--noscale', dest='scale', default=True,
					action='store_false',
                    help='Turn off rescaling to 640 by ?. Sometimes needed for odd-sized videos')
args = parser.parse_args()

if args.outfile is None:
	args.outfile = os.path.splitext(args.movie)[0] + '-twitter.mp4'

if os.path.exists(args.outfile) and not args.overwrite:
	response = raw_input('{} exists, overwrite? [y]'.format(args.outfile))
	if response not in ('','y','Y'):
		sys.exit()


cmd = [
	'ffmpeg',
	'-v','error',
	'-y',
	'-i',args.movie,
	'-pix_fmt', 'yuv420p', '-vcodec', 'libx264',
]
if args.scale:
	cmd.extend(['-vf', 'scale=640:-1'])
cmd.extend([
	'-acodec', 'aac',
	'-vb', '1024k',
	'-minrate', '1024k',
	'-maxrate', '1024k',
	'-bufsize', '1024k',
	'-ar', '44100',
	'-ac', '2',
	'-strict', 'experimental',
	'-r', '30',
	args.outfile
])

p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
stdout,_ = p.communicate()
if p.returncode != 0:
	print 'Failed!'
	print stdout

