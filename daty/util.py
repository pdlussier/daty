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
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

#from ast import literal_eval
from gi.repository import GObject
from pickle import dump
from pickle import load as pickle_load
from threading import BoundedSemaphore, Thread

threadLimiter = BoundedSemaphore(10)

class MyThread(Thread):

    def run(self):
        threadLimiter.acquire()
        try:
            super(MyThread, self).run()
        finally:
            threadLimiter.release()

def save(variable, path):
    """Save variable on given path using Pickle

    Args:
        variable: what to save
        path (str): path of the output
    """
    with open(path, 'wb') as f:
        dump(variable, f)
    f.close()

def load(path):
    """Load variable from Pickle file

    Args:
        path (str): path of the file to load

    Returns:
        variable read from path
    """
    with open(path, 'rb') as f:
        variable = pickle_load(f)
    f.close()
    return variable

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

    GObject.idle_add(lambda: on_done(result, error))

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



