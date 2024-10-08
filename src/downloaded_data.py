from typing import List

class DownloadedData:
    def __init__(self, name=None, id=None, type=None, filename=None, base_model=None, url=None, clip_skip=0, trigger_words=None, images=None):
        self.name = name
        self.id = id
        self.type = type
        self.filename = filename
        self.base_model = base_model
        self.url = url
        self.clip_skip = clip_skip
        self.trigger_words = trigger_words or []
        self.images = images or []
        self.custom_notes = None

    def set_name(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name

    def set_filename(self, filename: str):
        self.filename = filename

    def get_filename(self) -> str:
        return self.filename

    def set_url(self, url: str):
        self.url = url

    def get_url(self) -> str:
        return self.url

    def set_clip_skip(self, clip_skip: int):
        self.clip_skip = clip_skip

    def get_clip_skip(self) -> int:
        return self.clip_skip

    def set_trigger_words(self, trigger_words: List[str]):
        self.trigger_words = trigger_words

    def get_trigger_words(self) -> List[str]:
        return self.trigger_words

    def set_images(self, images: List[str]):
        self.images = images

    def get_images(self) -> List[str]:
        return self.images

    def set_base_model(self, base_model: str):
        self.base_model = base_model

    def get_base_model(self) -> str:
        return self.base_model

    def set_id(self, id: str):
        self.id = id

    def get_id(self) -> str:
        return self.id

    def set_custom_notes(self, custom_notes: str):
        self.custom_notes = custom_notes

    def get_custom_notes(self) -> str:
        return self.custom_notes
