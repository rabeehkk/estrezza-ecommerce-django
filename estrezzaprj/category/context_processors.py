from .models import Category

def menu_links(requests):
    links = Category.objects.all()
    return dict(links=links)