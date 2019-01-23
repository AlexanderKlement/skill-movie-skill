from mycroft import MycroftSkill, intent_file_handler


class SkillMovie(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('movie.skill.intent')
    def handle_movie_skill(self, message):
        self.speak_dialog('movie.skill')


def create_skill():
    return SkillMovie()

