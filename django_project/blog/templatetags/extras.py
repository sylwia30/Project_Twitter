from django import template

register = template.Library()


@register.filter()
def order_and_get_three(post):
    comments = post.comment_set.all().order_by("-date_comment")
    result = []
    for comment in comments:
        result.append(comment)
        if len(result) > 2:
            break
    return result