# _*_ coding:utf-8 _*_

#   Tiny WebDav Server for Pythonista - IOS.  (Base on pandav WebDav server )
#
#   (C)2013/11                                        By: Lai ChuJiang
#
#  this code can run not just Pythonista on IOS ,also run on OSX python.
#  Support Client: Windows / OSX / other Webdav client for IOS,etc : goodreader / iWorks for ios 
#
# 20170907 Change Log:
#  1. Fix Coda WebDav access problem.(because Coda WebDav all xml item add xmlns="DAV:".)
# 
# 2013/11  Change Log:
# 1. Combind all files to one file,so can using for Pythonista easy.
# 2. Add MKCOL(Create dir); MOVE(rename file);  DELETE(delete file or dir);  COPY (Copy file)   
# 3. Change some decode, Now it's can support Chinese.
# 4. Pythonista(For IOS) not dircache module ,so change code,don't using this module.
# 5. change DAV version from 1 to 2, so the OSX finder can write.   
# 6. for DAV version 2 support , add LOCK / UNLOCK fake support. (not real lock file)
#       *** !!!! So Don't using > 1 client sametime write or delete same file. maybe lost files.
# 7. Change the do_PROPFIND module, now it's simply & right for OSX 
# 8. Change the do_GET module, now support RANGE
# 9. Change the do_PUB module, add Content-Length=0 support (create empty file) ,so the OSX Finder support. 
#        *if not add empty file,the Finder copy files and then delete all this.
#10. Add WebDav Basic Auth function,now you can set user & passwd
#         **using wdusers.conf file (just user:passwd), if not this file ,the Auth disable.
#11. Fix the broken pipe error message
#
#   WebDav RFC: http://www.ics.uci.edu/~ejw/authoring/protocol/rfc2518.html
#                   http://restpatterns.org/HTTP_Methods
#
# Base : pandav v0.2 
# Copyright (c) 2005.-2006. Ivan Voras <ivoras@gmail.com>
# Released under the Artistic License
#

#modified by D. Baddeley to use PYME Cluster IO as a backend, 2018

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from SocketServer import ThreadingMixIn
from io import StringIO
import sys,urllib,re,urlparse
from time import time, timezone, strftime, localtime, gmtime
import os, shutil, uuid, md5, mimetypes, base64
import socket
import ssl

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

from PYME.IO import clusterIO
from PYME.IO import clusterListing

from io import BytesIO

def makedirs_safe(dir):
    """
    A safe wrapper for makedirs, which won't throw an error if the directory already exists. This replicates the functionality
    of the exists_ok flag in  the python 3 version of os.makedirs, but should work with both pytion 2 and python 3.

    Parameters
    ----------
    dir : str, directory to be created

    Returns
    -------

    """
    import errno
    try:
        os.makedirs(dir)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

# 获取本机IP地址
def get_localip():
    try:
       gAdd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
       gAdd.connect(('www.bing.com', 80))
       return gAdd.getsockname()[0]
    except:
       return '127.0.0.1'

class Member:
    M_MEMBER = 1           
    M_COLLECTION = 2        
    def getProperties(self):
        return {}  

class Collection(Member):
    def __init__(self, name):
        self.name = name
    def getMembers(self):
        return []
        
class FileMember(Member):
    def __init__(self, name, parent):
        self.name = name
        self.parent = parent
        self.name = name
        self.fsname = parent.fsname + name      # e.g. '/var/www/mysite/some.txt'
        self.virname = parent.virname + name    # e.g. '/mysite/some.txt'
        self.type = Member.M_MEMBER

    def __str__(self):
        return "%s -> %s" % (self.virname, self.fsname)

    def getProperties(self):
        """Return dictionary with WebDAV properties. Values shold be
        formatted according to the WebDAV specs."""
        st = clusterIO.stat(self.fsname)
        p = {}
        p['creationdate'] = unixdate2iso8601(st.st_ctime)
        p['getlastmodified'] = unixdate2httpdate(st.st_mtime)
        p['displayname'] = self.name
        p['getetag'] = md5.new(self.fsname).hexdigest()
        if self.type == Member.M_MEMBER:
            p['getcontentlength'] = st.st_size
            p['getcontenttype'], z = mimetypes.guess_type(self.name)
            p['getcontentlanguage'] = None
        else:   # Member.M_COLLECTION
            p['resourcetype'] = '<D:collection/>'
        if self.name[0] == ".":
            p['ishidden'] = 1
        if True:# not os.access(self.fsname, os.W_OK):
            p['isreadonly'] = 1
        if self.name == '/':
            p['isroot'] = 1
        return p

    def sendData(self, wfile,bpoint=0,epoint=0):
        """Send the file to the client. Literally."""
        data = clusterIO.get_file(self.fsname)
        f_size = len(data)
        #st = clusterIO.stat(self.fsname)
        #with open(self.fsname, 'rb') as f:
        f =  BytesIO(data) #TODO - does this make sense?
        writ = 0
        # for send Range xxx-xxx
        if bpoint>0 and bpoint<f_size:
            f.seek(bpoint)
        
        if epoint>bpoint:
            if epoint<=f_size:
                rsize = epoint - bpoint + 1
            else:
                rsize = f_size - bpoint
        else:
            rsize = f_size
            
            
        while writ < rsize:
            if (rsize - writ) < 65536:
                buf = f.read(rsize)
            else:
                buf = f.read(65536)
            if not buf:
                break
            writ += len(buf)
            wfile.write(buf)

