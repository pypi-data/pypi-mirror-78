
*****
oitnb
*****

.. image:: https://sourceforge.net/p/oitnb/code/ci/default/tree/_doc/_static/license.svg?format=raw
   :target: https://opensource.org/licenses/MIT

.. image:: https://sourceforge.net/p/oitnb/code/ci/default/tree/_doc/_static/pypi.svg?format=raw
   :target: https://pypi.org/project/oitnb/

.. image:: https://sourceforge.net/p/oitnb/code/ci/default/tree/_doc/_static/oitnb.svg?format=raw
   :target: https://sourceforge.net/p/oitnb/code


The uncompromising code formatter ``Black`` has very many good points, but by design
it is not very flexible. If you cannot accept it as is, ``oitnb`` might be an
alternative for you.

In short, on top of ``Black``'s features, ``oitnb``:

- defaults to single-quotes, but allows you to select double-quotes for
  strings (triple quotes and an empty string use double-quotes). Option ``--double``.
- allows you to run `meld` for visual comparison of reformatted code,
  so you can easily insert some ``# fmt: off`` at appropriate places. Option ``--meld``.
- reads your configuration in a format that you already know (Python) from a file
  that you most likely already have in your project anyway (``__init__.py``).
- have project spanning base defaults in your configuration directory
  (XDG). That is e.g. where your line-length goes, that is carefully
  brought in sync with your editor width, the width of the three
  terminals fitting on your screen or your multi-file diff utility.
- makes displaying icons optional. They might not display in your
  terminal in the first place, or not fit your professional environment.
- has support for diffing against version committed to the project *before* starting to
  use ``oitnb``


Work-in-progress/things planned:

- triple quotes multi-line strings that start after the left
  parenthesis of a function. Option ``--multi-line-unwrap``. (A must
  if you write a lot of in-file , dedented, strings with YAML, as e.g.
  YAML library developer would.)
- control spreading of multi-element list to one per line
- your wish here (we can always make it a configuration option, command-line option)
- keep alignment of EOL comments

Details
=======

Code base
+++++++++

``oitnb`` code is directly derived from ``Black``'s and uses many files
as-is. 

It can run most of ``Black``'s tests without problems but there is a
handful of errors, which should all have to do with hard-coded
references to `Black` in both file content and file naming.


Extra options, defaults and configuration
+++++++++++++++++++++++++++++++++++++++++

extra options: ``--double``, ``--meld``, ``--multi-line-unwrap``

``oitnb`` defaults to single-quotes around strings, if you want to use
the quoting like ``Black`` has use the option ``--double`` option.

``--meld`` which works like ``--diff``,
but for the invocation of ``meld`` on the original file and the
reformatted version. ``meld`` allows you to directly edit the left
hand side (original) so you can at that point decide to insert some
``# fmt: off`` / ``# fmt: on`` comments around lines, or to abandon
the use of a formatter altogether.

Specifying ``--multi-line-unwrap`` runs an ugly post-processor on the reformatted lines
**undoing** the rewrite of::

  x = yaml.load("""
  a: 1
  b: 2
  """)

into::

  x = yaml.load(
      """
  a: 1
  b: 2
  """
  )


