import os,string,pickle,math,sys
import collections
em={}
em['a']={}
em['a']['b']='c'
if 'c' in em.get('a', {}):
	print 'Im'
else:
	print 'out'

