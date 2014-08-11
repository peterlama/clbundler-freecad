from clbundler.formula import *
        
class sqlite3(Formula):
    version = "3.8.5"
    source = {
        "type":"archive", 
        "url":"http://www.sqlite.org/2014/sqlite-amalgamation-3080500.zip"
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(sqlite3, self).__init__(context, options)
       
    def build(self):
        system.run_cmd("cl", ["/c", "/O2", "/Oi", "/MD", "sqlite3.c"])
        system.run_cmd("lib", ["sqlite3.obj"])
        
        files = FileSet()
        files.add(["sqlite3.h", "sqlite3ext.h"], "include", category=Categories.build)
        files.add(["sqlite3.lib"], "lib", category=Categories.build)
        
        return files