The program starts with an empty config dict and tries to read the basic
configuration from ``oitnb.pon`` in the user config dir using
``appdirs.user_config_dir``. This adheres to the XDG standard on Linux
(i.e. ``~/.config/oitnb)`` if no environment variables are set to
change the defaults. That file should contain a valid Python dict
definition ( with `{}` or `dict()`, and from this ``dict`` the value
for ``default`` is taken (using safe evaluation) to update the config dict::

  dict(
     default=dict(line_length=666, double=True),
  )

After that the directory hierarchy up-the-tree is searched until
``.git`` is found, or ``.hg`` or an ``__init__.py`` file with a module
level definition of ``_package_data``. That should be a dict and from
there the value for the key ``oitnb`` is taken to update the
config::

  _package_data = dict(
      oitnb=dict(line_length=88),
  )
  
``oitnb``'s ``__init__.py`` has more information there used (without ``import``-ing!), and
programmatically updated, by other tools::

  _package_data = dict(
      full_package_name='oitnb',
      version_info=(0, 1, 1),
      __version__='0.1.1',
      author='Anthon van der Neut',
      author_email='a.van.der.neut@ruamel.eu',
      description="oitnb works around some of black's issues",
      entry_points='oitnb=oitnb:main',
      license='MIT',
      since=2018,
      status=alpha,
      package_data={"_oitnb_lib2to3": ["*.txt"]},
      install_requires=['click>=6.5', 'attrs>=17.4.0', 'appdirs', 'toml>=0.9.4'],
      test_suite="_test.test_oitnb",
      tox=dict(
          env='36', 
      ),
      oitnb=dict(line_length=88),
  )
  
  
  version_info = _package_data['version_info']
  __version__ = _package_data['__version__']
  

On top of this, any command-line options are used to overrule the config, and
then the program is initialised. 

Dashes (`-`) in options are internally replaced by underscore (`_`),
you can use that form as key in `dict(op_tion=True)`. With dashes you
would need to use `{"op-tion": True}`

There is currently no computer wide, setting for defaults, such as
``/etc/xdg/oitnb`` (is anyone sharing their development machines these
days?).

Finding changes against pre-``oitnb`` revisions
+++++++++++++++++++++++++++++++++++++++++++++++

If you have an existing project with revision history, and apply
``oitnb`` to your sources, then diffing between pre- and
post-``oitnb`` versions is going to be cluttered.

If your application of ``oitnb`` was applied without Internal errors, and if you did
not have to apply ``# fmt: no`` to often, then you can use the
following to get more useful visual diffs using ``meld``.

The installation of ``oitnb`` includes a minimal utility ``omeld``,
add this as an external diff tool to your mercurials ``.hgrc`` file::

  [extensions]
  hgext.extdiff =
  
  [extdiff]
  cmd.omeld =
  
Now you can execute ``hg omeld -r-4 -r-1`` or ``hg omeld -r-4``
(assuming revision -4 was from before applying ``oitnb``) and
``omeld`` will run ``oitnbt`` on both temporarily created source
trees, before handing those trees over to ``meld``. That means
e.g. that any source changes regarding quotes or removal of
superfluous u's from u'' strings, rewrapping, etc. are going to be the same for both
sides of the revisions. Thereby leaving the real code changes in the
diff that ``meld`` presents.

If the omeld tools gets a file or directory as argument that is **not**
under ``/tmp`` or ``/var/tmp``, it will not run ``oitnb`` on that
file/directory. If you keep your source tree under ``/var/tmp``, you are
out of luck: your python will be formatted.

The above approach: *check out both (old) revisions trees, code format
them with ``oitnb`` and run a diff*, is generic. ``meld`` and ``mercurial`` are just
the tools I use and can easily provide a working setup for.

For git, which in my experience is a bit more difficult to get to
understand multiple external difftools, you can do::

  alias gomeld='git difftool --extcmd=omeld -y'

and use that alias.

``git`` seems somewhat more optimised than ``hg`` in that if the current checked out
version of a file is the same as one of the reversions asked, that it
will not make a temporary version (not even if you have to compare
multiple files). Versions before 0.1.4 should therefore not be used
with the above alias, as those may result updated files
in your source tree (which should not break anything, but not be what
you expected).


Problems you might encounter with Black
=======================================

Double-quotes everywhere
++++++++++++++++++++++++

If you use single-quotes for your strings you are in good company:
`"People use to really love double quotes. I don't know
why. <https://www.youtube.com/watch?v=wf-BqAjZb8M&feature=youtu.be&t=1081>`__. 
And as PEP8 has the following to say about quotes around strings::

   In Python, single-quoted strings and double-quoted strings are the same. This PEP 
   does not make a recommendation for this. Pick a rule and stick to it.

Googling for *Stick to it*: continue or confine oneself to doing or using a particular thing.

It is not just the consistency of confining yourself, it is also the long term continuation.


Unwrapping where a second line might do
+++++++++++++++++++++++++++++++++++++++

If you have a list of short strings that fit on a line and add one so
that it doesn't fit anymore, 

you 

don't 

want 

that

to

all 

of

a 

sudden

force

every 

single

element 

on a new line. Just putting the added overflow on a new line is good enough in those cases.

Funny characters
++++++++++++++++

The Unicode in the messages might not display in the font
you're using (they did not for me with Inconsolata in my Gnome Terminal). Do you
know what those code-points should show?  If not, are you sure that when
using ``Black`` on a different computer, while the person who pays you
for your work looks over your shoulder, that you'll not be embarrassed (or get into
trouble if e.g. they were code-points U+5350 or U+0FD5)?

You might find seeing the SLEEPING FACE (U+1F634), SHORTCAKE (U+1F370),
COLLISION SYMBOL (U+1F4A5), BROKEN HEART (U+1F494), SPARKLES (U+2728)
interesting for a while. But especially when using a small font in order not to scroll too much the details become blurry and no-fun.

Little configurability
++++++++++++++++++++++

The configurability of Black consists inserting lines in Yet Another
Markup Format that adds nothing to the existing spectrum in Yet
Another Config File cluttering your project directory.


 


