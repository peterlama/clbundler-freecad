from clbundler.formula import *
        
class qhull(Formula):
    version = "2012.1"
    source = {
        "type":"archive", 
        "url":"http://www.qhull.org/download/qhull-{0}-src.tgz".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc11":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(qhull, self).__init__(context, options)
       
    def build(self):
        cmake(self.context, {"CMAKE_DEBUG_POSTFIX":"d"})
        
        if "debug" in self.variant:
            vcbuild(self.context, "cmake_build\\qhull.sln", "Debug")
        if "release" in self.variant:
            vcbuild(self.context, "cmake_build\\qhull.sln", "Release")
        
        vcproj = "cmake_build\\INSTALL" + vcproj_ext(self.context.toolchain)
        if "debug" in self.variant:
            vcbuild(self.context, vcproj, "Debug")
        if "release" in self.variant:
            vcbuild(self.context, vcproj, "Release")
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category=Categories.build)
        files.add(["lib/qhullstatic*.lib"], "lib", category=Categories.build)
        
        return files
