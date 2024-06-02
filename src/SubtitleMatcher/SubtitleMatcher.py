import re
import shutil
from enum import Enum
from pathlib import Path


class SubtitleFormat(Enum):
    ASS = ".ass"
    SRT = ".srt"


class Language(Enum):
    EN = 1
    zhCN = 2
    zhTW = 4


class subtitle:
    def __init__(self, subtitle_path):
        self.path: Path = Path(subtitle_path)
        self.name = self.path.stem
        self.format = self.path.suffix[1:]
        self.language_set = self.extract_language_set()

    def extract_language_set(self):
        segments = self.name.split('.')
        lang_set = 0
        if len(segments) > 1:
            lang_set_str = segments[-2]
            lang_set_group = lang_set_str.split('&')
            for part in lang_set_group:
                match part:
                    case '繁体':
                        lang_set |= Language.zhTW
                    case '简体':
                        lang_set |= Language.zhCN
                    case '英文':
                        lang_set |= Language.EN
            return lang_set


class video:
    def __init__(self, video_path):
        self.path: Path = Path(video_path)
        self.name = self.path.stem
        self.format = self.path.suffix[1:]
        self.subtitles: list[subtitle] = []
        self.episode_identifier = self.extract_episode_identifier()

    def add_subtitle(self, subtitle_dir):
        for subtitle_path in subtitle_dir.glob(f"{self.episode_identifier}*"):
            self.subtitles.append(subtitle(subtitle_path))

    def extract_episode_identifier(self):
        filename = self.path.stem
        match = re.search(r"(S\d{2}E\d{2})", filename)
        return match.group(1) if match else None

