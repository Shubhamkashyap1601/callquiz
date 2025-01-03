from django.contrib import admin
from .models import Quiz, Question, Option, Leaderboard

admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)

@admin.register(Leaderboard)
class LeaderboardAdmin(admin.ModelAdmin):
    list_display = ('user_name', 'quiz', 'score')  # Customize as needed
    search_fields = ('user_name', 'quiz__title')  # Enable search