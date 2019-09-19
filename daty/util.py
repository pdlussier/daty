# -*- coding: utf-8 -*-

#    util.py
#
#    ----------------------------------------------------------------------
#    Copyright © 2018  Pellegrino Prevete
#
#    All rights reserved
#    ----------------------------------------------------------------------
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

#from ast import literal_eval
from copy import deepcopy as cp
from gi.repository.GLib import idle_add
from gi.repository.Gtk import STYLE_PROVIDER_PRIORITY_APPLICATION, AccelFlags, CssProvider, accelerator_parse
from os import makedirs, umask
from pickle import dumpn
from pickle import load as pickle_load
from re import IGNORECASE, compile, escape, sub
from threading import BoundedSemaphore, Thread

threadLimiter = BoundedSemaphore(4)

class MyThread(Thread):

    def run(self):
        threadLimiter.acquire()
        try:
            super(MyThread, self).run()
        finally:
            threadLimiter.release()

class EntitySet(list):
    def __init__(self, triplet=False):
        self.triplet = triplet

    def add(self, element):
        if element['URI']:
            same_URI = element['URI'] in (v['URI'] for v in self)
            if not same_URI:
                self.append(element)
        else:
            if not element["Label"] in (v["Label"] for v in self):
                self.append(element)
            else:
                for v in self:
                    if element["Label"] == v["Label"]:
                        v = element

def save(variable, path):
    """Save variable on given path using Pickle

    Args:
        variable: what to save
        path (str): path of the output
    """
    with open(path, 'wb') as f:
        dump(variable, f)

def load(path):
    """Load variable from Pickle file

    Args:
        path (str): path of the file to load

    Returns:
        variable read from path
    """
    with open(path, 'rb') as f:
        variable = pickle_load(f)
    return variable

def chmod_recursively(path, mode=0o755):
    from os import chmod, walk
    from os.path import join
    chmod(path, mode)
    for root, dirs, files in walk(path):  
      for d in dirs:  
        current_path = join(root, d)
        print(current_path)
        chmod(current_path, mode)
      for f in files:
        current_path = join(root, f)
        print(current_path)
        chmod(current_path, mode)

def label_color(label, text=None, color='#e5a50a', bold=False):
    label_text = label.get_text()
    try: label.orig == True
    except Exception as e:
        label.orig = cp(label_text)
    if text:
        colored = "".join(["<b><span color='",
                           color,
                           "'>",
                           text,
                           "</span></b>"])
        cu_text = compile(escape(text), IGNORECASE)
        label_text = cu_text.sub(colored, label_text)
    elif bold:
        label_text = "".join(["<b>", label.orig, "</b>"])
    else:
        label_text = label.orig
    label.set_markup(label_text)

def pango_label(label, weight=""):
    label_text = label.get_text()
    try: label.orig == True
    except Exception as e:
        label.orig = cp(label_text)
    if weight:
        label_text = "".join(["<span weight='",
                              weight,
                              "'>",
                              label_text,
                              "</span>"])
    else:
        label_text = label.orig
    label.set_markup(label_text)

def set_text(widget, text, tooltip, markup=False):
    if markup:
        widget.set_markup(text)
    else:
        widget.set_text(text)
    widget.set_tooltip_text(tooltip)

def set_style(context, resource, style_class, enable):
    """Set style

    Args:
        context (Gtk.Context): the context;
        resource (Gtk.Resource): the resource;
        style_class (str): the class name;
        enable (bool): on/off;
        """
    if enable:
        provider = CssProvider()
        provider.load_from_resource(resource)
        context.add_provider(provider, STYLE_PROVIDER_PRIORITY_APPLICATION)
        context.add_class(style_class)
    else:
        context.remove_class(style_class)

def add_accelerator(accelerators, widget, accelerator, signal="activate"):
    """Adds a keyboard shortcut"""
    if accelerator is not None:
        #if DEBUG:
            #print accelerator, widget.get_tooltip_text()
        key, mod = accelerator_parse(accelerator)
        widget.add_accelerator(signal, accelerators, key, mod, AccelFlags.VISIBLE)

def mkdirs(newdir, mode=0o755):
    try:
        original_umask = umask(0)
        makedirs(newdir, mode)
    except OSError:
        pass
    finally:
        umask(original_umask)

def async_call(f, on_done):
  """Calls f on another thread

  Starts a new thread that calls f and schedules on_done to be run (on the main
  thread) when GTK is not busy.

  Args:
    f (function): the function to call asynchronously. No arguments are passed
                  to it. f should not use any resources used by the main thread,
                  at least not without locking.
    on_done (function): the function that is called when f completes. It is
                        passed f's result as the first argument and whatever
                        was thrown (if anything) as the second. on_done is
                        called on the main thread, so it can access resources
                        on the main thread.

  Returns:
    Nothing.

  Raises:
    Nothing.
  """

  if not on_done:
    on_done = lambda r, e: None

  def do_call():
    result = None
    error = None

    try:
      result = f()
    except Exception as err:
      error = err

    idle_add(lambda: on_done(result, error))

  thread = Thread(target = do_call)
  thread.start()

