from django import template
from urllib.parse import urlparse

register = template.Library()

@register.filter(name='get_icon_class')
def get_icon_class(url):
    if not url:
        return ''
    
    domain = urlparse(url).netloc.lower()
    
    icon_map = {
        'github.com': 'fab fa-github',
        'linkedin.com': 'fab fa-linkedin',
        'instagram.com': 'fab fa-instagram',
        'twitter.com': 'fab fa-twitter',
        'x.com': 'fab fa-twitter',
        'facebook.com': 'fab fa-facebook',
        'youtube.com': 'fab fa-youtube',
        'tistory.com': 'fas fa-blog',
        'velog.io': 'fas fa-blog',
        'medium.com': 'fab fa-medium',
        'mailto:': 'fas fa-envelope'
    }

    if url.startswith('mailto:'):
        return icon_map['mailto:']

    for key, value in icon_map.items():
        if key in domain:
            return value
    
    return 'fas fa-link'

@register.filter(name='get_link_name')
def get_link_name(url):
    if not url:
        return ''
        
    if url.startswith('mailto:'):
        return "Email"

    domain = urlparse(url).netloc.lower()
    
    # Remove 'www.'
    if domain.startswith('www.'):
        domain = domain[4:]
        
    # Capitalize the first letter of the main domain part
    return domain.split('.')[0].capitalize() 