# baby_heap_buffer_overflow 解题思路

## 1. 漏洞点

`object` 的结构体大小只有 `0x40`：

```c
struct object_t {
  char content[64];
};
```

但读取函数使用了：

```c
fgets(object->content, 0x64, stdin);
```

`fgets(..., 0x64, ...)` 最多会写入 `0x63` 字节，再补 `\0`，会越界覆盖到紧随其后的 `vtable` 堆块。

## 2. 程序关键布局

程序先后执行：

1. `malloc(sizeof(object_t))`
2. `malloc(sizeof(vtable_t))`

因此在常见 glibc 堆布局下：

- `object->content` 在前一个 chunk 的 user 区。
- `vtable` 在下一个 chunk 的 user 区，里面有两个函数指针：
  - `vtable->read`
  - `vtable->write`

利用越界可以改写这两个函数指针。

## 3. 利用策略

直接把 `read` 改成 `system` 不稳，因为触发 `read` 时传入的是 `object` 指针，而本次输入本身也会覆盖 `content`。

更稳定的方式：

1. 第一次 `cmd=1`：构造溢出，保持 `vtable->read = read_name`，把 `vtable->write` 改成 `system@plt`。
2. 第二次 `cmd=1`：正常输入命令字符串到 `object->content`（例如 `cat /flag`）。
3. 第三次 `cmd=2`：实际上调用 `system(object->content)`，命令执行。

## 4. 关键地址

- `read_name = 0x400877`
- `system@plt = 0x400730`

二进制为 **No PIE**，地址固定，可直接写死。

## 5. 一键利用

默认读取 `/flag`：

```bash
python3 solve.py
```

指定任意命令：

```bash
python3 solve.py --cmd 'id'
```

自动尝试常见 flag 路径：

```bash
python3 solve.py --try-common-flags
```

## 6. 说明

- 该 PoC 会破坏相邻 chunk 元数据，程序退出时可能触发 glibc 的 `double free or corruption (out)`，属于预期现象，不影响命令执行结果。
- 当前这个本地仓库环境中未提供 flag 文件，因此会看到 `No such file or directory`；把同样脚本用于真实靶机/远程环境即可直接读取对应路径的 flag。
