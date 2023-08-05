import logging
import importlib
from scrapy.dupefilters import BaseDupeFilter
from scrapy.utils.request import request_fingerprint
from .freedb import FreedbClient, DocumentDotExist


logger = logging.getLogger(__name__)


def null_id_mapper(request):
    return None


class FreedbDupefilter(BaseDupeFilter):
    '''SpiderStateService request duplicates filter.
    '''
    logger = logger
    visit_cache = None

    def __init__(self, db_name, col_name, client: FreedbClient, settings, debug=False, stats=None):
        self.db_name = db_name
        self.col_name = col_name
        self.client = client
        self.debug = debug
        self.settings = settings
        self.logdupes = True
        self.stats = stats
        self.visit_cache = set()
        
        free_id_mapper_setting = settings.get('FREEDB_ID_MAPPER')
        if free_id_mapper_setting:
            id_mapper_module_name, id_mapper_func_name = free_id_mapper_setting.split(':')
            id_mapper_module = importlib.import_module(id_mapper_module_name)
            self.id_mapper = getattr(id_mapper_module, id_mapper_func_name)
        else:
            self.id_mapper = null_id_mapper

    @classmethod
    def from_settings(cls, settings):
        '''
        This method is for older scrapy version which does not support
        a spider context when building a dupefilter instance. The spider name
        will be assumed as 'spider'
        :param settings:
        :return:
        '''
        base_url = settings.get("FREEDB_BASEURL")
        token = settings.get('FREEDB_TOKEN')
        db_name = settings.get('FREEDB_DBNAME')
        col_name = settings.get('FREEDB_COLNAME')
        client = FreedbClient(base_url, token)
        return cls(db_name, col_name, client, settings)

    @classmethod
    def from_crawler(cls, crawler):
        logger.debug('FreedbDupefilter from_crawler')
        return cls.from_spider(crawler.spider)

    @classmethod
    def from_spider(cls, spider):
        settings = spider.settings
        return cls.from_settings(settings)

    def request_seen(self, request):
        """Returns True if request was already seen.
        Parameters
        ----------
        request : scrapy.http.Request
        Returns
        -------
        bool
        """
        fp = self.request_fingerprint(request)
        if fp in self.visit_cache:
            return True
        
        try:
            doc_id = self.get_doc_id(request)
            if doc_id is None:
                raise DocumentDotExist()
            doc = self.client.get_document(self.db_name, self.col_name, doc_id)
            return True
        except DocumentDotExist:
            return False
        finally:
            self.visit_cache.add(fp)

    def get_doc_id(self, request):
        if self.id_mapper:
            id_ = self.id_mapper(request)
            logger.debug(f'id for request {request.method} {request.url} is {id_}')
            return id_


    def request_fingerprint(self, request):
        """Returns a fingerprint for a given request.
        Parameters
        ----------
        request : scrapy.http.Request
        Returns
        -------
        str
        """
        return request_fingerprint(request)

    def open(self):
        #self.client.create
        pass

    def close(self, reason=''):
        pass

    def clear(self):
        pass

    def log(self, request, spider):
        if self.debug:
            msg = "Filtered duplicate request: %(request)s"
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
        elif self.logdupes:
            msg = ("Filtered duplicate request: %(request)s"
                   " - no more duplicates will be shown"
                   " (see DUPEFILTER_DEBUG to show all duplicates)")
            self.logger.debug(msg, {'request': request}, extra={'spider': spider})
            self.logdupes = False

        spider.crawler.stats.inc_value('dupefilter/filtered', spider=spider)
