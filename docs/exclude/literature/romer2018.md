# Jones (2022) 

```python exec="1" linenums="1" source="tabbed-left" tabs="Source code|Output" title="hello.py"
print("Hello Markdown!")
print("Hello Markdown2!") # markdown-exec: hide
```

```md exec="1" source="material-block" title="Markdown link"
[Link to example.com](https://example.com)
```

```pycon exec="1" source="console"
>>> print("I'm the result!")
I'm not the result...
```

```console exec="1" source="console"
$ mkdocs --help
```

```tree
root1
    dir1/
    dir2/
    dir3/
```

```python exec="true" html="true" source="tabbed-right" title="Diagrams"
# https://matplotlib.org/stable/gallery/lines_bars_and_markers/scatter_demo2.html
from io import StringIO

import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import numpy as np

# Load a numpy record array from yahoo csv data with fields date, open, close,
# volume, adj_close from the mpl-data/example directory. The record array
# stores the date as an np.datetime64 with a day unit ('D') in the date column.
price_data = cbook.get_sample_data("goog.npz", np_load=True)["price_data"].view(np.recarray)
price_data = price_data[-250:]  # get the most recent 250 trading days

delta1 = np.diff(price_data.adj_close) / price_data.adj_close[:-1]

# Marker size in units of points^2
volume = (15 * price_data.volume[:-2] / price_data.volume[0]) ** 2
close = 0.003 * price_data.close[:-2] / 0.003 * price_data.open[:-2]

fig, ax = plt.subplots()
ax.scatter(delta1[:-1], delta1[1:], c=close, s=volume, alpha=0.5)

ax.set_xlabel(r"$\Delta_i$", fontsize=15)
ax.set_ylabel(r"$\Delta_{i+1}$", fontsize=15)
ax.set_title("Volume and percent change")

ax.grid(True)
fig.tight_layout()

buffer = StringIO()
plt.savefig(buffer, format="svg")
print(buffer.getvalue())
```



:journal-aer:

:journal-ecta:

:journal-jpube:

:journal-oxford-academic:

:fontawesome-regular-face-laugh-wink:

:fontawesome-brands-twitter:{ .twitter }

:octicons-heart-fill-24:{ .heart }




[@zhang1995]


