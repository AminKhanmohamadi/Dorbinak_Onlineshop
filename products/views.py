from typing import Any
from django.db.models import Case, When, DecimalField
from django.db.models.query import QuerySet
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView ,View
from django.shortcuts import render
from products.models import Product, Category, SubCategory


# Create your views here.
# def search_product(request):
#     if request.method == 'GET':
#         form = SearchForm(request.GET)
#         if form.is_valid():
#             query = form.cleaned_data['query']
#             product = get_object_or_404(Product ,title__icontains=query , is_active=True)
#             print(product)
#             return redirect(reverse('product_detail' , kwargs={'pk':product.pk}))
#     else:
#         form = SearchForm()
#         return redirect('pages:home_page')
#
#     return render(request , 'pages/header.html' , {'form': form})


def ajax_search_prodct(request):
    query = request.GET.get('query', '')

    if query:
        product = Product.objects.filter(title__icontains=query, is_active=True)

        product_list = [{'id': product.id, 'title': product.title, 'slug': product.slug} for product in product]
    else:
        product_list = []

    return JsonResponse({'products': product_list})







class AllProductListView(ListView):
    model = Product
    template_name = 'products/all_product.html'
    paginate_by = 12
    context_object_name = 'products'

    def get_queryset(self):
        sort_by = self.request.GET.get('sort_by', 'newest')  # دریافت پارامتر sort_by از GET
        products = Product.objects.select_related('sub_category' , 'category').all()

        # محاسبه قیمت نهایی با توجه به فیلدهای off_price و sell_price
        products = products.annotate(
            final_price=Case(
                When(off_price__isnull=False, then='off_price'),
                default='sell_price',
                output_field=DecimalField()  # استفاده از IntegerField
            )
        )

        # مرتب‌سازی محصولات بر اساس قیمت نهایی
        if sort_by == 'price_asc':
            products = products.order_by('final_price')
        elif sort_by == 'price_desc':
            products = products.order_by('-final_price')

        return products

    def render_to_response(self, context, **response_kwargs):
        # بررسی درخواست AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('products/partials/all_product_partial.html', context)
            return JsonResponse({'html': html})

        # در صورت نبود درخواست AJAX، صفحه کامل رندر شود
        return super().render_to_response(context, **response_kwargs)


class ProductListView(ListView):
    template_name = 'products/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        sort_by = self.request.GET.get('sort_by', 'newest')  # دریافت پارامتر sort_by از GET
        products = Product.objects.select_related('sub_category' , 'category').all()

        # فیلتر بر اساس زیرمجموعه (SubCategory) اگر slug مربوط به زیرمجموعه باشد
        try:
            sub_category = SubCategory.objects.get(slug=slug)
            products = products.filter(sub_category=sub_category).distinct()
        except SubCategory.DoesNotExist:
            pass

        # فیلتر بر اساس دسته‌بندی (Category) اگر slug مربوط به دسته‌بندی باشد
        try:
            category = Category.objects.get(slug=slug)
            products = products.filter(category=category).distinct()
        except Category.DoesNotExist:
            pass

        # محاسبه قیمت نهایی با استفاده از Case و When
        products = products.annotate(
            final_price=Case(
                When(off_price__isnull=False, then='off_price'),
                default='sell_price',
                output_field=DecimalField()
            )
        )

        # مرتب‌سازی بر اساس پارامتر sort_by
        if sort_by == 'price_asc':
            products = products.order_by('final_price')
        elif sort_by == 'price_desc':
            products = products.order_by('-final_price')

        return products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['slug'] = self.kwargs.get('slug')
        return context

    def render_to_response(self, context, **response_kwargs):
        # بررسی درخواست AJAX
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string('products/partials/product_partial.html', context)
            return JsonResponse({'html': html})

        # در صورت نبود درخواست AJAX، صفحه کامل رندر شود
        return super().render_to_response(context, **response_kwargs)


class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product_detail.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # استفاده از محصول موجود در context
        product = context['product']

        # # استفاده از select_related برای کاهش کوئری‌های اضافی
        # similar_products_by_category = Product.objects.filter(
        #     category=product.category,
        #     is_active=True
        # ).exclude(id=product.id).select_related('category', 'sub_category')

        similar_products_by_subcategory = Product.objects.filter(
            sub_category_id=product.sub_category.id,
            is_active=True
        ).exclude(id=product.id).select_related('sub_category')

        # ترکیب کوئری‌ها
        context['similar_products'] =  similar_products_by_subcategory
        context['sub_category'] = product.sub_category

        return context