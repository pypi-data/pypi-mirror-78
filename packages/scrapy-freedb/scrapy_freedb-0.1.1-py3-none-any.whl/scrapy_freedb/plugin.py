import json
import logging
from .base import SpiderPlugin, BooleanPluginParameter, StringPluginParameter
from scrapy.settings import Settings


logger = logging.getLogger(__name__)


class Plugin(SpiderPlugin):
    parameters = [
        BooleanPluginParameter('ENABLED', required=True, default_value=False),
        StringPluginParameter('freedb_token'),
        StringPluginParameter('freedb_baseurl'),
        StringPluginParameter('freedb_dbname'),
        StringPluginParameter('freedb_colname'),
    ]
    plugin_name = 'freedb_plugin'
    settings = None

    def perform(self, settings: Settings, plugin_settings):
        if not get_bool(plugin_settings.get('ENABLED', 'false')):
            return

        logger.info('scrapy-freedb plugin enabled.')

        item_pipelines = settings.getdict('ITEM_PIPELINES')
        item_pipelines['scrapy_freedb.middleware.pipeline.FreedbSaveItemPipeline'] = 100
        settings.set('ITEM_PIPELINES', item_pipelines)
        settings.set('DUPEFILTER_CLASS', 'scrapy_freedb.middleware.dupefilter.FreedbDupefilter')
        settings.set('FREEDB_BASEURL', plugin_settings.get('FREEDB_BASEURL'))
        settings.set('FREEDB_TOKEN', plugin_settings.get('FREEDB_TOKEN'))
        settings.set('FREEDB_DBNAME', plugin_settings.get('FREEDB_DBNAME'))
        settings.set('FREEDB_COLNAME', plugin_settings.get('FREEDB_COLNAME'))
        settings.set('FREEDB_ID_MAPPER', plugin_settings.get('FREEDB_ID_MAPPER'))
        settings.set('FREEDB_ID_FIELD', plugin_settings.get('FREEDB_ID_FIELD'))

    def apply(self, settings, **kwargs):
        plugin_settings = self.settings or {}
        self.perform(settings, plugin_settings)


def get_bool(value):
    try:
        return bool(int(value))
    except ValueError:
        if value in ("True", "true"):
            return True
        if value in ("False", "false"):
            return False
        raise ValueError("Supported values for boolean settings "
                         "are 0/1, True/False, '0'/'1', "
                         "'True'/'False' and 'true'/'false'")
