from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django import template
from adsense.adsense import adsense

register = template.Library()

fail_silently = getattr(settings, "ADSENSE_DEBUG", None) or settings.DEBUG
default_publisher_id = getattr(settings, "ADSENSE_PUBLISHER_ID", None)
# params = getattr(settings, "ADSENSE_DEFAULTS", None)

class MobileAdSenseNode(template.Node):
    def __init__(self, publisher_id):
        self.publisher_id = template.Variable(publisher_id)

    def render(self, context):
        assert "request" in context, "AdSense tag requires request in context."

        if self.publisher_id is not None:
            publisher_id = self.publisher_id.resolve(context)
        else:
            publisher_id = default_publisher_id
        if publisher_id is None:
            raise ImproperlyConfigured("No AdSense publisher id given.")
                
        return adsense(context["request"], publisher_id, 
                       fail_silently=fail_silently)

@register.tag
def mobileadsense(parser, token):
    try:
        tag_name, publisher_id = token.contents.split(None, 1)
    except ValueError:
        publisher_id = None

    return MobileAdSenseNode(publisher_id)
