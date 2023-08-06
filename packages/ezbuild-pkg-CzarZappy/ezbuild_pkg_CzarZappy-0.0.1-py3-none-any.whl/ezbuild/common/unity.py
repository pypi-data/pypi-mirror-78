import sys

from ezbuild.common import bash, zlog
from pathlib import Path


def get_unity_build_ext(build_target):
    switcher = {
        'OSXUniversal': 'app',
        'Win64': 'exe',
        'Win': 'exe',
        'Linux64': 'linux64'
    }

    return switcher.get(build_target)


class Unity:

    def __init__(self, path, output_dir):
        self.UNITY_PATH = str(path)
        self.output_dir = output_dir

    def run_unity_build(self, build_target: str, output: str):
        args = ["time", self.UNITY_PATH, "-quit -batchmode", "-logFile", "{}/stdout.log".format(self.output_dir),
                "-buildTarget",
                build_target,
                output]
        out = bash.run(args)
        print(out)

    def run_unity_osx_build(self, output_file_path):
        args = ["time", self.UNITY_PATH, "-quit -batchmode", "-buildOSXUniversalPlayer", output_file_path + ".app"]
        out = bash.run(args)
        print(out)

    def run_unity_linux64_build(self, output_file_path):
        args = ["time", self.UNITY_PATH, "-quit -batchmode", "-buildLinux64Player", output_file_path + ".linux64"]
        out = bash.run(args)
        print(out)

    def run_unity_win64_build(self, output_file_path):
        args = ["time", self.UNITY_PATH, "-quit -batchmode", "-buildWindows64Player", output_file_path + ".exe"]
        out = bash.run(args)
        print(out)

    def run_unity_webgl_build(self, output):
        args = ["time", self.UNITY_PATH, "-quit -batchmode", "-logFile", "{}/stdout.log".format(self.output_dir),
                "-executeMethod WebGLBuilder.build", "-zarg:output", output]
        out = bash.run(args)
        print(out)

    def run_build_target(self, project_name: str, build_target: str, output_dir: str):
        switch = {
            'OSXUniversal': self.run_unity_osx_build,
            'Win64': self.run_unity_win64_build,
            'WebGL': self.run_unity_webgl_build,
            'Linux64': self.run_unity_linux64_build,
        }

        filename_ext = get_unity_build_ext(build_target)

        if filename_ext is None:
            print("unknown file extension for build target", filename_ext, build_target)

        # output_path = '{}/{}.{}'.format(output_dir, PROJECT_NAME, filename_ext)
        output_file_path = '{}/{}'.format(output_dir, project_name)  # build_config["project_name"])
        print("output_path:", output_file_path)

        result = switch.get(build_target)

        if result is None:
            # mkdir(output_path)
            Unity.run_unity_build(build_target, output_file_path)
        else:
            result(output_file_path)


def get_unity_path(unity_version):
    windows_path = r'D:\Program Files\Unity Hub\Editors\{}\Editor'.format(unity_version)

    mac_osx_path = '/Applications/Unity/Hub/Editor/{}/Unity.app/Contents/MacOS/Unity'.format(unity_version)

    platform = sys.platform

    switcher={
        'darwin': mac_osx_path,
        'win32': windows_path
    }

    path = switcher.get(platform, None)

    if path is None:
        zlog.warn('Unknown platform:', platform)
        return

    return Path(path)
