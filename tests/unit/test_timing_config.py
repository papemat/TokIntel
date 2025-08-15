import importlib, os

def _reload_with(env):
    old = {k: os.environ.get(k) for k in env}
    try:
        for k, v in env.items():
            if v == "":
                os.environ.pop(k, None)
            else:
                os.environ[k] = str(v)
        mod = importlib.import_module("utils.timing_config")
        importlib.reload(mod)
        return mod
    finally:
        for k, v in old.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v

def test_defaults():
    mod = _reload_with({"TIMING_FAST":"", "TIMING_SLOW":""})
    assert mod.FAST == 30.0 and mod.SLOW == 60.0
    assert mod.color_for_duration(10) == "green"
    assert mod.color_for_duration(45) == "orange"
    assert mod.color_for_duration(80) == "red"

def test_custom_thresholds():
    mod = _reload_with({"TIMING_FAST":"20", "TIMING_SLOW":"40"})
    assert mod.color_for_duration(19.9) == "green"
    assert mod.color_for_duration(25) == "orange"
    assert mod.color_for_duration(41) == "red"

def test_bad_values_fall_back():
    mod = _reload_with({"TIMING_FAST":"abc", "TIMING_SLOW":"xyz"})
    assert mod.color_for_duration(10) == "green"
    assert mod.color_for_duration(45) == "orange"
    assert mod.color_for_duration(80) == "red"
