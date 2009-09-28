Helpers for using Google AdSense for Mobile in a Django app.


USAGE:

1) Add `adsense` into your INSTALLED_APPS:

    INSTALLED_APPS = [..., "adsense", ...]

2) Display an ad:

    from adsense.adsense import adsense

    def view(request):
        adsense_publisher_id = "get-from-google"
        ad = adsense(request, adsense_publisher_id, timeout=1, fail_silently=True)
        return HttpResponse(ad)
        
3) Or in a template:

    {% load adsense_tags %}
    
    <p>Fabulous content.</p>
    {% adsensemobile "adsense_publisher_id" %}