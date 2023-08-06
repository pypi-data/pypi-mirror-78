django-component
#################

**Modern components for django templates**
Declarative and composable components inspired by javascript frameworks.

Supports Python **3.6+** and Django **1.11**, **2.0+**, and **3.0+**

Usage
=====

Describe your component:

.. code-block:: python

    # myapp/templatetags/mycomponents.py

    from django_component import Library, Component

    register = Library()

    @register.component
    class Card(Component):
        template = "myapp/card.html"

        class Media:
            css = {"all": ["myapp/card.css"]}
            js = ["myapp/card.js"]
        

.. code-block:: html

    # myapp/templates/myapp/card.html

    <section class="card">
        <header>{{ header }}</header>
        <h1>{{ short_title }}</h1>
        <div>{{ children }}</div>
    </section>

And use them in your templates

.. code-block:: html

    {% load mycomponents %}
    {% components_css %}

    {% Card title="My card's title" %}
        This will be accessible as the `children` variable.
        It's just django template, <span>{{ variable }}</span> !

        {% arg header %}
            This <img src="foo.jpg" />
            will be in the header of the card
        {% endarg %}
    {% /Card %}

    {% components_js %}

``django-component`` also enable context processing per component, see the documentation (TODO) for the complete api.

Why django-component?
======================

``django-component`` make it easy to create reusable template components.
Django has some features to address this, but they all come with some limitations.
``django-component`` unify these features (``block``, ``includes``, ``inclusion_tag``, ``simple_tag``) under an unique api.
In addition ``django-component`` address one of my greatest frustration with reusable components in django: **tracking css and js dependencies** for each component and **include them only when they are effectively used**.


Installation
============

.. code-block:: sh

    pip install django-component

Then add ``django-component`` to your INSTALLED_APPS,
it is also recommended to add django-component.templatetags as builtins templatetags

.. code-block:: python

    INSTALLED_APPS = [
        ...,
        "django_component",
        ...
    ]


    TEMPLATES=[
        {
            'OPTIONS': {
                'builtins': [
                    'django_component.templatetags',
                ]
            },
        }
    ],
