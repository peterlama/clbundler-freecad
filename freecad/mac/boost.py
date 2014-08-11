from clbundler.formula import *
        
class boost(Formula):
    version = "1.55"
    source = {
        "type":"archive", 
        "url":"http://sourceforge.net/projects/boost/files/boost/1.55.0"
              "/boost_1_55_0.zip"
    }
    supported = {"gcc":["x64"]}
    
    def __init__(self, context, options={}):
        super(boost, self).__init__(context, options)
        
    def build(self):
        system.run_cmd("bootstrap.sh")
        
        system.run_cmd("b2", ["link=shared",
                              "variant=release",
                              "--with-filesystem",
                              "--with-program_options",
                              "--with-regex",
                              "--with-signals", 
                              "--with-system",
                              "--with-thread"])
        
        files = FileSet()
        files.add(["boost"], "include", category=Categories.build)
        files.add(["stage/lib/*.dylib"], "lib", category=Categories.run)
        
        return files
