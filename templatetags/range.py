from django import template

register = template.Library()

@register.filter()
def ranges(count=21):
    return range(1, count)

# 세팅에서 뭘 추가해야하는데 모르겠음 !