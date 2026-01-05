from django.contrib import admin
from .models import Field, Subfield, User, Problem, Project, Post, CollaborationRequest


admin.site.register(Field)
admin.site.register(Subfield)
admin.site.register(User)
admin.site.register(Problem)
admin.site.register(Project)
admin.site.register(Post)
admin.site.register(CollaborationRequest)