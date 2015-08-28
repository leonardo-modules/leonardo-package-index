from django import template



register = template.Library()


class ParticipantURLNode(template.Node):

    def __init__(self, repo, participant):
        self.repo = template.Variable(repo)
        self.participant = template.Variable(participant)

    def render(self, context):
        repo = self.repo.resolve(context)
        participant = self.participant.resolve(context)
        if repo.user_url:
            user_url = repo.user_url % participant
        else:
            user_url = '%s/%s' % (repo.url, participant)
        return user_url


@register.tag
def participant_url(parser, token):
    try:
        tag_name, repo, participant = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires exactly two arguments" % token.contents.split()[0]
    return ParticipantURLNode(repo, participant)


@register.filter
def commits_over_52(package):
    return package.commits_over_52()
