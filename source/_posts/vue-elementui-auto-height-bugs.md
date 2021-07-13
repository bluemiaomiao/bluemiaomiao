---
title: ElementUI在Vue中表格高度自适应
tags: ['ElementUI', 'Vue.js', '自适应']
date: 2021-01-28 19:37:58
category: 前端
description: '本文摘要: 如果你在构建管理后台，菜单栏横向摆放到整个View的顶部，下方是搜索框一些组件，然后最下面是表格来呈现数据，那么，当缩放浏览器窗口的时候，需要实现表格组件Table的高度自适应。'
top: false
filename: vue-elementui-auto-height-bugs.md
---

如果你在构建管理后台，菜单栏横向摆放到整个View的顶部，下方是搜索框一些组件，然后最下面是表格来呈现数据，那么，当缩放浏览器窗口的时候，需要实现表格组件Table的高度自适应。

你可以通过如下方法实现：

```javascript
setTimeout(() => {
    this.customTableHeight = window.innerHeight - this.$refs.table.$el.offsetTop;
}, 100);
```

然后将customTableHeight绑定到表格组件上：

```javascript
:height="customTableHeight" ref="table"
```

当然不要忘记在data中声明该变量。

