from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from datetime import timedelta

from danceschool.core.mixins import PluginTemplateMixin

from .models import NewsItem, LatestNewsPluginModel


class LatestNewsItemPlugin(PluginTemplateMixin, CMSPluginBase):
    model = LatestNewsPluginModel
    name = _('Show Latest News Items')
    template_choices = [('news/latest_news.html',_('Default Template')),]
    render_template = 'news/latest_news.html'
    cache = True
    module = _('News')

    def render(self, context, instance, placeholder):
        context = super(LatestNewsItemPlugin,self).render(context, instance, placeholder)

        listing = NewsItem.objects.all()

        if instance.daysBefore:
            listing = listing.filter(publicationDate__gte=timezone.now() - timedelta(days=instance.daysBefores))
        if instance.alertOnly:
            listing = listing.filter(alert=True)
        if instance.ignorePins:
            listing = listing.order_by('-publicationDate')

        context.update({
            'newsitem_list': listing[:instance.maxItems]
        })
        return context


plugin_pool.register_plugin(LatestNewsItemPlugin)
