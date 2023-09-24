# CONTRIBUTING GUIDE

如果对汉化内容有异议或见解，可以在 Steam 或 Github 上留言讨论，以帮助优化/参与翻译

警告：以下部分为汉化制作的相关信息，可能包含一定的剧透性质内容

# 开发 & 规约

## 使用 Git 在本地 安装/加载 模组

在 Draft 期间，需要不通过 workshop 加载模组。此时只需要在 "模组/mods"菜单下，选择 "资源管理器中打开路径" 后，直接在该路径下执行 git clone。

如此在游戏重新启动后即可在列表中找到此模组

## 版本RELEASE / GIT-TAG命名规则

mod的版本号为X.X.X.X的格式，其中前三位为翻译制作时所对应的游戏版本，最后一位是翻译文本的版本。

前三位的调整仅依据官方英文文本源而非游戏本身的更新进行。

X.X.X.0 版本计划对应于通过脚本自动在游戏更新后生成的临时汉化，实际发布的汉化版本尾号数字从1开始计数

# 翻译游戏文本

官方在[GITHUB:WaywardGame/english-language](https://github.com/WaywardGame/english-language)中已经提供了提取出的原始文本

为便于译制，该项目作为此项目的依赖项，设置于 mod-reference\english-official 路径下

## 存疑项列表

#### 部分文本因未找到在游戏中对照核对的方法，翻译是否得体有待确认

+ action的子项中，各个行为的进阶效果
    + 多个行为中关于技艺提升的表述存在细微差异，应根据实际效果统一意译
    + 屠宰 声望变化的表述存在矛盾的可能
    + 休息 不确定睡眠周期具体实质效果，此处应当根据游戏内功效意译

+ somethingInTheWayOf 一类中
    + 不特定场景的几项，有可能因为语法差异产生奇怪的表达，可能需要视实际场景对表述进行微调

+ bothEffectiveIneffective一项，不确定是否吻合实际效果

+ 铸铁/精铁 译作 铁/钢 表意更佳，可惜与游戏内贴图不是很吻合；铸铁/铁的翻译则容易让人误认为铸铁品质更佳，对比性没有 铸铁/精铁 这一组更好，尽管精铁XX有的时候还是感觉有点别扭

+ ~~ category 未找到实际使用场景，字面含义与 group 一项重叠 ~~ 开发者已确认该项未实际使用，属于旧版本遗留内容

#### 部分文本应可改善为更贴合游戏风格的雅译

+ 物品品质quality，游戏中大部分物品工具并不玄幻不适合“稀有史诗传说”的描述，但是原文直译中，优秀杰出的高品质用词区分度不够明显


## [译制材料] 特殊词译表

有一些词汇由于其性质会在多个不同的系统或是物品中反复出现，对此翻译时尽量统一了用语以便减少实际游玩时的割裂感。具体词表如下

### 通用
+ Action       进行
+ Item Action  使用

---

### 物品强化
+ upgrade       升格
+ enhance       强化
+ enchant       注魔
+ alter         转魔
+ absorb        汲取
+ exude         浸注
+ refine        精炼
+ transmogrify  异化
+ reinforce     加固

---

### 火

#### Action 
+ startFire    引火
+ stokeFire    添火
+ ignite       点燃
+ extinguish   熄火
+ smotherFire  灭火

#### Item doodad
+ Campfire    营火
+ TorchStand  火炬

#### item
+ firePlough  火犁
+ handDrill   手钻

#### Group
+ fireSource         火源
+ firemaking         生火物
+ campfire           营火
+ tinder             火绒
+ kindling           柴火
+ fireStarter        起火器
+ litTorch           点燃的火把
+ fireExtinguisher   灭火器
+ becomesFireSource  生火

---

### 材质
+ wooden        木
+ granite       石
+ leather       皮
+ scale         鳞
+ armoredScale  坚甲
+ iron          精铁
+ wroughtIron   铸铁
+ tin           锡
+ copper        铜
+ bronze        青铜
+ blackplate    黑钢
+ obsidian      黑曜石
+ basalt        火山岩
+ rawClay       生黏土/...的生胚
+ clay          黏土(对建材)/陶制
+ sandstone     砂石
+ talc          滑石
+ limestone     石灰岩
+ seawater                海水
+ desalinated water       淡水
+ medicinal water         药水
+ purified fresh water    净水
+ unpurified fresh water  未净化淡水
+ goat milk               羊奶

# 时间
+ nighttime  午夜
+ dawn       拂晓
+ sunrise    清晨
+ daytime    白昼
+ sunset     傍晚
+ dusk       黄昏

---

### 其他
+ water still  蒸馏器
+ milestone 丰碑

# 工具脚本

繁体中文生成 与 Version Update Tool 的功能均在 \mod-reference 下的 translate_tools.py 中实现
运行环境需求py 3.11以及zhconv py库（可pip install）

此外，translate_tools_cli / translate_tools_gui 分别基于 config 提供简易的命令行及图形界面，win下可以通过 run_gui.bat 直接双击运行启动 GUI

特别注意，cli与gui运行时默认已经 cd 至mod-reference后的相对路径，且资源文件路径按照tool_configs_default.json下配置（官方英文可从官方git中拉取）。如需修改配置建议将默认config复制至data后修改

以下提供两个脚本的简易实现思路，具体说明请参考代码中的注释

## 繁体中文生成

简繁转换使用 python 的 zhconv 项目来自动生成，当前目标繁体设置为 zh-tw
zhconv 中无任何额外设置，所有选项均为默认

## Version Update Tools

脚本工具集提供4组功能，对应不同场景使用：
+ 在大版本更新后原英文产生大量变更时辅助更新时，原始的英文文本也会在[GITHUB:WaywardGame/english-language](https://github.com/WaywardGame/english-language)中同步更新，此时需要对文本增删改三部分进行对应的更补。
+ 在本地进行翻译的过程中，需要比对原本与新版本格式对应的汉化文本，以确认未翻译部分的文档
+ 在完成翻译后，需要将新翻译的部分与之前的版本进行合并
+ 在发布更新前，需要自动生成繁体版本

### 原理 & 机制 & 功能

基于翻译文档的json格式，逐个key检索其对应的lang文档

依据更新前后不同版本 lang 文档的变动：
    + 移除旧版本中原文产生变更/移除的部分，即可生成一个临时的sync版本，以便兼容
    + 搜索新版本中原文产生变更/追加的部分，即可生成一个临时的diff-report，用于制作新版本变更部分的翻译

译者只需要在生成的 diff 文件中，完成翻译后将其merge回sync版本之中，即可完成变更。

该脚本理论上能兼容任何语言的翻译制作，只要脚本中python用于处理文本的utf-8 codec能够支持

## [JUST-IDEA] Translation/Test Check-up Tool
基于 debug-tools 已经提供的基础功能
定义行为集，将同类信息展示在同一个母页面中
定义子 View，展示游戏中的子页面（带有UI）
允许修改翻译，临时重载
debug-tools 自身环境始终有点问题跑不通，暂未进行更多尝试

#### process 参数
定义 process 来自动执行脚本

#### fetch 参数
+ source 源，原始英文文本对应的git项目

#### merge 参数
+ append
+ compatible

# 已弃用

### [HISTORY-IDEA] HISTORY Compatible Support

对于一些改动不大的小版本，mod版本可以与游戏本体不完全对应。新版的翻译理论上可以完全/部分兼容更早的游戏版本

在主体译制完成后，理论上需要将变更同步追溯到更早的只有对翻译的修正，否则由于情景变化部分新内容可能并不合适，应该直接使用其对应的版本，而这一点可以直接在历史release中获取

因此这一点实际上没有特别支持的必要；尽管如此，为防万一 waywardVersion 还是尽量保持了非必要不随本体更新追加。
