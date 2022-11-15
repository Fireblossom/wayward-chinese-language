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
+ milestone 往事

# 工具脚本

以下部分当前仅为一些想法，会在有条件时再考虑实现

## [JUST-IDEA] 繁体中文生成

可以使用 python 的 zhconv 项目来自动进行简繁转换，目标繁体可设置为 zh-tw

## [JUST-IDEA] Version Update Tool

在游戏更新后，原始的英文文本也会在[GITHUB:WaywardGame/english-language](https://github.com/WaywardGame/english-language)中同步更新，此时需要对文本变更部分进行更补。

此工具用于在大版本更新后原英文产生大量变更时辅助更新，也可在翻译未完成时，生成临时的中英混杂的文本

### 原理 & 机制 & 功能

由于中文文本是与英文文本几乎逐行对照的，因此可以利用 git 的 diff 来确认哪些英文文本产生了变动

对于变动的内容，以与 Git-diff 相同的规则生成一份单独的文件，用于新版本翻译的修正

译者只需要在生成的 diff 文件中，以约定格式追加翻译内容即可

最后执行 language-merge 操作，脚本会检查 diff 内容，对 add 的部分，使用翻译内容替换英文文本后，合并到 chinese-language 中
+ [特殊] 如果未进行翻译，则会只会删除冲突中的旧版翻译，此时游戏运行时会找不到对应的翻译文本，从而转用原始的英文文本
+ [特殊] 如果翻译内容处标记 append，则会在 merge 时将原始英文追加到新版翻译内容之后。在没有新版的翻译但存在旧版的可用翻译项时，也会将原始英文追加后保留。这一选项可以在游戏更新后立刻生成 WIP 状态的翻译版本，从而在游戏更新到完成翻译期间也能提供一个部分汉化的中间翻译版本

只要保证翻译后文本是与英文文本是逐行对照的，该脚本理论上也可辅助翻译其他语言

### [JUST-IDEA] Compatible Support

对于一些改动不大的小版本，mod版本可以与游戏本体不完全对应。新版的翻译也能完全/部分兼容更早的游戏版本

需注意，仅当不同版本下 dictionaries 中同 Variable 对应的翻译并没有产生冲突的表意变更时，才能支持兼容模式，否则旧版本会产生大量的翻译错误，不如彻底不兼容

在 version update tool 执行 language-merge 时，追加 -compatible 指令即可启用兼容模式输出，启用后脚本会将 diff 内容中旧版删除掉的部分以 extends 的模式提取到 lang\compatible 下，并保留原始翻译，来实现兼容

## [JUST-IDEA] Translation/Test Check-up Tool
基于 debug-tools 已经提供的基础功能
定义行为集，将同类信息展示在同一个母页面中
定义子 View，展示游戏中的子页面（带有UI）
允许修改翻译，临时重载

#### process 参数
定义 process 来自动执行脚本

#### fetch 参数
+ source 源，原始英文文本对应的git项目

#### merge 参数
+ append
+ compatible