def async_function(on_done = None):
  """Free function async decorator

  A decorator that can be used on free functions so they will always be called
  asynchronously. The decorated function should not use any resources shared
  by the main thread.
  Example:
  @async_function(on_done = do_whatever_done)
  def do_whatever(look, at, all, the, pretty, args):
    # ...

  Args:
    on_done (function): the function that is called when the decorated function
                        completes. If omitted or set to None this will default
                        to a no-op. This function will be called on the main
                        thread.
                        on_done is called with the decorated function's result
                        and any raised exception.

  Returns:
    A wrapper function that calls the decorated function on a new thread.

  Raises:
    Nothing.
  """

  def wrapper(f):
    def run(*args, **kwargs):
      async_call(lambda: f(*args, **kwargs), on_done)
    return run
  return wrapper

# method decorator
def async_method(on_done = None):
  """Async method decorator

     A decorator that can be used on class methods so they will always be called
     asynchronously. The decorated function should not use any resources shared
     by the main thread.
     Example:
     @async_method(on_done = lambda self, result, error: self.on_whatever_done(result, error))
     def do_whatever(self, look, at, all, the, pretty, args):
     
     Args:
         on_done (function): the function that is called when the decorated function
                             completes. If omitted or set to None this will default
                             to a no-op. This function will be called on the main
                             thread.
                             on_done is called with the class instance used, the
                             decorated function's result and any raised exception.

     Returns:
         A wrapper function that calls the decorated function on a new thread.
     Raises:
         Nothing.
  """

  if not on_done:
    on_done = lambda s, r, e: None

  def wrapper(f):
    def run(self, *args, **kwargs):
      async_call(lambda: f(self, *args, **kwargs), lambda r, e: on_done(self, r, e))
    return run
  return wrapper

def download(entity, callback, *cb_args, wikidata=None, use_cache=False, **kwargs):
    """Asynchronously download entity from wikidata
         Args:
            entity (dict): have keys "URI", "Label", "Description"
    """
    if not wikidata:
        from .wikidata import Wikidata
        wikidata = Wikidata()
    def do_call():
        entity['Data'] = wikidata.download(entity['URI'], use_cache=use_cache)
        idle_add(lambda: callback(entity, *cb_args, **kwargs))
        return None
    thread = Thread(target = do_call)
    thread.start()


def get_title(url, callback, *cb_args, **kwargs):
    """Asynchronously download entity from wikidata
         Args:
            entity (dict): have keys "URI", "Label", "Description"
    """
    def do_call():
        from requests import get
        from bs4 import BeautifulSoup
        title = BeautifulSoup(get(url).text).title.string
        idle_add(lambda: callback(url, title, *cb_args, **kwargs))
        return None
    thread = Thread(target = do_call)
    thread.start()

def download_light(URI, callback, *cb_args, wikidata=None, target=["Label", "Description"]):
    """Download an entity returning only a subset of its features

        Args:
            URI (str): the Q/P/L of the entity;
            callback (fun): the callback to give the downloaded entity;
            wikidata (Wikidata): a Wikidata instance (opt);
            target (list): the keys to be recorded in the entity (opt).

        Returns:
            (dict) which has for keys the member of targets.
    """
    if not wikidata:
        from .wikidata import Wikidata
        wikidata = Wikidata()
    def do_call():
        entity, error = None, None
        try:
            entity = wikidata.download(URI, target=target)
        except Exception as err:
            error = err
        idle_add(lambda: callback(URI, entity, error, *cb_args))
    thread = MyThread(target = do_call)
    thread.start()

def edit(URI, claim, target, callback, *cb_args, wikidata=None):
    if not wikidata:
        from .wikidata import Wikidata
        wikidata = Wikidata()
    def do_call():
        error = None
        try:
            wikidata.edit(URI, claim, target)
        except Exception as err:
            error = err
        idle_add(lambda: callback(target, error, *cb_args))
    thread = MyThread(target = do_call)
    thread.start()


def search(query, callback, *cb_args, wikidata=None, filters=[], **kwargs):
    if not wikidata:
        from .wikidata import Wikidata
        wikidata = Wikidata()
    def do_call():
        results, error = [], None
        try:
            results = wikidata.search(query, filters=filters)
        except Exception as err:
            from requests.exceptions import ConnectionError
            if type(err) == ConnectionError:
                error = err
            else:
                raise err
        idle_add(lambda: callback(results, error, *cb_args, **kwargs))
    thread = Thread(target = do_call)
    thread.start()

def select(var, statements, callback, *cb_args, wikidata=None, **kwargs):
    if not wikidata:
        from .wikidata import Wikidata
        wikidata = Wikidata()
    def do_call():
        results, error = None, None
        try:
            results = wikidata.select(var, statements)
        except Exception as err:
            raise err
        idle_add(lambda: callback(results, *cb_args, **kwargs))
    thread = Thread(target = do_call)
    thread.start()

# def import_translations(lang):
#     with open('po/'+lang+'.po', 'r') as g:
#         content = literal_eval(g.read())
#         g.close()
#     return content

#def gtk_style():
#    path = dirname(realpath(__file__))
#    with open(path + '/style.css', 'rb') as f:
#        css = f.read()
#        f.close()
#    style_provider = CssProvider()
#    style_provider.load_from_data(css)
#    StyleContext.add_provider_for_screen(Screen.get_default(),
#                                         style_provider,
#                                         STYLE_PROVIDER_PRIORITY_APPLICATION)



