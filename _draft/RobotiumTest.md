# Robotium 自动化测试

## 一、Setup
Android Studio环境下，在所要测试的Module的build.gradle文件下添加，
> compile 'com.jayway.android.robotium:robotium-solo:5.4.1'

然后Sync下。

## 二、Start
Robotium即是对Instrumentation框架方法的封装，所以使用之前需要继承测试类，重写构造器，setUp()和tearDown()方法。

    public class SplashActivityTest extends ActivityInstrumentationTestCase2 {

        private Solo solo;

        public SplashActivityTest() throws ClassNotFoundException {
            super(SplashActivity.class);
        }

        @Override
        public void setUp() throws Exception {
            super.setUp();
            solo = new Solo(getInstrumentation());
            getActivity();
        }

        @Override
        public void tearDown() throws Exception {
            solo.finishOpenedActivities();
            super.tearDown();
        }
    }

其中继承的是ActivityInstrumentationTestCase2测试类。ActivityInstrumentationTestCase2测试类主要用于跨Activity的测试。（测试类的关系和架构见附页1）

其中
`solo = new Solo(getInstrumentation());`

`solo.finishOpenedActivities();`是Robotium框架独有的。

测试方法必须是public的，且以test开头。这是因为用的是Junit3框架。

`public void testRun() {}`


## 三、Use
我们所会用到的API主要来自于四个部分：

- Robotium框架核心类Solo
- Instrumentation框架下的ActivityInstrumentationTestCase2类
- unit3下的断言方法
- UI组件的getXX或findXX方法

这里我们只单独简单说明Solo类的API。

Solo类是Robotium中核心类，几乎所有的测试方法都是调用它的方法实现。

#### 1.getXX() 匹配方法

一般使用getView(int id)，getText(String text)匹配想要操作的组件，如果匹配不到，还可以尝试getButton()，getImage()等

// getCurrentActivity()方法返回的是界面显示的Activity。

#### 2.action() 操作方法

- clickOnView()，clickOnText()
- clearEditText()，enterText()
- clickInList()，clickInRecyclerView()
- scrollDown()，scrollViewToSide()（如果是ListView等，这里不推荐使用，不如直接使用moveTo等方法）
- goBack()

#### 3.ssert()/search() 断言方法

- assert：只有solo. assertCurrentActivity() 方法
- search()返回布尔值，用于逻辑判断，断言。
- searchXXX()，waitXXX() 与assertEqual() 方法配合。

#### 4.waitXX(，time) 等待方法

waitForActivity()等，返回布尔值。

在time时间内条件成立，立即执行下一步，不一定非要等待time时间。

同时我们可以使用返回false的waitXX方法作为稳定的定时器使用，我常常用waitForEmptyActivityStack()。

三个作用：等待程序响应，逻辑判断，放缓测试速度

备注：waitXX方法的扩展：waitForCondition()用来支持所有判断条件，实例见下：

    solo.waitForCondition(new myCondition(viewGroup), 3000)

    class myCondition implements Condition {

        Object viewGroup;

        myCondition(Object viewGroup) {

            this.viewGroup = viewGroup;
        }

        @Override
        public boolean isSatisfied() {

            return viewGroup != null;
        }
    }

## 四、practice
SplashActivity.java（这里难点主要是对listView或RecyclerView组件的遍历和判断条件的选择）

需求：

1、从启动页进入

2、切换城市，遍历所有城市

3、搜索1-9

4、如果搜索结果返回多个匹配值，遍历所有匹配值。

5、如果进入站点详情，遍历所有路线，点击收藏按钮并取消收藏

6、如果进入线路详情，遍历所有站点，刷新，然后换向后，重复一遍换向前操作。

### 1、从启动页进入
测试进入第一个的界面即我们绑定的界面
public SplashActivityTest() throws ClassNotFoundException {
    super(SplashActivity.class);
}
这里类名是不是这个类无所谓，但构造方法中调用你想要进入的类。

