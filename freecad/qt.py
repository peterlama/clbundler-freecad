from clbundler.formula import *
from clbundler.exceptions import CommandNotFoundError

class qt(Formula):
    version = "4.8.6"
    source = {
        "type":"archive", 
        "url":"http://download.qt-project.org/official_releases"\
              "/qt/4.8/{0}/qt-everywhere-opensource-src-{0}.tar.gz".format(version)
    }
    supported = {"vc9":["x86", "x64"], "vc11":["x86", "x64"], "vc12":["x86", "x64"], "gcc":["x64"]}
    
    def __init__(self, context, options={}):
        super(qt, self).__init__(context, options)
        
        if vc_version(context.toolchain) > 10:
            self.patches.append("vc12")
        
    def build(self):
        if self.context.toolchain.startswith("vc"):
            mkspec = "win32-msvc" + vc_version_year(self.context.toolchain)
        elif self.context.os_name == "mac":
            mkspec = "macx-g++42"

        if self.context.toolchain.startswith("vc"):
            #change mkspec to use -EHa
            new_mkspec = ""
            with open("mkspecs/" + mkspec + "/qmake.conf") as f:
                for line in f:
                    new_mkspec += line.replace("-EHsc", "-EHa")
            with open("mkspecs/" + mkspec + "/qmake.conf", "w") as f:
                f.write(new_mkspec)
        
        configure_options = ["-opensource",
                             "-confirm-license",
                             "-platform", mkspec,
                             "-no-qt3support",
                             "-no-phonon",
                             "-no-multimedia",
                             "-nomake", "tests",
                             "-nomake", "examples",
                             "-nomake", "demos",
                             "-nomake", "docs"]
                             
        files = FileSet()
        plugins_exclude = ["plugins/bearer/*",
                           "plugins/designer/*",
                           "plugins/graphicssystems/*",
                           "plugins/qmltooling/*"]
        
        if self.context.toolchain.startswith("vc"):
            if self.variant == "release+debug":
                configure_options.append("-debug-and-release")
            else:
                configure_options.append("-" + self.variant)
            
            configure_options.append("-mp")
            configure_options.append("-no-vcproj")
            
            system.run_cmd("configure", configure_options)
            
            try:
                system.run_cmd("jom", ["-j4"])
            except CommandNotFoundError:
                system.run_cmd("nmake")
            
            #no install target -- copy files from source tree
            exclude = ["include/phonon",
                       "include/phonon_compat",
                       "include/Qt3Support",
                       "include/QtOpenVG",
                       "include/QtMultimedia",
                       "**/*.pri"]
            files.add(["include/*"], "include", exclude, category=Categories.build)
            
            exclude = ["src/imports/**",
                       "src/multimedia/**",
                       "src/openvg/**",
                       "src/phonon/**",
                       "src/qt3support/**",
                       "src/plugins/**"]
            files.add(["src/**/*.h"], "src", exclude, category=Categories.build)
            
            files.add(["tools/**/*.h"], "tools", category=Categories.build)
            files.add(["lib/*.lib"], "lib", category=Categories.build)
            files.add(["bin/*[!d]?.dll", "bin/*.exe"], "bin", category=Categories.run)
            files.add(["bin/*d?.dll"], "bin", category=Categories.run_dbg)
            
            files.add(["plugins/**/*[!d]?.dll"], "bin/QtPlugins", plugins_exclude, category=Categories.run)
            files.add(["plugins/**/*d?.dll"], "bin/QtPlugins", plugins_exclude, category=Categories.run)
        else:
            configure_options.append("-release")
            if self.context.os_name == "mac":
                configure_options.append("-no-framework")
            
            configure(self.context, configure_options)
            
            system.run_cmd("make", ["-j4"])
            system.run_cmd("make", ["install"])
        
            os.chdir(self.context.install_dir)
            files.add(["include/*"], "include", category=Categories.build)
            files.add(["lib/*.dylib"], "lib")
            files.add(["bin/*"], "bin")
            files.add(["plugins/*"], "lib/QtPlugins", plugins_exclude)
        
        with open("qt.conf", "w") as f:
            f.write("[Paths]\nPrefix = ..\nPlugins = bin/QtPlugins\n")
        
        files.add(["qt.conf"], "bin")
        
        return files