class DummyFileMember(FileMember):
    def getProperties(self):
        p = {}
        p['creationdate'] = unixdate2iso8601(time())
        p['getlastmodified'] = unixdate2httpdate(time())
        p['displayname'] = self.name
        p['getetag'] = md5.new(self.fsname).hexdigest()
        if self.type == Member.M_MEMBER:
            p['getcontentlength'] = 0
            p['getcontenttype'], z = mimetypes.guess_type(self.name)
            p['getcontentlanguage'] = None
        else:   # Member.M_COLLECTION
            p['resourcetype'] = '<D:collection/>'
        if self.name[0] == ".":
            p['ishidden'] = 1
        if True:# not os.access(self.fsname, os.W_OK):
            p['isreadonly'] = 1
        if self.name == '/':
            p['isroot'] = 1
        return p


class DirCollection(FileMember, Collection):
    COLLECTION_MIME_TYPE = 'httpd/unix-directory'           # application/x-collection ？
    def __init__(self, fsdir, virdir, parent=None):
        if not clusterIO.exists(fsdir):
            raise RuntimeError("Local directory (fsdir) not found: " + fsdir)
        self.fsname = fsdir
        self.name = virdir
        if self.fsname[-1] != os.sep:
            if self.fsname[-1] == '/': # fixup win/dos/mac separators
                self.fsname = self.fsname[:-1] + os.sep
            else:
                self.fsname += os.sep
        self.virname = virdir
        if self.virname[-1] != '/':
            self.virname += '/'
        self.parent = parent
        self.type = Member.M_COLLECTION

    def getProperties(self):
        p = FileMember.getProperties(self) # inherit file properties
        p['iscollection'] = 1
        p['getcontenttype'] = DirCollection.COLLECTION_MIME_TYPE
        p['getcontentlength'] = 0
        return p

    def getMembers(self):
        """Get immediate members of this collection."""
        l = clusterIO.listdirectory(self.fsname) # obtain a copy of dirlist
        #tcount=0
        #for tmpi in l:
        #        if os.path.isfile(self.fsname+tmpi) == False:
        #                l[tcount]=l[tcount]+'/'
        #        tcount += 1
        
        
        r = []
        for fn, f_info in l.items():
            if f_info.type == clusterListing.FILETYPE_NORMAL:
                m = FileMember(fn, self) # Member is a file
            else:
                m = DirCollection(self.fsname + fn, self.virname + fn, self) # Member is a collection
            r.append(m)
            
        for d_ in _temporary_directories:
            real_dirs = l.keys()
            if d_ in real_dirs or (d_ + '/') in real_dirs:
                _temporary_directories.remove(d_)
            
            if d_.startswith(self.fsname):
                d__ = d_[len(self.fsname):]
                if len(d__.lstrip('/').rstrip('/').split('/')) == 1:
                    #temporary directory is at this level
                    r.append(TempDirCollection(d_, self.virname + d__))
                    
        for f_ in _dummy_files:
            if f_.startswith(self.fsname):
                f__ = f_[len(self.fsname):]
                if len(f__.lstrip('/').rstrip('/').split('/')) == 1:
                    #temporary directory is at this level
                    r.append(DummyFileMember(f__.lstrip('/'), self))
                
        #print _temporary_directories
        #print [str(r_) for r_ in r]
        
        return r

        # Return WebDav Root Dir info
    def rootdir(self):
        return self.fsname
        
    def findMember(self, name):
        """Search for a particular member."""
        #l = os.listdir(self.fsname) # obtain a copy of dirlist
        l = clusterIO.listdirectory(self.fsname)
        # tcount=0
        # for tmpi in l:
        #         if os.path.isfile(self.fsname+tmpi) == False:
        #                 l[tcount]=l[tcount]+'/'
        #         tcount += 1
            
        
        # if name in l:
        #     if name[-1] != '/':
        #         return FileMember(name, self)
        #     else:
        #         return DirCollection(self.fsname + name, self.virname + name, self)
        
        try:
            info = l[name]
            if info.type == clusterListing.FILETYPE_NORMAL:
                return FileMember(name, self)
            else:
                return DirCollection(self.fsname + name, self.virname + name, self)
        except KeyError:
            pass
            
        fname = (self.fsname.rstrip('/') + '/' + name.lstrip('/'))
        if fname in _dummy_files:
            return DummyFileMember(name, self)
            
        name += '/'
        #print (self.fsname + name), _temporary_directories
        if name in l.keys():
            return DirCollection(self.fsname + name, self.virname + name, self)
        elif (self.fsname + name).rstrip('/') in _temporary_directories:
            return TempDirCollection(self.fsname + name, self.virname + name, self)

    def sendData(self, wfile):
        """Send "file" to the client. Since this is a directory, build some arbitrary HTML."""
        memb = self.getMembers()
        data = '<html><head><title>%s</title></head><body>' % self.virname
        data += '<table><tr><th>Name</th><th>Size</th><th>Timestamp</th></tr>'
        for m in memb:
            p = m.getProperties()
            if 'getcontentlength' in p:
                p['size'] = int(p['getcontentlength'])
                p['timestamp'] = p['getlastmodified']
            else:
                p['size'] = 0
                p['timestamp'] = '-DIR-'
            data += '<tr><td>%s</td><td>%d</td><td>%s</td></tr>' % (p['displayname'], p['size'], p['timestamp'])
        data += '</table></body></html>'
        wfile.write(data)

    def recvMember(self, rfile, name, size, req):
        """Receive (save) a member file"""
            
        fname = os.path.join(self.fsname, urllib.unquote(name))
        
        if size==0:
            _dummy_files.append(fname)
            return
        else:
            try:
                _dummy_files.remove(fname)
            except ValueError:
                pass
        
        #f = file(fname, 'wb')
        f = BytesIO()
        # if size=-1 it's Transfer-Encoding: Chunked mode, like OSX finder using this mode put data
        # so the file size need get here.
        if size == -2:
            l = int(rfile.readline(), 16)
            ltotal = 0
            while l > 0:
                buf = rfile.read(l)
                f.write(buf)        #yield buf
                rfile.readline()
                ltotal += l
                l = int(rfile.readline(), 16)
        elif size > 0:      # if size=0 ,just save a empty file.
            writ = 0
            bs = 65536
            while True:
                if size != -1 and (bs > size-writ):
                    bs = size-writ
                buf = rfile.read(bs)
                if len(buf) == 0:
                    break
                f.write(buf)
                writ += len(buf)
                if size != -1 and writ >= size:
                    break
        
        logger.debug('ClusterIO put: %s' % fname)
        clusterIO.put_file(fname, f.getvalue())
        
        f.close()

