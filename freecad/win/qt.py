from clbundler.formula import *
        
class qt(Formula):
    version = "4.8.6"
    source = {
        "type":"archive", 
        "url":"http://download.qt-project.org/official_releases"\
              "/qt/4.8/{0}/qt-everywhere-opensource-src-{0}.tar.gz".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc12":["x86", "x64"]}
    
    def __init__(self, context, options={}):
        super(qt, self).__init__(context, options)
        
        if context.toolchain == "vc12":
            self.patches.append("vc12")
        
    def build(self):
        #change mkspec to use -EHa
        new_mkspec = ""
        with open("mkspecs/win32-msvc2008/qmake.conf") as f:
            for line in f:
                new_mkspec += line.replace("-EHsc", "-EHa")
        with open("mkspecs/win32-msvc2008/qmake.conf", "w") as f:
            f.write(new_mkspec)
        
        if self.context.toolchain == "vc12":
            mkspec = "win32-msvc2012"
        else:
            mkspec = "win32-msvc2008"
        
        system.run_cmd("configure", ["-opensource", 
                                     "-confirm-license",
                                     "-platform", mkspec,
                                     "-debug-and-release", 
                                     "-mp", 
                                     "-no-qt3support",
                                     "-no-phonon", 
                                     "-no-multimedia", 
                                     "-no-declarative-debug",
                                     "-nomake", "tests",
                                     "-nomake", "examples",
                                     "-nomake", "demos",
                                     "-nomake", "docs",
                                     "-no-vcproj"])
        system.run_cmd("nmake")
        
        files = FileSet()
        
        exclude = ["include/phonon",
                   "include/phonon_compat",
                   "include/Qt3Support",
                   "include/QtOpenVG",
                   "include/QtMultimedia",
                   "**/*.pri"]
        files.add(["include/*"], "include", exclude, category="dev")
        
        exclude = ["src/imports/**",
                   "src/multimedia/**",
                   "src/openvg/**",
                   "src/phonon/**",
                   "src/qt3support/**",
                   "src/plugins/**"]
        files.add(["src/**/*.h"], "src", exclude, category="dev")
        
        files.add(["tools/**/*.h"], "tools", category="dev")
        files.add(["lib/*.lib"], "lib", category="dev")
        files.add(["bin/*[!d]?.dll", "bin/*.exe"], "bin", category="rel")
        files.add(["bin/*d?.dll"], "bin", category="dbg")
        
        exclude = ["plugins/bearer/*",
                   "plugins/designer/*",
                   "plugins/graphicssystems/*",
                   "plugins/qmltooling/*"]
        files.add(["plugins/**/*[!d]?.dll"], "bin/QtPlugins", exclude, category="rel")
        
        with open("qt.conf", "w") as f:
            f.write("[Paths]\nPrefix = ..\nPlugins = bin/QtPlugins\n")
        
        files.add(["qt.conf"], "bin")
        
        return files
