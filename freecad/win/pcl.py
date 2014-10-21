from clbundler.formula import *
        
class pcl(Formula):
    version = "1.7.2"
    source = {
        "type":"archive", 
        "url":"https://github.com/PointCloudLibrary/pcl/archive/pcl-{0}.tar.gz".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(pcl, self).__init__(context, options)
        
        self.add_deps("boost", "flann", "qhull")
        
        if self.context.toolchain = "vc9":
            self.patches = ["vc9_fixes"]
        
    def build(self):
        cmake(self.context, {"PCL_BUILD_WITH_BOOST_DYNAMIC_LINKING_WIN32":"ON"})
        
        if "debug" in self.variant:
            vcbuild(self.context, "cmake_build\\pcl.sln", "Debug")
        if "release" in self.variant:
            vcbuild(self.context, "cmake_build\\pcl.sln", "Release")
        
        vcproj = "cmake_build\\INSTALL" + vcproj_ext(vc_version(self.context.toolchain))
        if "debug" in self.variant:
            vcbuild(self.context, vcproj, "Debug")
        if "release" in self.variant:
            vcbuild(self.context, vcproj, "Release")
        
        os.chdir(self.context.install_dir)
        
        files = FileSet()
        files.add(["include/*"], "include", category=Categories.build)
        files.add(["lib/*.lib"], "lib", category=Categories.build)       
        files.add(["bin/*[!d].dll"], "bin", category=Categories.run)
        files.add(["bin/*d.dll"], "bin", category=Categories.run_dbg)
        
        return files