class TempDirCollection(DirCollection):
    """Temporary directories do not exist on disk. They are held in
    memory on the server to provide a mechanism for creating new
    directories with the create + rename/move mechanism used by most OSs"""
    
    def __init__(self, fsdir, virdir, parent=None):
        self.fsname = fsdir
        self.name = virdir
        if self.fsname[-1] != os.sep:
            if self.fsname[-1] == '/': # fixup win/dos/mac separators
                self.fsname = self.fsname[:-1] + os.sep
            else:
                self.fsname += os.sep
        self.virname = virdir
        if self.virname[-1] != '/':
            self.virname += '/'
        self.parent = parent
        self.type = Member.M_COLLECTION
        self.ctime = time()
        
    def getProperties(self):
        """Return dictionary with WebDAV properties. Values shold be
        formatted according to the WebDAV specs."""
        #st = os.stat(self.fsname)
        p = {}
        p['creationdate'] = unixdate2iso8601(self.ctime)
        p['getlastmodified'] = unixdate2httpdate(self.ctime)
        p['displayname'] = self.name
        p['getetag'] = md5.new(self.fsname).hexdigest()
        
        # Member.M_COLLECTION
        p['resourcetype'] = '<D:collection/>'
        p['iscollection'] = 1
        p['getcontenttype'] = DirCollection.COLLECTION_MIME_TYPE
    
        if self.name[0] == ".":
            p['ishidden'] = 1
        if True:# not os.access(self.fsname, os.W_OK):
            p['isreadonly'] = 1
        if self.name == '/':
            p['isroot'] = 1
        return p
    
    def getMembers(self):
        r = []

        for d_ in _temporary_directories:
            if d_.startswith(self.fsname):
                d__ = d_[len(self.fsname):]
                if len(d__.lstrip('/').rstrip('/').split('/')) == 1:
                    #temporary directory is at this level
                    r.append(TempDirCollection(d_, self.virname + d__))
    
        return r

    
    def findMember(self, name):
        if (self.fsname + name).rstrip('/') in _temporary_directories:
            return TempDirCollection(self.fsname + name, self.virname + name, self)
    
    def recvMember(self, rfile, name, size, req):
        #actually create the directory
        #makedirs_safe(self.fsname)
        #_temporary_directories.remove(self.fsname.rstrip('/'))
        
        DirCollection.recvMember(self, rfile, name, size, req)
    
