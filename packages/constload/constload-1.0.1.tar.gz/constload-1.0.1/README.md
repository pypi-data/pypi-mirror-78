# constload

![Tests](https://github.com/codemicro/constload/workflows/Tests/badge.svg)

constload is a package designed to simplify the process of loading settings into Python applications by providing
certain functionality that is frequently reimplemented from project to project. This includes the ability to set
defaults and set certain parameters as required.

### Usage examples

When loading settings, you have a couple of options. You can provide pre-parsed data in a dictionary, or you have have
data parsed for you from a filepath or from a string.

```python
from constload import ConstantLoader

# Loading JSON from file
c = ConstantLoader("/path/to/settings/file.json")

# Loading JSON from string
c = ConstantLoader("{'hello': 'world'}")

# Using preloaded dict
c = ConstantLoader(your_dict)
```

It's also trivial to write your own loaders.

```python
def my_loader(data):
    # Basic CSV loader
    my_dict = {}
    lines = data.split("\n")
    for line in lines:
        vals = line.split(",")
        my_dict[vals[0]] = vals[1:]
    return my_dict

c = ConstantLoader("/path/to/file.csv", loader=my_loader)

```

When you've got your data loaded, you can begin to extract values.

This is done by using tuples that contain paths to your values.

```python
# ("user", "name") is equivalent to ["user"]["name"]
USER_NAME = c.required(("user", "name"))
USER_PETS = c.default(("user", "pets"), [])
```

Any changes made by `c.default` are automatically mirrored to the dictionary as they're being made. This means you can
work directly with the dictionary, if you so choose.

```python
c.default(("user", "pets"), [])
c.data["user", "name"]  # -> []
```

### Installing

* With YAML support - `pip install constload[yaml]`
* Otherwise - `pip install constload`

### Licence

Licenced under the Mozilla Public Licence 2.0. [Licence text.](https://www.github.com/codemicro/constload/blob/master/LICENCE)


### Support

If you need help, feel free to open an issue.

### Contributing

Issues/pull requests are welcome. :)
