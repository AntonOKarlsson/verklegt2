
def footer_info(request):
    return {
        'company_name': 'Your Company',
        'social_links': {
            'facebook': 'https://facebook.com/castleapartments',
            'twitter': 'https://twitter.com/castleapartments',
            'instagram': 'https://instagram.com/castleapartments',
            'linkedin': 'https://linkedin.com/castleapartments',
        }
    }