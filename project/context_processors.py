from utils.callbacks import get_brand_config

def brand_theme_context(request):
    return {
        "brand_colors": get_brand_config()
    }
