# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import logging

from django.apps import AppConfig


class WeblateVpatchConfig(AppConfig):
    name = 'weblate_vpatch'

    def ready(self):
        try:
            from weblate.utils import docs
            def _mock(*args, **kwargs):
                return "https://docs.weblate.org/"
            docs.get_doc_url = _mock
        except Exception:
            logging.critical('Unable to apply monkey patch to documentation link')
