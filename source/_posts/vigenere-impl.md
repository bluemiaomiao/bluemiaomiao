---
title: 密码学之维吉尼亚加解密Java实现
filename: vigenere-impl.md
tags: ['密码学', '逆向破解']
category: '一些算法'
description: '本文摘要: 维吉尼亚密码（又译维热纳尔密码）是使用一系列凯撒密码组成密码字母表的加密算法，属于多表密码的一种简单形式。'
top: false
date: 2021-03-24 15:22:21
---

维吉尼亚密码（又译维热纳尔密码）是使用一系列凯撒密码组成密码字母表的加密算法，属于多表密码的一种简单形式。维吉尼亚密码曾被多次发明，具体关于该密码策略的介绍可以参考 [百度百科上关于维吉尼亚密码的介绍](https://baike.baidu.com/item/%E7%BB%B4%E5%90%89%E5%B0%BC%E4%BA%9A%E5%AF%86%E7%A0%81) 。


维吉尼亚密码的基本原理就是构建一个26x26的字母矩阵，然后给出秘钥还有加密的文字，然后进行如下处理:

- 判断秘钥长度是否与当前给出的字符串的长度相同或者大于当前字符串的长度, 一般情况下, 秘钥的长度都会小于待加密字符串的长度。

- 如果秘钥长度小于待加密字符串，那么就将秘钥的长度不断重复填充, 直到和待加密字符串长度相同

- 使用两个指针一依次扫描秘钥和待加密字符串，将秘钥产生的字符作为行，将待加密字符串产生的字符作为列，在26x26的字符矩阵中找出对应的字符就是加密后的字符

接下来我们构建出字符矩阵：

```java
//{'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'},
//{'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a'},
//{'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b'},
//{'d', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c'},
//{'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd'},
//{'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e'},
//{'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f'},
//{'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g'},
//{'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'},
//{'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i'},
//{'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'},
//{'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k'},
//{'m', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l'},
//{'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm'},
//{'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n'},
//{'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o'},
//{'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p'},
//{'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q'},
//{'s', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r'},
//{'t', 'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's'},
//{'u', 'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't'},
//{'v', 'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u'},
//{'w', 'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v'},
//{'x', 'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w'},
//{'y', 'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x'},
//{'z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y'},
```

我们当然可以使用查表的方法进行查找，但是这样代码中就会要包含很多字符。ASCII字符可以被转换为数字，通过计算的方式不仅效率高而且代码也会变得简洁:

```java
public String dealK(String str) {
	String K = this.salt.toUpperCase();
	StringBuilder sb = new StringBuilder(K);
	String key = "";
	if (sb.length() != str.length()) {
		if (sb.length() < str.length()) {
			while (sb.length() < str.length()) {
				sb.append(K);
			}
		}
		key = sb.substring(0, str.length());
	}
	return key;
}
```

在代码中我们定义alpha作为字母表，定义salt作为用户设置的秘钥: 

```java
private static final String alpha = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";
private String salt;
```

然后实现对应的加密算法：

```java
// P是待加密字符串
public String encrypt(String P) {
	P = P.toUpperCase();
	String K = this.dealK(P);
	int len = K.length();
	StringBuilder sb = new StringBuilder();
	for (int i = 0; i < len; i++) {
		char c = P.charAt(i);
		if (c > 90 || c < 65) {
			sb.append(c);
			continue;
		}

		int row = alpha.indexOf(K.charAt(i));
		int col = alpha.indexOf(P.charAt(i));
		int index = (row + col) % 26;
		sb.append(alpha.charAt(index));
	}
	return sb.toString().toLowerCase();
}
```

与之对应的解密算法也是查表的方式：

```java
// C是密文字符串
public String decrypt(String C) {
	C = C.toUpperCase();
	String K = this.dealK(C);
	int len = K.length();
	StringBuilder sb = new StringBuilder();
	for (int i = 0; i < len; i++) {
		char c = C.charAt(i);

		if (c > 90 || c < 65) {
			sb.append(c);
			continue;
		}

		int row = alpha.indexOf(K.charAt(i));
		int col = alpha.indexOf(C.charAt(i));
		int index;
		if (row > col) {
			index = col + 26 - row;
		} else {
			index = col - row;
		}
		sb.append(alpha.charAt(index));
	}
	return sb.toString().toLowerCase();
}
```

至此，维吉尼亚算法就实现完了，这个加密策略已经被破解了，所以工作中就不要用了。

