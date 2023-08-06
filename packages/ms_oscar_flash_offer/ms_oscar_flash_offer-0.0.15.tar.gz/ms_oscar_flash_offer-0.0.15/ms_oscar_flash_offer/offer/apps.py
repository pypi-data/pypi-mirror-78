import oscar.apps.offer.apps as apps


class OfferConfig(apps.OfferConfig):
    label = 'offer'
    name = 'ms_oscar_flash_offer.offer'
    verbose_name = 'Offer'
    