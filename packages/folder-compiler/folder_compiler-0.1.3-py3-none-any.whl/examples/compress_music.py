"""
This file shows how I compress my high quality flac music to compressed files for my
phone.
At the same time it copies cover images and already compressed music.
"""
import os
import subprocess
import shlex
import folder_compiler
from folder_compiler.processors import Processor, ProcessorUtils, FileCopyProcessor, \
    DevNullProcessor


class FlacToOggProcessor(Processor):
    """
    This processor compresses flac files to ogg.
    """

    def process_file(self, source: str, utils: ProcessorUtils):
        target = os.path.splitext(source)[0] + ".ogg"  # change file extension of target
        utils.add_file(target)  # do not delete this file!
        if utils.is_target_outdated(source=source, target=target):
            source_file = utils.get_full_source_path(source)  # get full path
            target_file = utils.get_full_target_path(target)  # get full path
            # oggenc command
            cmd = " ".join(
                ["oggenc", "-q", "8", shlex.quote(source_file), "-o",
                 shlex.quote(target_file)])
            # execute
            print(cmd)
            subprocess.run(cmd, check=True, shell=True)
        return True  # The file has been processed


# The processors are applied for each file in this order
# until the first one accepts the file.
# For example, the DevNullProcessor will accept all hidden files and block them
# from being forwarded to the later processors.
processors = [
    FileCopyProcessor().add_include(".*/\.conver\.jpg"),  # copy hidden cover images
    DevNullProcessor().include_hidden_files_and_folders(),  # ignore other hidden files
    FlacToOggProcessor().add_include(".*\.flac"),  # compress flacs
    FileCopyProcessor().add_include(".*\.mp3").add_include(".*\.ogg"),  # Copy mp3 and ogg
    FileCopyProcessor().add_include(".*\.jpg").add_include(".*\.png")  # copy cover images
]

# Paths: From where should the music compiled to where
uncompressed_music_source = "/home/krupke/Music"
compressed_music_target = "/path/to/my/phones/sd"
compressed_music_target = "/run/user/1000/gvfs/mtp:host=HMD_Global_Nokia_7_plus_B2NGAA8841802054/Samsung SD card/Music"

folder_compiler.FolderCompiler(input=uncompressed_music_source,
                               output=compressed_music_target).compile(processors).remove_orphaned_files()
