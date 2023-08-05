|LogoMakr_4ojFPZ|

Motivation

This is a library to use feature toggles as a service. It refresh
toggles from a URL that can be a simple file or a service.

Usage

.. code:: python

   from togglee import Togglee

   url = "https://gist.githubusercontent.com/kanekotic/c469f99bef5a5c0634b4a94a4acd6546/raw/b67985d8e3a5112c9be2da47bdadf2cf17edbe44/toggles"
   refresh_rate_seconds = 5
   default_values = {
       "prop": False
   }
   subject = Togglee(url, refresh_rate_seconds, default_values)
   if subject.is_enabled("prop"):
       print("do stuff")
   else:
       print("dont do stuff")

.. |LogoMakr_4ojFPZ| image:: https://user-images.githubusercontent.com/3071208/90978825-2b93de00-e540-11ea-8e0d-60267e95fec8.png
