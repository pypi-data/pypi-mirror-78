import re

from django.http import HttpResponseBadRequest, Http404
from django.shortcuts import redirect
from django.views.generic import TemplateView


class AjaxRequestMixin:
    def dispatch(self, request, *args, **kwargs):
        if request.META.get('HTTP_X_REQUESTED_WITH') != 'XMLHttpRequest':
            return HttpResponseBadRequest()

        return super().dispatch(request, *args, **kwargs)


class SlugIdMixin(TemplateView):
    REGEX = re.compile(r'([\w-]+)?-([\d]+)')

    def dispatch(self, request, *args, **kwargs):
        match = self.REGEX.match(self.kwargs['slugid'])
        if match:
            slug, pk = match.groups()
            self.object = self.queryset.filter(pk=pk).first()
            if self.object:
                if self.object.slug == slug:
                    return super().dispatch(request, *args, **kwargs)

                return redirect(self.object)

        raise Http404('slug and id not exist')

    def get_context_data(self, **kwargs):
        context = {'object': self.object}

        return super().get_context_data(**context)