def unixdate2iso8601(d):
    tz = timezone / 3600 # can it be fractional?
    tz = '%+03d' % tz
    return strftime('%Y-%m-%dT%H:%M:%S', localtime(d)) + tz + ':00'

def unixdate2httpdate(d):
    return strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime(d))
  
class Tag:
    def __init__(self, name, attrs, data='', parser=None):
        self.d = {}
        self.name = name
        self.attrs = attrs
        if type(self.attrs) == type(''):
            self.attrs = splitattrs(self.attrs)
        for a in self.attrs:
            if a.startswith('xmlns'):
                nsname = a[6:]
                parser.namespaces[nsname] = self.attrs[a]
        self.rawname = self.name

        p = name.find(':')
        if p > 0:
            nsname = name[0:p]
            if nsname in parser.namespaces:
                self.ns = parser.namespaces[nsname]
                self.name = self.rawname[p+1:]
        else:
            self.ns = ''
        self.data = data

    # Emulate dictionary d
    def __len__(self):
        return len(self.d)

    def __getitem__(self, key):
        return self.d[key]

    def __setitem__(self, key, value):
        self.d[key] = value

    def __delitem__(self, key):
        del self.d[key]

    def __iter__(self):
        return self.d.iterkeys()

    def __contains__(self, key):
        return key in self.d

    def __str__(self):
        """Returns unicode semi human-readable representation of the structure"""
        if self.attrs:
            s = u'<%s %s> %s ' % (self.name, self.attrs, self.data)
        else:
            s = u'<%s> %s ' % (self.name, self.data)

        for k in self.d:
            if type(self.d[k]) == type(self):
                s += u'|%s: %s|' % (k, str(self.d[k]))
            else:
                s += u'|' + u','.join([str(x) for x in self.d[k]]) + u'|'
        return s

    def addChild(self, tag):
        """Adds a child to self. tag must be instance of Tag"""
        if tag.name in self.d:
            if type(self.d[tag.name]) == type(self): # If there are multiple sibiling tags with same name, form a list :)
                self.d[tag.name] = [self.d[tag.name]]
            self.d[tag.name].append(tag)
        else:
            self.d[tag.name] = tag
        return tag

class XMLDict_Parser:
    def __init__(self, xml):
        self.xml = xml
        self.p = 0
        self.encoding = sys.getdefaultencoding()
        self.namespaces = {}

    def getnexttag(self):
        ptag = self.xml.find('<', self.p)
        if ptag < 0:
            return None, None, self.xml[self.p:].strip()
        data = self.xml[self.p:ptag].strip()
        self.p = ptag
        self.tagbegin = ptag
        p2 = self.xml.find('>', self.p+1)
        if p2 < 0:
            raise "Malformed XML - unclosed tag?"
        tag = self.xml[ptag+1:p2]
        self.p = p2+1
        self.tagend = p2+1
        ps = tag.find(' ')
        ### Change By LCJ @ 2017/9/7 from  [ if ps > 0: ]  ###
        ### for IOS Coda Webdav support ###
        if ps > 0 and tag[-1] != '/':
            tag, attrs = tag.split(' ', 1)
        else:
            attrs = ''
        return tag, attrs, data

    def builddict(self):
        """Builds a nested-dictionary-like structure from the xml. This method
        picks up tags on the main level and calls processTag() for nested tags."""
        d = Tag('<root>', '')
        while True:
            tag, attrs, data = self.getnexttag()
            if data != '': # data is actually that between the last tag and this one
                sys.stderr.write("Warning: inline data between tags?!\n")
            if not tag:
                break
            if tag[-1] == '/': # an 'empty' tag (e.g. <empty/>)
                d.addChild(Tag(tag[:-1], attrs, parser=self))
                continue
            elif tag[0] == '?': # special tag
                t = d.addChild(Tag(tag, attrs, parser=self))
                if tag == '?xml' and 'encoding' in t.attrs:
                    self.encoding = t.attrs['encoding']
            else:
                try:
                    self.processTag(d.addChild(Tag(tag, attrs, parser=self)))
                except:
                    sys.stderr.write("Error processing tag %s\n" % tag)
        d.encoding = self.encoding
        return d

    def processTag(self, dtag):
        """Process single tag's data"""
        until = '/'+dtag.rawname
        while True:
            tag, attrs, data = self.getnexttag()
            if data:
                dtag.data += data
            if tag == None:
                sys.stderr.write("Unterminated tag '"+dtag.rawname+"'?\n")
                break
            if tag == until:
                break
            if tag[-1] == '/':
                dtag.addChild(Tag(tag[:-1], attrs, parser=self))
                continue
            self.processTag(dtag.addChild(Tag(tag, attrs, parser=self)))

def splitattrs(att):
    """Extracts name="value" pairs from string; returns them as dictionary"""
    d = {}
    for m in re.findall('([a-zA-Z_][a-zA-Z_:0-9]*?)="(.+?)"', att):
        d[m[0]] = m[1]
    return d

