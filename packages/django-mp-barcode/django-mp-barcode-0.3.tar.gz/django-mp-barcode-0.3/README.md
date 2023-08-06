### Installation

Install with pip:

```
pip install django-mp-product-barcode
```

Add your custom static settings:

```
from product_barcode.settings import BarCodeSettings
```

Models:
```
from product_barcode.models import BarCodeField

bar_code = BarCodeField()
```

Add bar codes to admin:

```
ParentItem(
    _('Bar codes'),
    icon='fa fa-barcode',
    children=[
        ChildItem(
            label=_('Generate bar codes'),
            url='admin:generate-bar-codes'
        )
    ]
),
```

Print bar code button example:
```
{% if object.bar_code %}
    <a href="{% url 'barcode:print' %}?codes={{ object.bar_code }}"
       target="blank"
       class="btn btn-primary btn-sm"
       title="{% trans 'Print bar code' %}">
        <i class="fa fa-barcode"></i>
    </a>
{% endif %}
```
