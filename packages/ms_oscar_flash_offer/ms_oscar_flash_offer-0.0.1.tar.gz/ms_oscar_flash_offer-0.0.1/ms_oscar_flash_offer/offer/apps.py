import oscar.apps.offer.apps as apps


class OfferConfig(apps.OfferConfig):
    label = 'offer'
    name = 'store.offer'
    verbose_name = 'Offer'
    