# Wayward 中文补丁

友情提醒
+ 存疑待定项外的所有文本均已汉化完毕，后续视个人情况可能会更新增补与修正
+ 关于存疑待定项等更多信息请见 WORK-LIST
+ 将来如需自力更生，可参考 CONTRIBUTING 中的说明

---

此外请注意，此 mod 主体是基于游戏官方文本重新译制适配的，并非只是修改版本号而来的临时性兼容 mod，相较前几者在各方面均存在大量增删等差异。
+ 由于游戏本体的文本也已经产生了很大变化，汉化时对之前的几个模组仅在部分用词上保持了一致
+ 特别注意，为便于脚本工具使用，格式上当前版本已经不再严格与原文本逐行对应，且未翻译的文本将不会复制进汉化文本中

## 汉化范围

官方内容
+ 游戏本体 <更新至 2.13.1-beta 版本> <变更已经校对完成，但当前较2.12中的新增项大部分未完成汉化>
+ 内置 mod [Starter Quest] <更新至 2.13.1-beta 版本>

创意工坊中的部分 mod <均更新至 2.13.1-beta 版本>
+ [debug tools], [balancing tools], [tars], [oddmagicks]

## 使用

安装后在设置选项[Options]中，将语言[Language]选为简体中文或繁体中文即可。

[WIP 暂时并未提供繁体支持]需要注意，繁体中文是通过将简体中文进行简繁转换自动获得，并未经过人工校对可能会存在谬误，建议尽量使用简体中文游玩。

由于语言包内部格式可能存在差异，不建议在更早版本中使用，否则可能会使汉化文本产生缺失、错误或混乱

# CONTRIBUTING

如需译制材料等其他参考信息，请在本地文件中打开CONTRIBUTING.md，或在 GITHUB 中查看[GITHUB:wayward-chinese-language/CONTRIBUTING.md](https://github.com/PlotNarrater/wayward-chinese-language/blob/master/CONTRIBUTING.md)

此外，提供了部分更新/比对的脚本工具，但脚本工具本身并未提供GUI或API，如有需求需有python基础并自行参照注释文档使用。更多相关信息也请在CONTRIBUTING.md中查看

# WORK-LIST

## 未完成内容

+ 可能有极少数文本未找到游戏内对应的内容，因难以翻译而有意遗留

## 保留项

以下部分会保留原文，不进行翻译
+ 部分错误信息、专有名词翻译后反而会令人迷惑
+ Input 按键名，名称与键盘标识可直接对应，且由于样式没有特殊适配，翻译后游戏效果很差
+ 更新日志/新闻等部分从游戏官网在线获取的内容，文字量较大且无法通过 mod 进行替换
+ 少数文本，由于中文字符存在排版、大小等显示问题（如存档导出处的单字单行），且用词较为常见对游戏影响极小，未曾修改。该部分如需汉化，需要官方优化游戏内部分基础组件在中文下的表现后才可进行

## 存疑项

某些项由于各种原因暂未翻译，或在中文后以备注形式保留了部分原文。具体列表请在 CONTRIBUTING.md / [GITHUB:wayward-chinese-language/CONTRIBUTING.md](https://github.com/PlotNarrater/wayward-chinese-language/blob/master/CONTRIBUTING.md) 中查看

此部分内容如果能提供令人信服的改良或见解，可以在 Steam 或 Github 上留言讨论，以帮助优化翻译效果
