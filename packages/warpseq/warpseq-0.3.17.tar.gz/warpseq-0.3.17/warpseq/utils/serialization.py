# ------------------------------------------------------------------
# Warp Sequencer
# (C) 2020 Michael DeHaan <michael@michaeldehaan.net> & contributors
# Apache2 Licensed
# ------------------------------------------------------------------

import importlib

def save_relative_object(root, grand_parent, parent, obj, noref=False, key=None, depth=0):

    from warpseq.model.base import NewReferenceObject

    noref = False
    if obj == root:
        noref == True
    if obj is None:
        return obj
    elif type(obj) in [ str, float, int, bool]:
        return obj
    elif type(obj) in [ list, tuple ]:
        alist = [ save_relative_object(root, grand_parent, parent, x, noref=noref, depth=depth+1) for x in obj if not hasattr(x, 'is_hidden') or not x.is_hidden() ]
        return alist
    elif type(obj) == dict:
        return { k: save_relative_object(root, grand_parent, parent, v, noref=noref, depth=depth+1) for (k,v) in obj.items() if not hasattr(v, 'is_hidden') or not v.is_hidden() }
    elif isinstance(obj, NewReferenceObject) and key in parent.__class__.SAVE_AS_REFERENCES:
        _cls = (obj.__class__.__module__, obj.__class__.__name__,)
        return dict(_ID=obj.obj_id, _TYP=key, _CLS=_cls)
    elif isinstance(obj, object):
        results = dict()
        _cls = (obj.__class__.__module__, obj.__class__.__name__,)
        for k in obj.__slots__:
            if k.startswith("_"):
                continue
            value = getattr(obj, k)
            results[k] = save_relative_object(root, parent, obj, value, noref=noref, key=k, depth=depth+1)
        results['_CLS'] = _cls
        return results
    else:
        raise Exception("error")

def save_object(obj):
    result = save_relative_object(obj, obj, obj, obj, key=None, depth=0)
    return result

# ------------------------------------------------------------------------------------

def load_object(song, data):

    from warpseq.model.track import Track

    if data is None:
        return None

    if type(data) in [ int, float, bool, str ]:
        return data

    elif type(data) == list:
        res = [ load_object(song, x) for x in data ]
        return res

    elif '_ID' in data:
        method = getattr(song, "find_%s" % data['_TYP'])
        res = method(data['_ID'])
        assert res is not None
        return res

    elif '_CLS' in data:
        (mod, classname) = data['_CLS']
        mod = importlib.import_module(mod)
        cls = getattr(mod, classname)
        del data['_CLS']
        params = { x : load_object(song, y) for (x,y) in data.items() }
        res = cls(**params)
        return res

    else:
        res = { k : load_object(song, v) for (k, v) in data.items() }
        return res
