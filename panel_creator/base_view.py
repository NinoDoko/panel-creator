from django.views.generic import TemplateView
from django.utils.safestring import mark_safe
from django.shortcuts import redirect
import openstack_dashboard.salt_utils.salt_utils as salt_utils
import openstack_dashboard.salt_utils.utils as salt_api
import json

#Actions#

class IndexView(TemplateView):
    template_name = '#Template_Location#/index.html'

    def get_tables(self):
        tables = #Tables_Dictionary#
        for table in tables :
            rows = []
            table['rows'] = rows
        return tables

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        table = dict()
        context['tables'] = self.get_tables()
        context['panel_header'] = '#Panel_Header#'
        context['panel_title'] = '#Panel_Title#'
        return context
