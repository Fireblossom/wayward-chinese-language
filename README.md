# Wayward 中文补丁

请注意，此 mod 并非从之前很早版本的几个汉化模组修改版本号而来，而是个人逐行重译并校对测试了几乎全部文本，且同时支持部分其他模组的汉化

[WIP] 目前物品描述/帮助文档尚未完全完成翻译，如有特别需要可以寻找之前的社区汉化以作参考。物品名、提示信息等其他游戏内文本已经基本完全翻译完成，已经不影响正常进行游戏了。物品描述/帮助文档会在完成后再更新，其他存疑项请见TO-DO-LIST

## 汉化范围

+ 游戏本体 2.12.1 版本
+ 内置mod [Starter Quest] 
+ 官方在创意工坊中发布的部分mod [debug tools], [balancing tools], [tars], [oddmagicks]

## 使用

安装后在设置选项[Options]中，将语言[Language]选为简体中文或繁体中文即可。

[WIP 暂时并未提供繁体支持]需要注意，繁体中文是通过将简体中文进行简繁转换自动获得，可能会存在谬误，建议尽量使用简体中文游玩。

## 历史版本

历史版本及不同版本的更新信息请利用 github 查看

由于语言包内部格式可能存在差异，不建议使用非对应版本的语言包，如果使用可能会导致翻译内容的错误或混乱

mod的版本号为X.X.X.X的格式，其中前三位为翻译制作时所对应的游戏版本，最后一位是翻译文本的版本。前三位的调整仅依据官方英文文本源[GITHUB:WaywardGame/english-language](https://github.com/WaywardGame/english-language)而非游戏本身的更新进行。

# TO-DO-LIST

## 未翻译内容

+ 部分错误信息、专有名词翻译后反而会令人迷惑，这部分直接完全保留在原始状态
+ 所有input内容，按键与键盘标识可以直接对应，且中文无法适配游戏中的特殊显示效果，完全保留在原始状态
+ 更新日志/新闻等部分从游戏官网在线获取的内容，无法通过mod进行替换，所以仍然是原生的英文文本。该部分如需汉化，需要官方提供额外的支持，且内容相较本体更为庞杂
+ 少数文本，由于中文字符存在排版、大小等显示问题（如存档导出处的单字单行），且用词较为常见对游戏影响极小，未曾修改。该部分如需汉化，需要官方优化游戏内部分基础组件在中文下的表现后才可进行
+ 汉化中的部分存疑项未完全/未进行翻译

## 存疑项

对以下某些项如果能够提供令人信服的解释或改良，可以在Steam或Github上留言，以帮助优化翻译效果

+ 部分可能存疑的小段文本，在游戏内进行了部分翻译，并在翻译文本左近以备注形式保留了对应的原始英文

#### 部分文本因未找到在游戏中对照核对的方法，翻译是否得体有待确认

+ action的子项中，各个行为的进阶效果
    + 多个行为中关于技艺提升的表述存在细微差异，应根据实际效果统一意译
    + 屠宰 声望变化的表述存在矛盾的可能
    + 休息 睡觉的周期的表述可能需要根据实际效果，改用意译而非直译

+ category 未找到实际使用场景，字面含义与 group 一项重叠
+ equip 中 Held 类型未找到对应物品

+ somethingInTheWayOf 一类中
    + 不特定场景的几项，有可能因为语法差异产生奇怪的表达，可能需要视实际场景对表述进行微调

#### 部分文本应可改善为更贴合游戏风格的雅译

+ 物品品质quality，游戏中大部分物品工具并不玄幻不适合“稀有史诗传说”的描述，但是原文直译中，优秀杰出的高品质用词区分度不够明显

# Contribute

警告：以下部分为汉化制作的相关信息，可能包含一定的剧透性质内容。

## [WIP] version update tool

在游戏更新后，原始的英文文本也会在[GITHUB:WaywardGame/english-language](https://github.com/WaywardGame/english-language)中同步更新，此时需要对本语言包同步进行更新。

此工具用于在大版本更新后原英文产生大量变更时辅助更新，也可在翻译未完成时，生成临时的中英混杂的文本

### 原理 & 机制 & 功能

由于中文文本是与英文文本几乎逐行对照的，因此可以利用 git 的 diff 来确认哪些英文文本产生了变动

对于变动的内容，以与 Git-diff 相同的规则生成一份单独的文件，用于新版本翻译的修正

译者只需要在生成的 diff 文件中，以约定格式追加翻译内容即可

最后执行 language-merge 操作，脚本会检查 diff 内容，对 add 的部分，使用翻译内容替换英文文本后，合并到 chinese-language 中
+ [特殊] 如果未进行翻译，则会只会删除冲突中的旧版翻译，此时游戏运行时会找不到对应的翻译文本，从而转用原始的英文文本
+ [特殊] 如果翻译内容处标记 append，则会在 merge 时将原始英文追加到新版翻译内容之后。在没有新版的翻译但存在旧版的可用翻译项时，也会将原始英文追加后保留。这一选项可以在游戏更新后立刻生成 WIP 状态的翻译版本，从而在游戏更新到完成翻译期间也能提供一个部分汉化的中间翻译版本

只要保证翻译后文本是与英文文本是逐行对照的，该脚本理论上也可辅助翻译其他语言

### [WIP] Compatible Support

对于一些改动不大的小版本，mod版本可以与游戏本体不完全对应。新版的翻译也能完全/部分兼容更早的游戏版本

需注意，仅当不同版本下 dictionaries 中同 Variable 对应的翻译并没有产生冲突的表意变更时，才能支持兼容模式，否则旧版本会产生大量的翻译错误，不如彻底不兼容

在 version update tool 执行 language-merge 时，追加 -compatible 指令即可启用兼容模式输出，启用后脚本会将 diff 内容中旧版删除掉的部分以 extends 的模式提取到 lang\compatible 下，并保留原始翻译，来实现兼容

## [WIP] translation/test check-up tool
基于 debug-tools 已经提供的基础功能
定义行为集，将同类信息展示在同一个母页面中
定义子 View，展示游戏中的子页面（带有UI）
允许修改翻译，临时重载

### 如何使用

#### process 参数
定义 process 来自动执行脚本

#### fetch 参数
+ source 源，原始英文文本对应的git项目

#### merge 参数
+ append
+ compatible

## [WIP] 繁体中文生成

简繁转换 使用 python 的 zhconv 来自动进行，目标繁体为 zh-tw

## [参考] 特殊词译表

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
+ iron          铁
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


drop will not be marked as used