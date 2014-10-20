from django.template.defaultfilters import title
from django.utils.translation import ugettext_lazy as _

from cmsplugin_top_products.models import TopProducts
from cms.models.pluginmodel import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
from shop.models.productmodel import Product
from shop.util.cart import get_or_create_cart
from shop.models.productmodel import Product
from shop.models.ordermodel import OrderItem
from ashop.models.productmodels import SingleProduct


# from shop.models.defaults.product.Product import Product

class SingleProductPlugin(CMSPluginBase):
    model = SingleProduct
    admin_preview = False
    name = title(_('single product plugin'))
    render_template = "shop/plugins/single_product.html"
    
    def render(self, context, instance, placeholder):
        
        context.update({
            'instance': instance,
            'style': instance.style,
            'object': instance.product,
            'placeholder': placeholder,
        })
        return context
 
#plugin_pool.register_plugin(SingleProductPlugin)



class CartPlugin(CMSPluginBase):
    model = CMSPlugin
    name = _("ASHOP Cart")
    render_template = "shop/plugins/cart.html"

    def render(self, context, instance, placeholder):
        request = context['request']
        cart = get_or_create_cart(request)
        
        cart_items = cart.items.all() # hm, w ? t ?? f ???
        
        # help(cart)
        
        print cart.total_quantity
        
        context.update({'cart':cart})
        context.update({'cart_items':cart_items})

        return context
    
plugin_pool.register_plugin(CartPlugin)