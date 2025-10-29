from django.urls import path
from .views import GoodListView, GoodDetailView, GetListViewFromBrand,GetListViewFromCategory


urlpatterns = [
    path('list', GoodListView.as_view(), name='good-list'),
    path('list/<int:id>/', GoodDetailView.as_view(), name='good-detail'),  # <int:id> captures the product ID
    path('<int:category_id>/getByCategoryId', GetListViewFromCategory.as_view(), name='good-by-category'),
    path('<int:brand_id>/getByBrandId', GetListViewFromBrand.as_view(), name='good-by-brand')
]