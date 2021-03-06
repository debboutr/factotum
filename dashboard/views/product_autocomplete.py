from dal import autocomplete
from dashboard.models import Product, ProductCategory
from django.db.models import Q


class PUCAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated():
            return ProductCategory.objects.none()
        qs = ProductCategory.objects.all()
        if self.q:
            qs = qs.filter(Q(gen_cat__icontains=self.q) | Q(prod_fam__icontains=self.q) | Q(prod_type__icontains=self.q)) 

        return qs
