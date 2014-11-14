from clbundler.formula import *
        
class freeimage(Formula):
    version = "3.15.4"
    source = {
        "type":"archive", 
        "url":"http://downloads.sourceforge.net/freeimage/FreeImage3154.zip"
    }
    supported = {"vc9":["x86", "x64"], "vc11":["x86", "x64"], "vc12":["x86", "x64"], "gcc":["x64"]}
    
    def __init__(self, context, options={}):
        super(freeimage, self).__init__(context, options)
        
        self.patches = ["cmake", "inc_algorithm"]
        
    def build(self):
        cmake(self.context, {"BUILD_SHARED_LIBS":"ON", "CMAKE_BUILD_TYPE":"Release"})
        
        if self.context.toolchain.startswith("vc"):
            if "debug" in self.variant:
                vcbuild(self.context, "cmake_build\\freeimage.sln", "Debug")
            if "release" in self.variant:
                vcbuild(self.context, "cmake_build\\freeimage.sln", "Release")
            
            vcproj = "cmake_build\\INSTALL" + vcproj_ext(self.context.toolchain)
            if "debug" in self.variant:
                vcbuild(self.context, vcproj, "Debug")
            if "release" in self.variant:
                vcbuild(self.context, vcproj, "Release")
        else:
            os.chdir("cmake_build")
            system.run_cmd("make", ["-j4"])
            system.run_cmd("make", ["install/fast"])
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category=Categories.build)
        
        if self.context.toolchain.startswith("vc"):
            files.add(["lib/*"], "lib", category=Categories.build)
            files.add(["bin/*[!d].dll"], "bin", category=Categories.run)
            files.add(["bin/*d.dll"], "bin", category=Categories.run_dbg)
        else:
            if self.context.os_name == "mac":
                files.add(["lib/*.dylib"], "lib", category=Categories.run)
            else:
                files.add(["lib/*.so"], "lib", category=Categories.run)
        
        return files