def builddict(xml):
    """Wrapper function for straightforward parsing"""
    p = XMLDict_Parser(xml)
    return p.builddict()

#hold new directories in memory (not on disk) so they can be renamed
_temporary_directories = []
#similarly, for OSX 0-sized files
_dummy_files = []

  
class DAVRequestHandler(BaseHTTPRequestHandler):
    server_version = "Pythonista_dav"
    all_props = ['name', 'parentname', 'href', 'ishidden', 'isreadonly', 'getcontenttype',
                'contentclass', 'getcontentlanguage', 'creationdate', 'lastaccessed', 'getlastmodified',
                'getcontentlength', 'iscollection', 'isstructureddocument', 'defaultdocument',
                'displayname', 'isroot', 'resourcetype']
    basic_props = ['name', 'getcontenttype', 'getcontentlength', 'creationdate', 'iscollection']
    auth_file = False 
    auth_enable = False
    Auserlist = []

     # User Auth 
     # if success ,return False; 
     # Get WebDav User/Pass file : wdusers.conf
     # file formate:   user:pass\n user:pass\n
    def WebAuth(self):
        if self.server.auth_enable:
            if 'Authorization' in self.headers:
                try:
                    AuthInfo = self.headers['Authorization'][6:]
                except:
                    AuthInfo = ''
                if AuthInfo in self.server.userpwd:
                    return False    # Auth success
            self.send_response(401,'Authorization Required')
            self.send_header('WWW-Authenticate', 'Basic realm="WebDav Auth"')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            return True 
        else:
            return False 

    def do_OPTIONS(self):
        if self.WebAuth():
            return 
        self.send_response(200, DAVRequestHandler.server_version)
        #self.send_header('Allow', 'GET, HEAD, POST, PUT, DELETE, OPTIONS, PROPFIND, PROPPATCH, MKCOL, LOCK, UNLOCK, MOVE, COPY')
        self.send_header('Allow',
                         'GET, HEAD, POST, PUT, OPTIONS, PROPFIND, PROPPATCH, MKCOL')#, LOCK, UNLOCK')
        self.send_header('Content-length', '0')
        self.send_header('X-Server-Copyright', DAVRequestHandler.server_version)
        self.send_header('DAV', '1, 2')            #OSX Finder need Ver 2, if Ver 1 -- read only
        self.send_header('MS-Author-Via', 'DAV')
        self.end_headers()

    def do_DELETE(self):
        if self.WebAuth():
            return
        
        logger.debug('Attempting to delete %s' % self.path)
        
        self.send_error(403, 'Forbidden')
        self.send_header('Content-length', '0')
        self.end_headers()
        return
        
        # path = urllib.unquote(self.path)
        # if path == '':
        #     self.send_error(404, 'Object not found')
        #     self.send_header('Content-length', '0')
        #     self.end_headers()
        #     return
        # path = self.server.root.rootdir() + path
        # if os.path.isfile(path):
        #     os.remove(path)         #delete file
        # elif os.path.isdir(path):
        #     shutil.rmtree(path)     #delete dir
        # else:
        #     self.send_response(404,'Not Found')
        #     self.send_header('Content-length', '0')
        #     self.end_headers()
        #     return
        # self.send_response(204, 'No Content')
        # self.send_header('Content-length', '0')
        # self.end_headers()
        
    def do_MKCOL(self):
        if self.WebAuth():
            return 
        path = urllib.unquote(self.path)
        
        logger.debug('MKCOL: %s' % path)
        
        if path != '':
            path = self.server.root.rootdir().rstrip('/') + '/' + path.lstrip('/')
            if os.path.exists(path) == False:
                #os.mkdir(path)
                _temporary_directories.append(path)
                self.send_response(201, "Created")
                self.send_header('Content-length', '0')
                self.end_headers()
                return
            
        self.send_response(403, "OK")
        self.send_header('Content-length', '0')
        self.end_headers()        

    def do_MOVE(self):
        if self.WebAuth():
            return
        oldfile = self.server.root.rootdir().rstrip('/') + '/' + urllib.unquote(self.path).lstrip('/').rstrip('/')
        newfile = self.server.root.rootdir().rstrip('/') + '/' + urlparse.urlparse(urllib.unquote(self.headers['Destination'])).path.lstrip('/').rstrip('/')
        
        print('MOVE: %s -> %s' % (oldfile, newfile))
        #print _temporary_directories
        
        if oldfile in _temporary_directories:
            _temporary_directories.remove(oldfile)
            _temporary_directories.append(newfile)
        
            #if (os.path.isfile(oldfile)==True and os.path.isfile(newfile)==False):
            #    shutil.move(oldfile,newfile)
            #if (os.path.isdir(oldfile)==True and os.path.isdir(newfile)==False):
            #    os.rename(oldfile,newfile)
            self.send_response(201, "Created")
            self.send_header('Content-length', '0')
            self.end_headers()
            return
        else:
            self.send_error(403, 'Forbidden')
            self.send_header('Content-length', '0')
            self.end_headers()
            return


    def do_COPY(self):
        if self.WebAuth():
            return

        logger.debug('Attempting to copy %s' % self.path)

        self.send_error(403, 'Forbidden')
        self.send_header('Content-length', '0')
        self.end_headers()
        return
        # oldfile = self.server.root.rootdir() + urllib.unquote(self.path)
        # newfile = self.server.root.rootdir() + urlparse.urlparse(urllib.unquote(self.headers['Destination'])).path
        # if (os.path.isfile(oldfile)==True):        #  and os.path.isfile(newfile)==False):  copy can rewrite.
        #     shutil.copyfile(oldfile,newfile)
        # self.send_response(201, "Created")
        # self.send_header('Content-length', '0')
        # self.end_headers()

    def do_LOCK(self):
        if 'Content-length' in self.headers:
            req = self.rfile.read(int(self.headers['Content-length']))
        else:
            req = self.rfile.read()
        d = builddict(req)
        #logger.debug('do_LOCK: path = ' + self.path)
        #logger.debug('do_LOCK: headers = ' + str(self.headers))
        #logger.debug('do_LOCK: req = ' + req)
        #logger.debug('do_LOCK: d = ' + str(d))
        
        if req == '':
            #refreshing lock (windows)
            locktoken = self.headers['If']
            logger.debug(locktoken)
            lockid = locktoken[18:-2]
            logger.debug(lockid)
            
            clientid = 'foo'
        else:
            try:
                clientid = str(d['lockinfo']['owner']['href'])[7:]      # temp: need Change other method!!!
            except KeyError:
                pass
            clientid = 'foo'
            lockid = str(uuid.uuid1())
        
        retstr = '<?xml version="1.0" encoding="utf-8" ?>\n<D:prop xmlns:D="DAV:">\n<D:lockdiscovery>\n<D:activelock>\n<D:locktype><D:write/></D:locktype>\n<D:lockscope><D:exclusive/></D:lockscope>\n<D:depth>Infinity</D:depth>\n<D:owner>\n<D:href>'+clientid+'</D:href>\n</D:owner>\n<D:timeout>3600</D:timeout>\n<D:locktoken><D:href>opaquelocktoken:'+lockid+'</D:href></D:locktoken>\n</D:activelock>\n</D:lockdiscovery>\n</D:prop>\n'
        self.send_response(200,'OK')
        self.send_header("Content-type",'text/xml')
        self.send_header("charset",'"utf-8"')
        self.send_header("Lock-Token",'<opaquelocktoken:'+lockid+'>')
        self.send_header('Content-Length',len(retstr))
        self.end_headers()
        self.wfile.write(retstr)
        self.wfile.flush()

    def do_UNLOCK(self):
        # frome self.headers get Lock-Token:
        logger.debug('do_UNLOCK')
        self.send_response(204, 'No Content')        # unlock using 204 for sucess.
        self.send_header('Content-length', '0')
        self.end_headers()

    def do_PROPFIND(self):
        if self.WebAuth():
            return 
        depth = 'infinity'
        if 'Depth' in self.headers:
            depth = self.headers['Depth'].lower()
        if 'Content-length' in self.headers:
            req = self.rfile.read(int(self.headers['Content-length']))
        else:
            req = self.rfile.read()
        d = builddict(req)              # change all http.request to dict stru
        wished_all = False
        if len(d) == 0:
            wished_props = DAVRequestHandler.basic_props
        else:
            if 'allprop' in d['propfind']:
                wished_props = DAVRequestHandler.all_props
                wished_all = True
            else:
                wished_props = []
                for prop in d['propfind']['prop']:
                ### 2017/9/7 Edit By LCJ , Old is [ wished_props.append(prop)  ]
                ### for IOS Coda Webdav support ###
                     wished_props.append(prop.split(' ')[0])
        path, elem = self.path_elem()
        if not elem:
            if len(path) >= 1: # it's a non-existing file
                self.send_response(404, 'Not Found')
                self.send_header('Content-length', '0')
                self.end_headers()
                return
            else:
                elem = self.server.root     # fixup root lookups?
        if depth != '0' and not elem:   #or elem.type != Member.M_COLLECTION:
            self.send_response(406, 'This is not allowed')
            self.send_header('Content-length', '0')
            self.end_headers()
            return
        self.send_response(207, 'Multi-Status')          #Multi-Status
        self.send_header('Content-Type', 'text/xml')
        self.send_header("charset",'"utf-8"')        
        # !!! if need debug output xml info,please set last var from False to True. 
        w = BufWriter(self.wfile, True)
        w.write('<?xml version="1.0" encoding="utf-8" ?>\n')
        w.write('<D:multistatus xmlns:D="DAV:" xmlns:Z="urn:schemas-microsoft-com:">\n')

        def write_props_member(w, m):
            w.write('<D:response>\n<D:href>%s</D:href>\n<D:propstat>\n<D:prop>\n' % urllib.quote(m.virname))     #add urllib.quote for chinese
            props = m.getProperties()       # get the file or dir props 
            # For OSX Finder : getlastmodified,getcontentlength,resourceType
            if ('quota-available-bytes' in wished_props) or ('quota-used-bytes'in wished_props) or ('quota' in wished_props) or ('quotaused'in wished_props):
                sDisk = os.statvfs('/') #TODO - FIXME
                props['quota-used-bytes'] = (sDisk.f_blocks - sDisk.f_bavail) * sDisk.f_frsize
                props['quotaused'] = (sDisk.f_blocks - sDisk.f_bavail) * sDisk.f_frsize
                props['quota-available-bytes'] = sDisk.f_bavail * sDisk.f_frsize
                props['quota'] = sDisk.f_bavail * sDisk.f_frsize
                
                #print props
            for wp in wished_props:
                if props.has_key(wp) == False:
                    w.write('  <D:%s/>\n' % wp)
                else:
                    w.write('  <D:%s>%s</D:%s>\n' % (wp, str(props[wp]), wp))
            w.write('</D:prop>\n<D:status>HTTP/1.1 200 OK</D:status>\n</D:propstat>\n</D:response>\n')
            
            #print props

        write_props_member(w, elem)
        if depth == '1':
            for m in elem.getMembers():
                write_props_member(w,m)
        w.write('</D:multistatus>')
        self.send_header('Content-Length', str(w.getSize()))
        self.end_headers()
        w.flush()

    def do_PROPPATCH(self):
        if self.WebAuth():
            return
        
        if 'Content-length' in self.headers:
            req = self.rfile.read(int(self.headers['Content-length']))
        else:
            req = self.rfile.read()
    
        logger.debug('Attempting to proppatch %s' % self.path)
        logger.debug('do_PROPPATCH: req = ' + req)
    
        self.send_error(403, 'Forbidden')
        self.send_header('Content-length', '0')
        self.end_headers()
        return
    
        # path = urllib.unquote(self.path)
        # if path == '':
        #     self.send_error(404, 'Object not found')
        #     self.send_header('Content-length', '0')
        #     self.end_headers()
        #     return
        # path = self.server.root.rootdir() + path
        # if os.path.isfile(path):
        #     os.remove(path)         #delete file
        # elif os.path.isdir(path):
        #     shutil.rmtree(path)     #delete dir
        # else:
        #     self.send_response(404,'Not Found')
        #     self.send_header('Content-length', '0')
        #     self.end_headers()
        #     return
        # self.send_response(204, 'No Content')
        # self.send_header('Content-length', '0')
        # self.end_headers()

    def do_GET(self, onlyhead=False):
        if self.WebAuth():
            return 
        path, elem = self.path_elem()
        if not elem:
            self.send_error(404, 'Object not found')
            return
        try:
            props = elem.getProperties()
        except:
            self.send_response(500, "Error retrieving properties")
            self.end_headers()
            return
        # when the client had Range: bytes=3156-3681 
        bpoint = 0
        epoint = 0
        fullen = props['getcontentlength']
        logger.debug('do_GET: fullen = ' + str(fullen))
        if 'Range' in self.headers:
            stmp = self.headers['Range'][6:]
            stmp = stmp.split('-')
            try:
                bpoint = int(stmp[0])
            except:
                bpoint = 0
            try:
                epoint = int(stmp[1])
            except:
                epoint = fullen - 1
            if (epoint<=bpoint):
                bpoint = 0
                epoint = fullen - 1
            fullen = epoint - bpoint + 1
        if epoint>0:
            self.send_response(206, 'Partial Content')            
            self.send_header("Content-Range", " Bytes %s-%s/%s" % (bpoint, epoint, fullen))            
        else:
            self.send_response(200, 'OK')
        if elem.type == Member.M_MEMBER:
            self.send_header("Content-type", props['getcontenttype'])
            self.send_header("Last-modified", props['getlastmodified'])
            self.send_header("Content-length", fullen)
        else:
            try:
                ctype = props['getcontenttype']
            except:
                ctype = DirCollection.COLLECTION_MIME_TYPE
            self.send_header("Content-type", ctype)
        self.end_headers()
        if not onlyhead:
            if fullen >0 :      # all 0 size file don't need this 
                elem.sendData(self.wfile,bpoint,epoint)

    def do_HEAD(self):
        self.do_GET(True)           # HEAD should behave like GET, only without contents

    def do_PUT(self):
        if self.WebAuth():
            return 
        try:
            if 'Content-length' in self.headers:
                size = int(self.headers['Content-length'])
            elif 'Transfer-Encoding' in self.headers:
                if self.headers['Transfer-Encoding'].lower()=='chunked':
                    size = -2
            else:
                size = -1
            path, elem = self.path_elem_prev()
            ename = path[-1]
        except:
            logger.exception('Error parsing request on: %s' % self.path)
            self.send_response(400, 'Cannot parse request')
            self.send_header('Content-length', '0')
            self.end_headers()
            return
        # for OSX finder, it's first send a 0 byte file,and you need response a 201 code,and then osx send real file.
        # OSX finder don't using content-length.
        if ename == '.DS_Store':
            logger.debug('Trying to save .DS_Store')
            self.send_response(403, 'Forbidden')
            self.send_header('Content-length', '0')
            self.end_headers()
        elif ename.startswith('._'):
            #block OSX resource forks
            logger.debug('Trying to save resource fork')
            self.send_response(403, 'Forbidden')
            self.send_header('Content-length', '0')
            self.end_headers()
        else:
            try:
                #if not size == 0:
                elem.recvMember(self.rfile, ename, size, self)
            except:
                logger.exception('Error saving file: %s' % self.path)
                self.send_response(500, 'Cannot save file')
                self.send_header('Content-length', '0')
                self.end_headers()
                return
            if size == 0:
                logger.debug('File created %s' % path)
                self.send_response(201, 'Created')
            else:
                logger.debug('File saved  %s' % path)
                self.send_response(200, 'OK')
            self.send_header('Content-length', '0')
            self.end_headers()

    def split_path(self, path):
        """Splits path string in form '/dir1/dir2/file' into parts"""
        p = path.split('/')[1:]
        while p and p[-1] in ('','/'):
           p = p[:-1]
           if len(p) > 0:
              p[-1] += '/'
        return p

    def path_elem(self):
        """Returns split path (see split_path()) and Member object of the last element"""
        path = self.split_path(urllib.unquote(self.path))
        elem = self.server.root
        for e in path:
            elem = elem.findMember(e)
            if elem == None:
                break
        return (path, elem)

    def path_elem_prev(self):
        """Returns split path (see split_path()) and Member object of the next-to-last element"""
        path = self.split_path(urllib.unquote(self.path))
        elem = self.server.root
        for e in path[:-1]:
            elem = elem.findMember(e)
            if elem == None:
                break
        return (path, elem)
     
     # disable log info output to screen    
    def log_message(self,format,*args):
        if True:
            logger.info("%s - - [%s] %s\n" %
                        (self.client_address[0],
                         self.log_date_time_string(),
                         format % args))

