# AX3 mixins

Mixins for use into the AX3 tech stack.


## AjaxRequestMixin

Useful when you need a view only for AJAX queries:

```
from ax3_mixins import mixins

class AjaxView(mixins.AjaxRequestMixin, View):
    def post(self, request, *args, **kwargs):
        # Only get here if was called by an AJAX request.
        ...
```


## SlugIdMixin

Allows a view to support smart urls with slug and ids.

At urls use:
```
path('leer/<slug:slugid>/', views.PageDetailView.as_view(), name='page_detail'),
```

At views use:
```
from ax3_mixins import mixins

class PageDetailView(mixins.SlugIdMixin):
    template_name = 'app/page_detail.html'
    queryset = Page.objects.filter(is_active=True)
```

At models use:
```
def get_absolute_url(self):
    return reverse('page_detail', args=[f'{self.slug}-{self.id}'])
```

This mixin will get the object using the id and redirect to the current object
slug if is different from the URL. It will add the `object` to the template context.

