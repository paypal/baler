Baler
=====

.. image:: https://raw.githubusercontent.com/paypal/baler/master/doc/baler-logo.jpg

Baler is a Python-based tool that makes it easy to bundle and use resources (images,
strings files, etc.) in an iOS static library.

The `card.io`_ and `PayPal iOS SDK`_ projects use baler to include images and
other non-code assets in their SDK static libraries. Developers only
need to add the ``.h`` headers and ``.a`` archive, which includes all
resources.

.. _card.io: https://github.com/card-io/card.io-iOS-SDK
.. _PayPal iOS SDK: https://github.com/paypal/PayPal-iOS-SDK

Baler is *not* a good way to handle assets in a regular consumer-facing
app!

Features
--------

-  Preserves all subdirectory structure (useful for localization via
   ``.lproj`` subbundles)
-  Optional transparent libz compression (good for text, not helpful for images
   only).
-  Resolution- and device-aware image loading very similar to
   ``UIImage's +imageNamed:``.

To see the full set of options, run ``bale -h``.

To use the generated code, look at the generated header file. It should
be documented and self-explanatory. If the help flag to the python
script or the header file is not sufficient documentation, please `file
an issue`_!

.. _file an issue: https://github.com/paypal/baler/issues

The included Xcode project is not needed to use baler. It is useful for
developing baler itself, and for an example integration.


Requirements
------------

-  Python 2 >= 2.6 (pull requests to also support Python 3 welcomed)
-  ARC, deployment target of iOS 6.0+, and Xcode 5+
-  `pip`_

.. _pip: http://www.pip-installer.org/


Installation
------------

Install with pip:

::

    pip install baler

Or download and install from source:

::

    python setup.py install


Usage
-----

Baler generates code. A python script (``bale``) accepts a directory of
assets and generates an Objective-C class that bundles those assets.

Options are documented in the built-in help:

::

    bale -h

Example invocation:

::

    bale resources/bundle_assets/,resources/strings Classes/ --overwrite-delay 0 -z -c BalerBundle

This would use the files in ``resources/bundle_assets`` and
``resources/strings`` to generate a bundle class written to
``Classes/BalerBundle.h`` and ``Classes/BalerBundle.m``, with
compression and no overwrite delay. Be sure to use a class
name more appropriate to your SDK than "BalerBundle", to
avoid possible collisions with other SDKs using baler.

Once the class files are generated, go ahead and add them to your project, then
in your code import the generated header:

::

    #import "MyBalerBundle.h"

And then get and use your bundle normally:

::

    NSBundle *aBundle = [[PPZebraBundle sharedInstance] NSBundle]

Or take advantage of the `imageNamed` method:

::

    UIImage *img = [[MyBalerBundle sharedInstance] imageNamed:@"baler-logo.jpg"];


Integration
-----------

You can integrate baler into your build process in two ways:

1. Manually, by running it whenever you alter your assets.
2. Automatically, by integrating it into your Xcode build.

Manual Use
~~~~~~~~~~

A quick way to get running is to manually invoke baler whenever you
change, add, delete, or move assets.

1. Install baler as described above.
2. Run
   ``bale <dir_containing_assets> <dir_for_output_code>``.
3. Add the output code to your project. Refer to the header file
   (e.g. ``BalerBundle.h``) for usage.
4. If using compression, add ``libz.dylib`` in the Link Binary With
   Libraries build phase.


Automated Use
~~~~~~~~~~~~~

Instead of running `bale` manually each time you want to update the generated code, you can add a `bale` step into your Xcode project.

1. Install baler as described above.

2. Place the assets that you want to include in a subdirectory (e.g. `baled_assets`), usually alongside your `.xcodeproj` bundle. Optional: You can add this directory to your
   Xcode project if you want, but be sure not add them to any targets.

3. Create a **Run Script** build phase. In your project/target's Build Phases tab -- before the Compile Sources phase -- add an appropriate invocation of `bale`, e.g.

   ::

      /path/to/python/env/bin/bale baled_assets Classes --overwrite-delay 0 -c BalerBundle

   This will regenerate the bundle from the assets each time you build. See tips below for more further advice.

4. Add the generated files (e.g. ``Classes/BalerBundle.[h|m]``) to your Xcode project as usual. Refer to the header file (e.g. `BalerBundle.h`) for usage.

5. If using compression, add ``libz.dylib`` in the Link Binary With Libraries build phase.

6. Optional: Add the generated classes' self-tests to your unit tests.

   Set ``BALER_DEBUG=1`` in your test target settings, then use the bundle instance's ``passesSelfTest`` method:

   ::

        NSError *bundleSelfTestError = nil;
        BOOL pass = [[BalerBundle sharedInstance] passesSelfTest:&bundleSelfTestError];
        STAssertTrue(pass, @"BalerBundle failed self-test with error %@", bundleSelfTestError);


Run Script tips
```````````````

Skip if baler isn't set up
''''''''''''''''''''''''''

You can ensure the build progresses even if the baler invocation fails by having the shell command swallow the non-zero return code from baler, e.g.

::

    /path/to/python/env/bin/bale baled_assets Classes --overwrite-delay 0 || echo "Failed to generate bundle"

This keeps the coupling with baler a little looser, so other contributors won't need baler to build the project.

BYOB (Bring Your Own Baler)
''''''''''''''''''''''''''''

You may want to let your teammates specify which baler to use in a `.gitignore`'d shell script. For example, a `.env`:

::

    export PATH="/path/to/python/env/bin:$PATH"

Then your Run Script would look like this:

::

    [ -f .env ] && source .env 2>/dev/null
    bale ...

Contribute
----------

Pull requests and new issues are welcome. See CONTRIBUTING.md_ for details.

.. _CONTRIBUTING.md: https://github.com/paypal/baler/blob/master/CONTRIBUTING.md


Thanks
------

Logo image
~~~~~~~~~~

The baler logo is modified and shared with permission of Wikimedia Commons using the same `Creative Commons Attribution-Share Alike 3.0 Unported license.`_ See also the `original image and license`_.

.. _Creative Commons Attribution-Share Alike 3.0 Unported license.: http://creativecommons.org/licenses/by-sa/3.0/deed.en
.. _original image and license: http://commons.wikimedia.org/wiki/File:Britains_-_Fiat_880DT_and_a_hay_baler.jpg

Contributors
~~~~~~~~~~~~

* `Dave Goldman`_
* `Roman Punskky`_
* `Josh Bleecher Snyder`_
* `Brent Fitzgerald`_

.. _Dave Goldman: https://github.com/dgoldman-ebay/
.. _Roman Punskky: https://github.com/romk1n/
.. _Josh Bleecher Snyder: https://github.com/josharian/
.. _Brent Fitzgerald: https://github.com/burnto/

Brought to you by `PayPal`_.

.. _PayPal: https://paypal.com/

