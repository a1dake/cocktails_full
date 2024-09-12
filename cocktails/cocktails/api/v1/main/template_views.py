from django.shortcuts import render


def legal_page(request):
    return render(request, 'license_agreement.html', locals())


def offer_page(request):
    return render(request, 'offer.html', locals())