### 2、切换城市，遍历所有城市
由于城市列表是ListView或者RecyclerView，数据对我们是未知的，布局是可变的，我们不能采用直接clickOnText，或者clickOnView进入某个城市。
对于ListView或者RecyclerView解决办法有三种，具体使用看具体情况：

a、通过遍历，获得所有城市集合，然后调用clickOnText。
获得所有城市集合：

    /**
     * 在CityChooseActivity界面内得到城市列表
     *
     * @return 城市列表
     */
    private String[] getCities() {

        solo.clickOnView(solo.getView(R.id.cll_mod_main_tab_mine));
        solo.clickOnView(solo.getView(R.id.cll_row_city));

        if (solo.waitForActivity(CityChooseActivity.class, 3000)) {

            solo.waitForEmptyActivityStack(3000);
            StickyListHeadersListView stickyLv =(StickyListHeadersListView)     solo.getCurrentActivity().findViewById(R.id.cll_city_change_list);

            List cities = new ArrayList();

            for (int i = 3; i < stickyLv.getAdapter().getCount(); i++) {

                City city = (City) stickyLv.getAdapter().getItem(i);

                cities.add(city.getCityName());
            }
            solo.goBack();

            return (String[]) cities.toArray(new String[cities.size()]);
        } else {
            solo.goBack();

            return new String[]{"天津", "北京"};

    }

clickOnText方法有三个特点：

1）特别稳定，一般都能找到相应的view，无论view被包裹多少层。

2）如果text没有显示或者所在Item初始化，方法会使ListView滚动，直到找到该View。

当然可以设置是否滚动查找。

3）由于查找该View的机制或者存在两个以上相同Text的View，默认选择第一个，可以设置选第几个。

但是这里我们使用

`solo.clickOnView(solo.getView(R.id.cll_search_section));`

`solo.clearEditText((EditText) solo.getView(R.id.frame_toolbar_search_query));`

`solo.enterText((EditText) solo.getView(R.id.frame_toolbar_search_query), city);`

`solo.clickInList(1);`

借用程序的功能，同时测试了这个功能。

但是这种方法的缺陷一是，必须首先进入ListView所在的界面，初始化ListrView后，才能得到城市集合，否则只是一个空集合；二是有些组件无法通过遍历获得城市集合。


b、clickInList ()或者clickInRecyclerView()

解决方法1的缺陷，但缺点是：

1）方法内部的限制如果触发事件并没有绑定到Item上，二是item的子View上，可能无法触发事件。

2）方法参数为可见child的index，需要对不同界面进行position到index的转换和组件滚动。

3）如果一个Item有两个监听事件，比如站点详情的收藏，无法触发。

（注意：参数从1开始）

我在对多结果的遍历和线路详情中遍历所有路线使用这种方法，详细使用会在下文中说明。


c、通过给定的组件，通过findLastVisibleItemPosition或者findViewByPosition找到目标View，再找到具体子View，使用clickOnView(targetView);
终极方法（clickOnScreen除外），几乎可以解决所有需求，但是特别麻烦而且不稳定。不稳定在于即使position指的是从0开始的item数，但依然要求在方法执行时该item是可见的，否则出bug。
我在线路详情遍历所有站点，采用这种方法，详细使用会在下文中说明。

### 3、搜索1-9

### 4、如果搜索结果返回多个匹配值，遍历所有匹配值。

由于不同搜索内容返回的结果是不同懂得，需要对搜索结果的处理，同时考虑网络环境不佳，导致无结果返回的情况。

    for (String content : contents) {

        performSearch(content);
        Log.d("TestTab", "查询" + content);

        Log.d("TestTab", "处理返回的结果");
        if (solo.waitForActivity(LineDetailActivity.class, 2000)) {

            Log.d("TestTab", "进入线路详情界面");
            lineModule.run();

            solo.goBack();
            solo.goBack();


        } else if (solo.waitForActivity(StationDetailActivity.class, 2000)) {

            Log.d("TestTab", "进入车站详情界面");
            stationModule.run();

            solo.goBack();
            solo.goBack();


        } else if (solo.searchButton("重试", true)) {

            Log.d("TestTab", "没有返回结果");

            solo.goBack();

            continue;

        } else if (solo.searchText("没有找到合适的线路和车站", true)) {

            Log.d("TestTab", "没有找到合适的线路和车站");

            solo.goBack();

            continue;

        } else if (solo.waitForFragmentById(R.id.cll_fragment_fuzzy)) {

            traversalResults();
            solo.goBack();
        }
    }

这里主要是判断条件的应用。这里需要注意有两点，一是solo.waitForFragmentById()方法，在程序里如果ViewFlipper的机制是呈现的另个ViewGroup时，目标Fragment依然被初始化。那么solo.waitForFragmentById()就无法正常起作用。
二是searchXX方法。这个方法可以穿透封装，找到目标View。但是两个缺点：

+ 由于方法内部是遍历所有View，寻找匹配项，耗时较长。
+ 在ListView等组件中，该方法会自动滚动寻找匹配项，但不会再滚动回原来位置，在调用clickInLine等方法时，需要手动回滚到第一行。

traversalResults()方法，是通过上述第二种遍历ListView的方法遍历。

    /**
     * 遍历返回多个搜索结果的情况
     */
    private void traversalResults() {

        ListView lv = (ListView) solo.getView(R.id.cll_lv, 1);

        solo.scrollListToTop(lv);

        int sum = lv.getAdapter().getCount();
        Log.d("TestTab", "有" + sum + "结果");

        int itemCount = lv.getLastVisiblePosition() - lv.getFirstVisiblePosition() + 1;
        Log.d("TestTab", "可见的Item有 " + itemCount);

        int loops = sum / itemCount;
        int last = sum % itemCount;

        if (sum < itemCount + 1) {

            for (int p = 1; p < sum + 1; p++) {

                solo.clickInList(p);

                toLineOrStation();
                solo.goBack();

            }

        } else {

            for (int i = 0; i < loops + 1; i++) {

                if (i < loops) {

                    for (int m = 1; m < itemCount; m++) {//由于scrollDown()逻辑和遍历条件无关，到itemCount-1便停止遍历

                        solo.clickInList(m);
                        Log.d("TestTab", "搜索结果遍历" + m);

                        toLineOrStation();
                        solo.goBack();

                    }
                    solo.scrollDown();

                } else {

                    for (int n = itemCount - last + 1; n < itemCount + 1; n++) {

                        solo.clickInList(n);

                        toLineOrStation();
                        solo.goBack();

                    }
                }
            }
        }
    }

需要得到三个值item的总数，单页可见Item数，前两者相除的余数，具体逻辑看上面代码。

注意在处理最后一页的逻辑。

最后一个需要注意的地方：

`ListView lv = (ListView) solo.getView(R.id.cll_lv, 1);`

Index为1，这是由于当时可以匹配到两个ListView，选择第二个。

### 5、如果进入站点详情，遍历所有路线，点击收藏按钮并取消收藏

两个步骤，遍历点击每个Item，遍历点击每个收藏按钮

遍历点击每个Item，获得Item总数，屏幕内item数量，前两者相除的商和余数，每次循环通过clickInLine遍历屏幕上的每一个item，循环商加一的次数，最后一次只需要遍历倒数余数个item。

    @Override
    public void run() {

        solo.waitForActivity(StationDetailActivity.class);//保证recyclerView不为空。

        RecyclerView recyclerView = (RecyclerView) solo.getView(R.id.cll_station_detail_list);
    	//找到目标RecyclerView，这样比getCurrentActivity().findViewById()更加有效。

        LinearLayoutManager mLinearLayoutManager = (LinearLayoutManager) recyclerView.getLayoutManager();

        int sum = recyclerView.getAdapter().getItemCount();
        Log.d("TestTab", "共有 " + sum + " 条线路");

        int itemCount = ((LinearLayoutManager) recyclerView.getLayoutManager()).findLastVisibleItemPosition() - ((LinearLayoutManager) recyclerView.getLayoutManager()).findFirstVisibleItemPosition() + 1;//计算显示在屏幕的item的数量

        int loops = sum / itemCount;需要滚动几次
        int last = sum % itemCount;最后一次

        if (sum < itemCount + 1) {

            for (int p = 0; p < sum; p++) {

                clickItem(p);

                clickFavourInStation(mLinearLayoutManager, p);

            }

        } else {

            for (int i = 0; i < loops + 1; i++) {

                if (i < loops) {
                    //保证不点击到返回按钮
                    recyclerView.smoothScrollToPosition(itemCount * i);//由于solo.scrollDown()不稳定，需要稳定的定位

                    for (int m = 0; m < itemCount; m++) {

                        clickItem(m);

                        clickFavourInStation(mLinearLayoutManager, i * itemCount + m);
                    }
                    solo.scrollDown();

                } else {

                    int lastPageItemsCount = ((LinearLayoutManager) recyclerView.getLayoutManager()).findLastVisibleItemPosition() - ((LinearLayoutManager) recyclerView.getLayoutManager()).findFirstVisibleItemPosition() + 1;

                    for (int n = lastPageItemsCount - last, q = 0; n < lastPageItemsCount - 1; n++, q++) {

                        clickItem(n);

                        clickFavourInStation(mLinearLayoutManager, loops * itemCount + q);
                    }
                }
            }
        }
    }

点击收藏按钮并取消收藏：

主要思路是保证该Item可见的情况下，通过findViewByPosition找到目标Item的view，然后再找到处理监听事件的子View，click。

    private void clickFavourInStation(LinearLayoutManager mLinearLayoutManager, int i) {

            Log.d("TestTab", "点击收藏");

            ViewGroup targetGroup = (ViewGroup) mLinearLayoutManager.findViewByPosition(i);

            LineStnView mLineStnView = (LineStnView) targetGroup.getChildAt(1);

            if (mLineStnView.getX() < 0) {
                mLineStnView = (LineStnView) targetGroup.getChildAt(0);
            }

            View v = mLineStnView.findViewById(R.id.fav_view);

            solo.clickOnView(v);

            if (solo.waitForDialogToOpen()) {

                solo.clickOnText("取消收藏");

            } else {

                solo.clickOnView(v);

                solo.waitForDialogToOpen(2000);

                solo.clickOnText("取消收藏");
            }

        }

### 6、如果进入线路详情，遍历所有站点，刷新，然后换向后，重复一遍换向前操作。

主要思路是：通过getView得到list组件，通过组件给定的方法使我们想要选中的目标Item保持在屏幕内，然后findViewByPosition找到目标Item的组件，依次点击。

这里设置一个Flag值用来记录是否已经变向。

    private void traversalAllStat(Boolean flag) {

        solo.waitForEmptyActivityStack(2000);

        RealTimePanelContent content = (RealTimePanelContent) solo.getView(R.id.cll_real_time_panel_content);
        Log.d("TestTab", "获取到RealTimePanelContent的实例");

        LinearLayoutManager mLinearLayoutManager = (LinearLayoutManager) content.getLayoutManager();
        Log.d("TestTab", "获取到LinearLayoutManager的实例");

        int sum = content.getAdapter().getItemCount();//获取站数
        Log.d("TestTab", "获取到车站数" + String.valueOf(sum - 1));

        content.moveToPosition(3);
        solo.waitForEmptyActivityStack(2000);
        Log.d("TestTab", "等待2s到tab移动到左侧");


        int lastPosition = mLinearLayoutManager.findLastVisibleItemPosition();
        Log.d("TestTab", "界面出现的最后一个Item的position" + lastPosition);

        for (int i = 0; i < sum - 1; i++) {

            final ViewGroup viewGroup;
            Log.d("TestTab", "当前position为 " + String.valueOf(i));

            if (i < lastPosition) {

                solo.waitForEmptyActivityStack(1000);

                viewGroup = (ViewGroup) mLinearLayoutManager.findViewByPosition(i);

                if ((!solo.waitForCondition(new myCondition(viewGroup), 3000)) || (!viewGroup.isShown())) {
                    Log.d("TestTab", "viewGroup为null");

                    content.moveToPosition(i);
                    Log.d("TestTab", "由于viewGroup为null，将" + i + "移动到中间");

                    i--;
                    Log.d("TestTab", "保持position位置不变");

                    continue;
                }
                Log.d("TestTab", "viewGroup不为null");

                View viewToClick = viewGroup.findViewById(R.id.cll_apt_station_name);

                if ((!viewToClick.isShown()) || (!solo.waitForView(viewToClick, 1500, true))) {
                //这里反复验证取得View是否为空或者不可见，或者事件未触发
                }

                    Log.d("TestTab", "viewToClick不可见");

                    content.moveToPosition(i);
                    Log.d("TestTab", "viewToClick不可见，将" + i + "移动到中间");

                    i--;
                    Log.d("TestTab", "保持position位置不变");

                    continue;
                }

                solo.clickOnView(viewToClick);
                Log.d("TestTab", "点击到position" + String.valueOf(i));

                if (!solo.waitForDialogToClose(6000)) {

                    Log.d("TestTab", "刷新框没有出现");

                    content.moveToPosition(i);
                    i--;
                    Log.d("TestTab", "保持position位置不变");

                    continue;
                }

                Log.d("TestTab", "点击收藏");
                clickFavourInLine();

                Log.d("TestTab", "点击刷新");
                clickRefresh();


            } else {

                content.moveToPosition(lastPosition);
                Log.d("TestTab", "将" + lastPosition + "移动到中间");

                solo.waitForEmptyActivityStack(2000);
                Log.d("TestTab", "等待2s");

                lastPosition = mLinearLayoutManager.findLastVisibleItemPosition();
                Log.d("TestTab", "改变lastPosition为" + lastPosition);

                viewGroup = (ViewGroup) mLinearLayoutManager.findViewByPosition(i);

                if ((!solo.waitForCondition(new myCondition(viewGroup), 3000)) || (!viewGroup.isShown())) {

                    Log.d("TestTab", "viewGroup为null");

                    content.moveToPosition(i);
                    Log.d("TestTab", "将" + i + "移动到中间");

                    i--;
                    Log.d("TestTab", "保持position位置不变");

                    continue;
                }

                View viewToClick = viewGroup.findViewById(R.id.cll_apt_station_name);

                if (!viewToClick.isShown()) {
                    Log.d("TestTab", "viewToClick不可见");

                    content.moveToPosition(i);
                    Log.d("TestTab", "viewToClick不可见，将" + i + "移动到中间");

                    i--;
                    Log.d("TestTab", "保持position位置不变");

                    continue;
                }

                solo.clickOnView(viewToClick);
                Log.d("TestTab", "点击到position" + String.valueOf(i));

                if (!solo.waitForDialogToOpen(6000)) {

                    Log.d("TestTab", "刷新框没有出现");

                    content.moveToPosition(i);
                    i--;
                    Log.d("TestTab", "保持position位置不变");

                    continue;
                }

                Log.d("TestTab", "点击收藏");
                clickFavourInLine();

                Log.d("TestTab", "点击刷新");
                clickRefresh();
            }

            if (i == sum - 2 && flag) {

                flag = false;
                Log.d("TestTab", "切换标志，不可再换向");

                clickChangeDec();
                Log.d("TestTab", "点击换向");

                Log.d("TestTab", "重新遍历");
                traversalAllStat(flag);
            }

            if (!solo.waitForDialogToClose(60000)) {

                Log.d("TestTab", "刷新失败");
                solo.goBack();
            }
        }
    }

## 五、Caution

1、最稳定最常用的的solo.clickOnView(solo.getView(R.id.xxx));可封装成根据ID进行点击，优先使用。

2、时间控制

速度过慢不符合我们快速测试的需求

速度过快，会导致两个问题，一是前一个动作未响应完（动作本身耗时长或者网络环境不好），后一个动作触发找不到组件；二是并行冲突，比如listView前一动作要求listView向下滑，后一个动作要求向上滑。

解决方法：waitXX方法等待动作完成，如果在规定时间内没有完成

3、界面的作用范围
