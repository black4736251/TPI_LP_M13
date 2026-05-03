from PySide6.QtCore import QUrl
from PySide6.QtMultimedia import QAudioOutput, QMediaPlayer


class SoundManager:
    _instance: "SoundManager | None" = None

    # Make basedpyright happy
    player: QMediaPlayer | None
    audio_out: QAudioOutput | None

    def __init__(self):
        # Make basedpyright happy
        if not hasattr(self, "player"):
            self.player = None

        if not hasattr(self, "audio_out"):
            self.audio_out = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            # Real initialization
            cls._instance.player = QMediaPlayer()
            cls._instance.audio_out = QAudioOutput()

            cls._instance.player.setAudioOutput(cls._instance.audio_out)
            cls._instance.audio_out.setVolume(1)

        return cls._instance

    def play(self, path: str):
        if self.player is None:
            return

        self.player.setSource(QUrl.fromLocalFile(path))
        self.player.play()