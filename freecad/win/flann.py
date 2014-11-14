from clbundler.formula import *
        
class flann(Formula):
    version = "1.8.4"
    source = {
        "type":"git", 
        "url":"https://github.com/mariusmuja/flann.git",
        "revision":"04b4a56533"
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(flann, self).__init__(context, options)
        
        self.patches = ["msvc_int64"]
        
    def build(self):
        cmake(self.context, {"BUILD_TESTS":"OFF", 
                             "BUILD_EXAMPLES":"OFF", 
                             "BUILD_C_BINDINGS":"OFF",
                             "CMAKE_DEBUG_POSTFIX":"d"})
        
        if "debug" in self.variant:
            vcbuild(self.context, "cmake_build\\flann.sln", "Debug")
        if "release" in self.variant:
            vcbuild(self.context, "cmake_build\\flann.sln", "Release")
        
        vcproj = "cmake_build\\INSTALL" + vcproj_ext(self.context.toolchain)
        if "debug" in self.variant:
            vcbuild(self.context, vcproj, "Debug")
        if "release" in self.variant:
            vcbuild(self.context, vcproj, "Release")
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category=Categories.build)
        files.add(["lib/*.lib"], "lib", category=Categories.build)
        
        return files
