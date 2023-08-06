import os
import urllib
import urllib.parse
import urllib.request

def register(url):
    data = urllib.parse.urlencode({'action': "register"})
    data = data.encode('ascii')
    r = urllib.request.urlopen(url, data)
    return r.msg

def unregister(url, name):
    data = urllib.parse.urlencode({'action': "unregister",
                                   'name': name})
    data = data.encode('ascii')
    r = urllib.request.urlopen(url, data)
    return r.msg

def bunnies_saved(url, name, number):
    data = urllib.parse.urlencode({'action': "saved",
                                   'name': name,
                                   'number': number})
    data = data.encode('ascii')
    r = urllib.request.urlopen(url, data)
    return int(r.msg)

def bunny_saved(url, name, number):
    data = urllib.parse.urlencode({'action': "saved",
                                   'name': name})
    data = data.encode('ascii')
    r = urllib.request.urlopen(url, data)
    return int(r.msg)

def get_results(url):
    r = urllib.request.urlopen(url + "?notebook=1")
    return r.read().decode("utf-8")
