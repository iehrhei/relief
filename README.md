# 浮雕：谁在雕刻这颗星球

*Relief: Who Carves the Earth*

一篇可以"读出"海底的文章。正文背后是一条真实的海底：大西洋中脊，从北冰洋边缘出发，经过冰岛、亚速尔群岛，一路向南到布韦岛，全长约一万五千公里。

它先以素压的方式藏在纸里。读到哪里，声呐就测到哪里，海底像拓印一样显现出来。读者另有 12 次声呐，结尾会留下一幅属于自己的航迹图，向林璎的《水线》（*Water Line*, 2006）致意。

在线阅读：https://iehrhei.github.io/relief/

---

## 目录结构

```
index.html        页面（HTML、CSS、JS 都在这一个文件里）
relief.json       条带元数据、海岸线、GEBCO 海底地名
relief.bin.gz     海底高程（压缩传输格式，见下文）
relief.bin        海底高程（未压缩备用，int16 小端，单位米）
relief.b64.txt    relief.bin.gz 的 base64 文本版（只给不能托管二进制文件的预览环境用，可删）
fonts/            按本文实际用字裁剪的字体子集
img/              七张档案图版（灰度）
og.jpg            分享卡片图
build/            从原始数据重建以上文件的脚本
```

页面不依赖任何外部服务，字体和数据都随仓库一起提供，所以在中国大陆也能完整显示。

## 海底数据

- **来源**：NOAA National Centers for Environmental Information (2022), *ETOPO 2022 15 Arc-Second Global Relief Model*, doi:10.25921/fd45-gt74。可免费使用与再分发。
- **取样**：经 NOAA CoastWatch ERDDAP，每 1 弧分取一个点，再按 2×2 平均成 2 弧分网格。
- **条带**：
  - 沿大西洋中脊轴线切出，东西方向沿大圆展开，宽约 2,300 公里；
  - 从北纬 85° 到南纬 55.6°，共 4,219 行 × 621 列，每格约 3.7 公里。
- **对位**：南北比例全程一致。锚点是两处真实位置：
  - 「失落之城」（北纬 30°08′）落在讲述它的段落旁；
  - 布韦岛落在最后一段旁边。
- **素压层**：把同一份数据平滑到约 15 公里，模拟卫星测高的分辨率。
- **地名**：依据 GEBCO 海底地名录。

### `relief.bin.gz` 的格式

每一行沿列方向差分（第一列为原值），把 int16 拆成低字节层和高字节层，先存所有低字节，再存所有高字节，最后 gzip 压缩。浏览器用 `DecompressionStream` 解压；不支持的浏览器自动改读 `relief.bin`；两者都取不到时，再读 `relief.b64.txt`。

### 重建

需要 Python 3，以及 numpy、scipy、scikit-image、fonttools、brotli。

```bash
bash build/get_etopo2022.sh       # 从 ERDDAP 下载条带覆盖范围内的 ETOPO 2022（约 100 MB，存到 build/data/）
python3 build/mosaic22.py         # 拼接并平均成 2 弧分网格
python3 build/strip22.py          # 追踪中脊轴线，沿大圆切出条带
python3 build/export22.py         # 导出 relief.bin、relief.bin.gz、relief.json
```

字体子集：先把 npm 上的 `@fontsource/noto-serif-sc`、`@fontsource/cormorant-garamond`、`@fontsource/ibm-plex-mono` 解压到 `build/fontsource/`，然后运行：

```bash
python3 build/fonts.py index.html fonts
```

正文改动后需要重新生成字体子集，否则新增的字会退回系统字体。

## 图版与授权

| 图版 | 作者 / 来源 | 授权 |
|---|---|---|
| 北大西洋水深图，1854 | Matthew Fontaine Maury · NOAA Central Library | 公有领域 |
| 《圣乔治屠龙》浮雕，约 1417 | 多纳泰罗，摄影 Sailko | CC BY 2.5 |
| 塔状蚯蚓粪堆，1881 | Charles Darwin | 公有领域 |
| 颗石藻 *Coccolithus pelagicus* | Richard Lampitt, Jeremy Young, The Natural History Museum, London | CC BY 2.5 |
| 失落之城，2000 | National Science Foundation（UW / WHOI） | 公有领域 |
| 锰结核版画，1907 | Jules Richard，据 Murray & Renard（Challenger） | 公有领域 |
| DISCOL 实验区，2015 | ROV-Team / GEOMAR | CC BY 4.0 |

以上图片均取自 Wikimedia Commons，并已转为灰度。萨普的手稿、贝兰的原画，以及林璎、野口勇、Jason deCaires Taylor 的作品仍受版权保护，页面中只提供链接。

字体：Noto Serif SC、Cormorant Garamond、IBM Plex Mono，均为 SIL Open Font License 1.1。

## 版权

- 文字：© 2026 Rhei Tan，保留所有权利。
- 代码（`index.html` 中的脚本与样式、`build/` 中的脚本）：MIT License，见 `LICENSE`。
- 数据与图片：按上文各自的授权。
