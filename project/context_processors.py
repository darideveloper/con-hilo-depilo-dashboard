from utils.callbacks import get_brand_config

def branding(request):
    return {
        "brand_colors": get_brand_config()
    }
