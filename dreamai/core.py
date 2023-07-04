# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['flatten_list', 'noop', 'is_list', 'is_tuple', 'list_or_tuple', 'is_iter', 'is_dict', 'is_df', 'is_str', 'is_int',
           'is_float', 'is_array', 'is_pilimage', 'is_img', 'is_set', 'is_path', 'path_or_str', 'is_subscriptable',
           'is_clip', 'path_name', 'path_stem', 'path_suffix', 'extend_path_name', 'end_of_path', 'last_modified',
           'load_yaml', 'save_obj', 'load_obj', 'resolve_data_path', 'yml_to_pip', 'reqs_to_pip', 'set_pip_req',
           'uniq_lines', 'update_settings', 'dict_values', 'dict_keys', 'sort_dict', 'locals_to_params', 'list_map',
           'next_batch', 'model_children', 'replace_dict_key', 'proc_fn', 'filter_dict', 'setify', 'get_files']

# %% ../nbs/00_core.ipynb 3
from .imports import *


# %% ../nbs/00_core.ipynb 4
# def default_device(device=None):
# if device is None:
# device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
# return device


def flatten_list(l):
    "Flatten a list of lists."
    l2 = []
    for x in l:
        if is_list(x):
            l2 += flatten_list(x)
        else:
            l2.append(x)
    return l2


def noop(x=None, **kwargs):
    "Do nothing."
    return x


def is_list(x):
    return isinstance(x, list)


def is_tuple(x):
    return isinstance(x, tuple)


def list_or_tuple(x):
    return is_list(x) or is_tuple(x)


def is_iter(o):
    "Test whether `o` can be used in a `for` loop."
    return isinstance(o, (Iterable, Generator)) and getattr(o, "ndim", 1)


def is_dict(x):
    return isinstance(x, dict)


def is_df(x):
    return isinstance(x, pd.core.frame.DataFrame)


def is_str(x):
    return isinstance(x, str)


def is_int(x):
    return isinstance(x, int)


def is_float(x):
    return isinstance(x, float)


# def is_array(x):
#     return isinstance(x, np.ndarray)


def is_array(x):
    "`True` if `x` supports `__array__` or `iloc`"
    return hasattr(x, "__array__") or hasattr(x, "iloc")


def is_pilimage(x):
    return "PIL" in str(type(x))


def is_img(x):
    return is_array(x) or is_pilimage(x)


def is_set(x):
    return isinstance(x, set)


def is_path(x):
    return isinstance(x, Path)


def path_or_str(x):
    return is_str(x) or is_path(x)


def is_subscriptable(x):
    return hasattr(x, "__getitem__")


def is_clip(x):
    return type(x).__name__ == "ProntoClip" or "moviepy" in str(type(x))


def path_name(x):
    return Path(x).name


def path_stem(x):
    return Path(x).stem


def path_suffix(path):
    return Path(path).suffix


def extend_path_name(p, s="_2"):
    "Add `s` to the name of a path `p`. Before the extension."
    p = Path(p)
    return p.parent / (p.stem + s + p.suffix)


def end_of_path(p, n=2):
    "Get the last `n` parts of a path `p`."
    p = Path(p)
    parts = p.parts
    p = Path(parts[-n])
    for i in range(-(n - 1), 0):
        p /= parts[i]
    return p


def last_modified(x):
    "Get the last modified time of a file."
    return x.stat().st_ctime


def load_yaml(file):
    with open(file) as f:
        env = load(f, Loader=Loader)
    return env


def save_obj(path, obj):
    with open(path, "wb") as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


def load_obj(path):
    with open(path, "rb") as f:
        return pickle.load(f)


def resolve_data_path(data_path):
    if not is_list(data_path):
        data_path = [data_path]
    data_path = flatten(data_path)
    paths = []
    for dp in data_path:
        if path_or_str(dp):
            dp = Path(dp)
            if not dp.exists():
                raise Exception(f"Path {dp} does not exist.")
            if dp.is_dir():
                paths.append(dp.iterdir())
            else:
                paths.append([dp])
    return chain(*paths)


def yml_to_pip(yml, less_eq=True, remove_eq=False, ignore=["nvidia"]):
    "Get pip packages from a conda environment `yml` file."
    env = load_yaml(yml)
    env_pip = env["dependencies"][-1]["pip"]
    pip_list = []
    for x in env_pip:
        if not any([ign.lower() in x.lower() for ign in ignore]):
            if remove_eq:
                x = x.split("==")[0].split(">=")[0]
            elif less_eq and "torch" not in x:
                x = x.replace("==", "<=")
            pip_list.append(x)
    # if remove_eq:
    # env_pip = [x.split('==')[0].split('>=')[0] for x in env_pip]
    return " ".join(np.unique(pip_list))


