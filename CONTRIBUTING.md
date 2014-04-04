# Contribute to Baler

Pull requests are welcome!


General Guidelines
------------------

* **Code style.** Please follow local code style. Ask if you're unsure. Python code should conform to PEP8.
* **No warnings.** All python code must run without warnings. All generated code must compile without warnings. All generated code must pass the static analyzer.
* **Stability.** The generated code should be stable; put another way, running `bale` with the same flags should be idempotent. This is so that all generated code changes correspond to actual asset changes.
* **iOS version support.** Generated code should support targets one major iOS version back. E.g., if iOS 7.x is the newest version of iOS, then the code should build and run correctly in an app targeting and deployed on iOS 6.x.
* **Architecture support.** Generated code should support armv7, armv7s, arm64, i386 and x86_64.
* **ARC agnostic.** No code that depends on the presence or absence of ARC should appear in generated public header files.
* **No printing/logging.** Don't log anything to the console.
* **Testing.** Test with the included sample Xcode app, which has extra compatibility warnings enabled.

Design
------

The design decision to have the instance unpack each time to the Cache directory was motivated by several factors:

* **NSBundle support.** It enables NSBundle access, which (most critically) allows bundled strings files to be used by the usual iOS localization engine.
* **Simple.** The mental model is very simple.
* **Lightweight.** Once a shared instance has been created, it no longer requires significant memory resources.
