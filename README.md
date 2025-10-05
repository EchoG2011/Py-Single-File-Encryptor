

## 0. 30 秒速览
| 你是开发者 | 你是最终用户 |
|------------|--------------|
| 1. 改密码 → 2. 运行脚本 → 3. 得到 `decryptor_single.py` | 1. 拿到 `decryptor_single.py` → 2. `python decryptor_single.py` → 3. 程序直接跑 |

---

## 1. 下载与安装
### 1.1 克隆仓库
```bash
git clone https://github.com/你的用户名/py-single-file-encryptor.git
cd py-single-file-encryptor
```

### 1.2 安装唯一依赖
```bash
# 建议建个虚拟环境，可选
python -m venv venv
source venv/bin/activate      # Windows 用 venv\Scripts\activate
pip install pycryptodome
```

---

## 2. 打包方：加密你的脚本
### 2.1 改密码（必须）
用任何编辑器打开 `make_single_file.py`，找到第 10 行：
```python
PWD = b"YourPassword123"   # ← 改成你自己的密码
```
保存。

### 2.2 一键加密（图形界面）
```bash
python make_single_file.py
```
* 弹出文件选择框 → 选中你要加密的 `xxx.py` → 点“打开”。  
* 同目录立刻生成 `decryptor_single.py`，这就是最终发给用户的文件。

### 2.3 批量/命令行调用（可选）
```bash
python make_single_file.py src/my_script.py dist/my_script_decrypt.py
```
参数说明：
| 参数 | 说明 |
|------|------|
| 第 1 个 | 要加密的源 `.py` |
| 第 2 个 | 输出的解密器文件名（可省略，默认 `src/decryptor_single.py`） |

---

## 3. 最终用户：运行加密脚本
用户 **不需要源码、不需要依赖、不需要 Python 环境配置**（只要机器装了 Python 3.7+ 即可）。

### 3.1 最简命令
```bash
python decryptor_single.py
```
脚本会在内存里解密并执行你的原始代码，效果与直接 `python original.py` 完全一致。

### 3.2 传参也能用
```bash
python decryptor_single.py --help
python decryptor_single.py arg1 arg2
```
参数会**原封不动**透传给原始脚本。

---

## 4. 自定义场景示例
### 4.1 把解密器变成可执行图标（Windows）
```bash
pip install pyinstaller
pyinstaller -F -w -i app.ico decryptor_single.py
```
dist 目录下生成 `decryptor_single.exe`，双击即可运行。

### 4.2  Linux / macOS 开机自启
```bash
chmod +x decryptor_single.py
sudo cp decryptor_single.py /usr/local/bin/myapp
# 加 systemd 或 launchd 服务即可
```

---

## 5. 技术细节（懂加密的同学看）
| 项目 | 值 |
|------|----|
| 对称算法 | AES-256-GCM |
| 密钥派生 | PBKDF2-HMAC-SHA256，迭代 500 000 次 |
| 盐长度 | 32 B（随机） |
| Nonce  | 16 B（随机） |
| Tag    | 16 B（GCM 认证标签） |
| 密文格式 | `salt(32) + nonce(16) + tag(16) + ct(len)` |
| 编码 | Base64（无换行） |
| 解密流程 | 内存解密 → `compile()` → `exec()`，**不落地磁盘** |

---

## 6. 安全警告 & 免责
1. 密码硬编码在文件里，**任何人拿到解密器都能逆向出字节码**，无法对抗专业逆向。  
2. 仅适用于“防君子不防小人”场景：内部脚本、小工具分发、CTF 出题、演示 Demo 等。  
3. 如需商业级保护，请考虑：  
   - Cython 编译 `.pyd` / `.so`  
   - 混淆 + 加壳（PyArmor、Nuitka）  
   - 硬件绑定 / 远程授权校验  
4. 作者不对因误用或破解造成的任何损失负责。

---

## 7. 常见问题（FAQ）
**Q1 用户电脑没装 `pycryptodome` 怎么办？**  
A：解密器里只用到标准库 + `Crypto.Cipher`，运行时会报错。可提前用 PyInstaller 把依赖打进去（见 4.1）。

**Q2 可以加密整个包吗？**  
A：目前只支持单文件。如需整包，先 `zip -r pkg.zip mypkg/` 再把 zip 当脚本加密，解密后内存解压并 `import` 即可（模板稍后会更新）。

**Q3 为什么每次加密结果都不一样？**  
A：盐、nonce 都是随机生成，所以密文不同，但都能解密。

**Q4 加密后文件变大多少？**  
A：固定增加 96 字节头（64 B 原始 + Base64 膨胀约 1.33 倍），整体 ≈ 原始大小 ×1.34。

---

## 8. 更新日志
| 日期 | 版本 | 说明 |
|----|----|------|
| 2025-10-05 | v1.0 | 首版，单文件加密 & 图形界面 |

---

## 9. 贡献 & 反馈
欢迎提 Issue / PR：  
- 想支持文件夹加密  
- 想换成 ChaCha20-Poly1305  
- 想加许可证校验  
直接到 [Issues](https://github.com/你的用户名/py-single-file-encryptor/issues) 留言即可。

---

## 10. 许可证
MIT License — 可商用、可修改、可再分发，只需保留原始版权行。

```
```
