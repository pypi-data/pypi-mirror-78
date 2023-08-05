# remote-ssh-tunnel-controller-lib

![Run tests](https://github.com/guallo/remote-ssh-tunnel-controller-lib/workflows/Run%20tests/badge.svg)
![Upload release assets](https://github.com/guallo/remote-ssh-tunnel-controller-lib/workflows/Upload%20release%20assets/badge.svg)

```shell
pip install remote-ssh-tunnel-controller-lib
```

```python3
>>> from rssht_controller_lib import factories
>>> ctl = factories.RSSHTControllerFactory.new()
>>> ctl.update()
>>> ctl.get_agents()
(<RSSHTAgent: raspberry-pi-1>, <RSSHTAgent: other-agent>)
...
... # use ctl's object tree
...
>>> ctl.dispose()  # break cyclic references before ctl's deletion
```