def reqs_to_pip(reqs, less_eq=True, remove_eq=False, ignore=["nvidia"]):
    pip_list = []
    with open(reqs) as f:
        for x in f.readlines():
            x = x.strip()
            if not any([ign.lower() in x.lower() for ign in ignore]):
                if remove_eq:
                    x = x.split("==")[0].split(">=")[0]
                elif less_eq and "torch" not in x:
                    x = x.replace("==", "<=")
                pip_list.append(x)
    return " ".join(np.unique(pip_list))


def set_pip_req(req_file, settings, less_eq=True, remove_eq=False, ignore=["nvidia"]):
    "Update the pip_requirements in settings.ini from a conda environment `yml` file."
    # env_pip = yml_to_pip(yml, less_eq=less_eq, remove_eq=remove_eq, ignore=ignore)
    env_pip = reqs_to_pip(req_file, less_eq=less_eq, remove_eq=remove_eq, ignore=ignore)
    config = ConfigParser(delimiters=["="], allow_no_value=True)
    config.read(settings)
    cfg = config["DEFAULT"]
    config.set("DEFAULT", "pip_requirements", env_pip)
    with open(settings, "w") as configfile:
        config.write(configfile)


def uniq_lines(file):
    lines = set(open(file).readlines())
    open(file, "w").writelines(lines)


def update_settings(path="dreamai_pdf"):
    path = Path(path)
    uniq_lines(path / "reqs.txt")
    set_pip_req(path / "reqs.txt", path / "settings.ini")


def dict_values(d):
    "Get the values of a dictionary sorted by key."
    return [v for _, v in sorted(d.items(), key=lambda x: x[0])]


def dict_keys(d):
    "Get the sorted keys of a dictionary."
    return [k for k, _ in sorted(d.items(), key=lambda x: x[0])]


def sort_dict(d, by_value=False):
    "Sort a dictionary by key by default or by value if `by_value` is True."
    idx = int(by_value)
    return {k: v for k, v in sorted(d.items(), key=lambda item: item[idx])}


def locals_to_params(l, omit=[], expand=["kwargs"]):
    "Convert all the local variables to a dictionary of parameters."
    if "kwargs" not in expand:
        expand.append("kwargs")
    omit += ["self", "__class__"]
    l = {k: v for k, v in l.items() if k not in omit}
    l = copy.deepcopy(l)
    keys = dict_keys(l)
    for k in keys:
        if k in expand:
            for k2 in l[k]:
                if k2 not in l.keys():
                    l[k2] = l[k][k2]
            del l[k]
        if k in omit:
            del l[k]
    return l


def list_map(l, m):
    "Apply `m` to each element of `l`."
    return list(pd.Series(l).apply(m))


def next_batch(dl):
    "Get the next batch from a dataloader `dl`."
    return next(iter(dl))


def model_children(model):
    "Get the children of a model."
    return list(model.children())


def replace_dict_key(
    d: dict, x="", y="", strict=False
):  # If True, replace if `x` == key. If False, replace if `x` in key.
    "Replace key `x` with `y` in dictionary `d`."
    if (x == "" and y == "") or x == y:
        return d
    if strict:
        fn = lambda k: k.replace(x, y) if x == k else k
    else:
        fn = lambda k: k.replace(x, y) if x in k else k
    return {fn(k): v for k, v in d.items()}


def proc_fn(fn):
    "Process function `fn`. It can be a string to match or a function that takes a key and returns True/False."
    if is_str(fn):
        t = copy.deepcopy(fn)
        fn = lambda x: x == t
    return fn


def filter_dict(
    d, fn
):  # Can be a string to match or a function that takes a key and returns True/False.
    "Filter dict `d` based on function `fn`."
    d2 = {}
    fn = proc_fn(fn)
    keys = dict_keys(d)
    for k in keys:
        if fn(k):
            d2[k] = d[k]
    return d2


def setify(o):
    return o if isinstance(o, set) else set(list(o))


def _get_files(p, fs, extensions=None):
    p = Path(p)
    res = [
        p / f
        for f in fs
        if not f.startswith(".")
        and ((not extensions) or f'.{f.split(".")[-1].lower()}' in extensions)
    ]
    return res


def get_files(
    path, extensions=None, recurse=True, folders=None, followlinks=True, make_str=False
):
    "Get all the files in `path` with optional `extensions`, optionally with `recurse`, only in `folders`, if specified."
    if folders is None:
        folders = list([])
    path = Path(path)
    if extensions is not None:
        extensions = setify(extensions)
        extensions = {e.lower() for e in extensions}
    if recurse:
        res = []
        for i, (p, d, f) in enumerate(
            os.walk(path, followlinks=followlinks)
        ):  # returns (dirpath, dirnames, filenames)
            if len(folders) != 0 and i == 0:
                d[:] = [o for o in d if o in folders]
            else:
                d[:] = [o for o in d if not o.startswith(".")]
            if len(folders) != 0 and i == 0 and "." not in folders:
                continue
            res += _get_files(p, f, extensions)
    else:
        f = [o.name for o in os.scandir(path) if o.is_file()]
        res = _get_files(path, f, extensions)
    if make_str:
        res = [str(o) for o in res]
    return list(res)
