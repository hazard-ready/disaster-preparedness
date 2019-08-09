from embed_video.backends import YoutubeBackend

class LazyLoadBackend(YoutubeBackend):
  template_name = 'embed_video.html'

