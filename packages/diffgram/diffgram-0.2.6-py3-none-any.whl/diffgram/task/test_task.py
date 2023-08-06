import random

from diffgram import Project
from diffgram import File


project = Project(
		  debug = True,
          project_string_id = "twilightgem",
          client_id = "LIVE__1ewq9uge3fxammxonajr",
          client_secret = "j6htpnka3x4x3uvjfmbj0lli6hqsomyfzxer04ghut1xnv9r6924egxjwdnb") 

id = 2

task = project.task.get_by_id(id = id)

print(task)

assert task.id == id

print(task.file)
print(task.file.id)
