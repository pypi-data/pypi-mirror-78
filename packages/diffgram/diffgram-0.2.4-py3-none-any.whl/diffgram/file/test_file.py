import random

from diffgram import Project
from diffgram import File


project = Project(
		  debug = True,
          project_string_id = "twilightgem",
          client_id = "LIVE__1ewq9uge3fxammxonajr",
          client_secret = "j6htpnka3x4x3uvjfmbj0lli6hqsomyfzxer04ghut1xnv9r6924egxjwdnb") 

id = 787

file = project.file.get_by_id(id = id)

assert file.id == id

print(file)
print(file.id)