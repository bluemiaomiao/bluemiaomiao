---
title: JavaFX开发指南
filename: javafx-dev-guide.md
tags: ['JavaFX', 'GUI', '桌面开发']
category: 桌面开发
description: '本文摘要: JavaFX是Oracle于2008年推出的新一代GUI应用开发框架, 支持Webview, 支持更丰富的控件以及先进的编程模型。'
top: false
date: 2021-02-03 13:54:46
---

# 一、概述

Sun公司已于2008年12月05日发布了JavaFX技术的正式版该产品于2007年5月在JavaOne大会上首次对外公布。JavaFX技术主要应用于创建Rich Internet Applications（[RIAs](https://baike.baidu.com/item/RIAs)）。JavaFX技术有着良好的前景，包括可以直接调用Java API的能力。因为 JavaFX Script是静态类型，它同样具有结构化代码、重用性和封装性，如包、类、继承和单独编译和发布单元，这些特性使得使用JavaFX技术创建和管理大型程序变为可能。

使用IDEA构建Java应用时需要安装**JavaFX Runtime for Plugins**。 如果使用JDK11及以上版本可能需要单独导入JavaFX，因为新版本JDK不再内置JavaFX。JavaFX在今天这个JavaScript盛行的时代并没有过时, 国内使用JavaFX技术很少是因为大部分系统并没有很高的软件复杂度, 所以一般采用Web方式构建应用。接下来本文都是基于JDK 8展开叙述。

JavaFX的SDK都在`javafx.*`下存放, `Stage`表示一个窗口, 调用`show()`方法显示界面，具体代码如下: 

```java
import javafx.application.Application;
import javafx.stage.Stage;

public class Main extends Application {

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) {
        primaryStage.setTitle("HelloWorld");
        primaryStage.show();
    }
}
```

`launch()`方法是`Application`类中的静态方法, 支持传入一个启动类的Class对象, 这样可以将启动方法与`main`方法剥离:

```java
// Bootstrap.java
import javafx.application.Application;

public class Bootstrap {
    public static void main(String[] args) {
        Application.launch(App.class, args);
    }
}
```

```java
// App.java
import javafx.stage.Stage;

public class App extends Application {
    @Override
    public void start(Stage s) {
        s.setTitle("HelloWorld");
        s.show();
    }
}
```

# 二、生命周期

JavaFX提供了`init()`、`start()`、`stop()`生命周期钩子方法，在`start()`运行之前执行`init()`方法, 之后执行`stop()`方法。与其他的GUI框架设计方式类似, JavaFX使用了主线程+UI线程的方式, 所有的组件全部放到UI线程中:

```java
import javafx.application.Application;
import javafx.stage.Stage;

public class Main extends Application {

    public static void main(String[] args) {
        System.out.println("main() -> " + Thread.currentThread().getName());
        launch(args);
    }

    @Override
    public void init() throws Exception {
        System.out.println("init() -> " + Thread.currentThread().getName());
    }

    @Override
    public void stop() throws Exception {
        System.out.println("stop() -> " + Thread.currentThread().getName());
    }

    @Override
    public void start(Stage primaryStage) {
        primaryStage.setTitle("HelloWorld");
        primaryStage.show();
        System.out.println("start() -> " + Thread.currentThread().getName());
    }
}
```

```
main() -> main
init() -> JavaFX-Launcher
start() -> JavaFX Application Thread   // 这是UI线程
stop() -> JavaFX Application Thread
```

# 三、Stage窗口

`Stage`是一个窗口类, 在`start()`方法中JavaFX会提供一个`Stage`对象, 如果不想用这个对象, 那么可以创建一个新的`Stage`对象:

```java
Stage s = new Stage();
```

`Stage`提供了一些常用的方法:

- `s.setTitle(Stirng s)`: 设置窗口标题

- `s.getIcons().add(new Image(String uri))`: 设置窗口图标

- `s.setIconified(boolean b)`: 设置最小化

- `s.setMaximized(boolean b)`: 设置最大化

- `s.show()`: 显示窗口

- `s.close()`: 关闭窗口

- `s.setHeight(double d)`: 设置高度, `s.setMaxHeight(double d)`设置最大高度, `s.setMinHeight(double d)`设置最小高度, 使用`s.getHeight()`获取高度

- `s.setWidth(double i)`: 设置宽度, `s.setMaxWidth(double d)`设置最大宽度, `s.setMinWidth(double d)`设置最小宽度, 使用`s.getWidth()`获取宽度

- `s.setResizable(boolean b)`: 设置是否可以调整大小

-  动态获取宽高:

  ```java
  s.heightProperty().addListener(new ChangeListener<Number>() {
    @Override
    public void changed(ObservableValue<? extends Number> observable, Number oldValue, Number newValue) {
      System.out.println("oldValue:" + oldValue + ", newValue:" + newValue);
    }
  });
  ```

  其他属性的动态监听也是以`xxxProperty`的形式提供。

- 窗口全屏:

  ```java
  s.setScene(new Scene(new Group()));
  s.setFullScreen(true);
  ```

- `s.setOpacity(double d)`: 设置透明度, 范围是0~1

-  `s.setAlwaysOnTop(boolean b)`: 设置窗口置顶

-  `s.setX(double d)`用来设置x轴位置, `s.setY(double d)`用来设置y轴位置, 坐标原点是屏幕左上角

- `s.setInitSytle(StageStyle ss)`: 设置窗口样式

- `s.setModality(Modality mod)`: 设置模态模式

  - `Modality.APPLICATION_MODAL`: 应用模态
  - `Modality.WINDOW_MODAL`: 窗口模态, 需要通过`s.initOwner(Stage s)`来设置父窗口

# 四、Platform工具类

`Platform`是平台工具类, 提供了如下方法:

- `Platform.setImplicitExit(boolean b)`: 设置是否隐式退出,  用户点击按钮后关闭界面, 但是后台保持运行, `Platform.setImplicitExit()`用于获取
- `Platform.accessibilityActiveProperty()`: 是否开启辅助功能, `Platform.isAccessibilityActive()`获取设定的值
- `Platform.exit()`: 退出JavaFX应用, 包括Java虚拟机
- `Platform.isFxApplicationThread()`: 是否为JavaFX的UI线程
- `Platform.isSupported(ConditionalFeature feature)`: 检测是否支持特定功能
- `Platform.runLater(Runnable runnable)`: 在一个随机的未来时间运行某个任务, 不要执行某些类似于下载等重型任务

# 五、Screen工具类

`Screen`是屏幕类, JavaFX将屏幕分为全部区域和可视区域, 并且分别通过`getBounds`和`getVisualBounds`返回`Rectangle2D`对象或者通过`getDpi()`获取DPI。在获取屏幕区域的时候, 应该先获取到所有的屏幕集合, 因为可能存在不止一块屏幕:

- `Screen.getPrimary()`: 获取主屏幕
- `Screen.getScreens()`: 获取屏幕集合
- `Screen.getScreensForRectangle(double x, double y, double width, double height)`: 自定义一个矩形区域, 返回在这个区域内的屏幕, 相当于过滤掉比该区域大的屏幕
- `Screen.getScreensForRectangle(Rectangle2D 2d)`: 同上

获取到`Screen`对象之后就可以通过如下方法获取屏幕信息:

- `getBounds()`: 获取屏幕全部区域
- `getVisualBounds()`: 获取除去顶部栏或者任务栏的可视区域
- `getDpi()`: 获取屏幕DPI

获取到矩形区域后, 就可以进一步得到图形信息:

- `getMaxX()`、`getMinX()`
- `getMaxY()`、`getMinY()`
- `getWidth()`、`getHeight()`

# 六、Scene类











