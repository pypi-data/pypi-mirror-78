from django.conf.urls import url

import oscar.apps.dashboard.offers.apps as apps


class OffersDashboardConfig(apps.OffersDashboardConfig):
    label = 'offers_dashboard'
    name = 'ms_oscar_flash_offer.dashboard.offers'
    verbose_name = 'Offers dashboard'

    def ready(self):
        super().ready()
        from .views import FlashSaleCreateView

        self.flash_sale_create_view = FlashSaleCreateView

    def get_urls(self):
        urls = [
            url(r'^new/flash-sale/(?P<product_pk>\d+)/$', self.flash_sale_create_view.as_view(),
                name='create-flash-sale'),
        ]
        return super().get_urls() + self.post_process_urls(urls)