class BufWriter:
    def __init__(self, w, debug=True):
        self.w = w
        self.buf = StringIO(u'')             
        self.debug = debug

    def write(self, s):
        if self.debug:
            sys.stderr.write(s)
        self.buf.write(s)
        #self.buf.write(unicode(s,'utf-8'))              # add unicode(s,'utf-8') for chinese code.
        
    def flush(self):
        self.w.write(self.buf.getvalue().encode('utf-8'))
        self.w.flush()

    def getSize(self):
        return len(self.buf.getvalue().encode('utf-8'))
       
class DAVServer(ThreadingMixIn, HTTPServer):
    def __init__(self, addr, handler, root, userpwd):
        HTTPServer.__init__(self, addr, handler)
        self.root = root
        self.userpwd = userpwd      # WebDav Auth user:passwd 
        if len(userpwd)>0:
            self.auth_enable = True
        else:
            self.auth_enable = False

    # disable the broken pipe error message 
    def finish_request(self,request,client_address):
        try:
            HTTPServer.finish_request(self, request, client_address)
        except socket.error as e:
            pass


    
def main():
    # WebDav TCP Port 
    srvport = 9090
    # Get local IP address
    import socket
    myaddr = get_localip()
    print('PYMECluster WebDav Server run at '+myaddr+':'+str(srvport)+'...')
    server_address = ('', srvport)
    # WebDav Auth User/Password file 
    # if not this file ,the auth function disable.
    # file format: user:passwd\n user:passwd\n
    # or you can change your auth mode and file save format 
    userpwd = []
    try:
        with open('wdusers.conf', 'r') as f:
            for uinfo in f.readlines():
                uinfo = uinfo.replace('\n','')
                if len(uinfo)>2:
                    userpwd.append(base64.b64encode(uinfo))
    except:
        userpwd.append(base64.b64encode('test:test'))
        pass
    # first is Server root dir, Second is virtual dir
    # **** Change first ./ to your dir , etc :/mnt/flash/public 
    root = DirCollection('/', '/')
    httpd = DAVServer(server_address, DAVRequestHandler, root, userpwd)
    
    #httpd.socket = ssl.wrap_socket (httpd.socket, certfile='./server.pem', server_side=True)
    
    httpd.serve_forever()       # todo: add some control over starting and stopping the server
    
if __name__ == '__main__':
    main()