---
layout: post
title:  "【Android】RecyclerView"
date:   2014-12-02 12:46:04 +0800
categories: android
tag: [android]
---

# RecyclerView

##R ecyclerView简明

RecyclerView 在v7.21+包中，是一个用来展示大量数据的组件，或者说，就是ListView的改善版本（注：现阶段的功能没有ListView完善，因此想完全取代ListView的话并不明智）。
相比ListView，RecyclerView的扩展性更好，因此也更适合与android新曾的组件配合使用，这样使用起来更得心应手。

RecyclerView与ListView的原理差不多，本质上都是以适配器为核心。只不过ListView缓存的是view，viewHolder附着在view上，而RecyclerView缓存的是viewHolder，view包含在viewHolder内。

如果我们将ListViewAdapter稍作修改，也可以实现这种设计：

```java
    abstract class LvAdapter<VH extends LvAdapter.ViewHolder> extends BaseAdapter {
        public class ViewHolder {
            private View view;
            public ViewHolder(View view) {
                this.view = view;
            }
            public View getView() {
                return view;
            }
        }

        @Override
        public int getCount() {
            return 0;
        }

        @Override
        public Object getItem(int position) {
            return null;
        }

        @Override
        public long getItemId(int position) {
            return 0;
        }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            VH vh = getViewHolder();
            onBindViewHolder(vh, position);
            return vh.getView();
        }

        public abstract VH getViewHolder();

        public abstract void onBindViewHolder(VH holder, int position);
    }
```

这样有点不直观，所以更进一步，ListView的Adapter可以更抽象，将数据绑定方法交给viewHolder，这样adapter的工作就更单纯一点.

一个方便的ListViewAdapter可以参考[base-adapter-helper](https://github.com/JoanZapata/base-adapter-helper)


## RecyclerView使用

#### 适配器
既然都是以适配器为核心，因此，只需要写好适配器就行了：

```java
    class RvViewHolder extends RecyclerView.ViewHolder {

        public TextView tv;

        public RvViewHolder(View itemView) {
            super(itemView);
            tv = (TextView) itemView.findViewById(R.id.tv);
        }
    }

    class RvAdapter extends RecyclerView.Adapter<RvViewHolder> {

        Context context;
        String[] items;

        public RvAdapter(Context context, String[] items) {
            this.context = context;
            this.items = items;
        }

        @Override
        public RvViewHolder onCreateViewHolder(ViewGroup parent, int viewType) {
            View view = LayoutInflater.from(parent.getContext()).inflate(R.layout.apt_v7_recycler_view, parent, false);
            return new RvViewHolder(view);
        }

        @Override
        public void onBindViewHolder(RvViewHolder holder, int position) {
            holder.tv.setText(items[position]);
        }

        @Override
        public int getItemCount() {
            return items.length;
        }
    }

    rv.setAdapter(new RvAdapter(this, new String[]{
            "A", "B", "C", "D",
            "A", "B", "C", "D",
            "A", "B", "C", "D",
            "A", "B", "C", "D",
            "A", "B", "C", "D",
            "A", "B", "C", "D",
            "A", "B", "C", "D",
            "A", "B", "C", "D",
            "A", "B", "C", "D",
            "A", "B", "C", "D",
            "A", "B", "C", "D",
            "A", "B", "C", "D",
            "A", "B", "C", "D"
    }));
    LinearLayoutManager linearLayoutManager = new LinearLayoutManager(this);
    linearLayoutManager.setOrientation(LinearLayout.VERTICAL);
    rv.setLayoutManager(linearLayoutManager);
```

#### 布局管理器 与 横向列表

RecyclerView的另一个特点就是布局管理器（LayoutManager），个人觉得的一个比较方便的地方就是，终于可以方便的实现**横向列表**</em>了！布局管理的作用就是负责摆放view以及回收view。
类似的

```java
    int findFirstVisibleItemPosition();
    int findLastVisibleItemPosition();
```

方法也在布局管理器中

#### 设置item动画

```java
    rv.setItemAnimator(ItemAnimator);
```

#### 分割线
由于RecyclerView的布局不固定，因此没有像ListView那样直接设定divider的方式，这些可能需要自己实现。一个简单粗鲁的纵向列表分割线如下：

```java
    rv.addItemDecoration(new RecyclerView.ItemDecoration() {

        Paint paint = new Paint();

        @Override
        public void onDraw(Canvas c, RecyclerView parent, RecyclerView.State state) {
            super.onDraw(c, parent, state);
        }

        @Override
        public void onDrawOver(Canvas c, RecyclerView parent, RecyclerView.State state) {
            super.onDrawOver(c, parent, state);
            for (int i = 0, size = parent.getChildCount(); i < size; i++) {
                View child = parent.getChildAt(i);
                c.drawLine(child.getLeft(), child.getBottom(), child.getRight(), child.getBottom(), paint);
            }
        }

        @Override
        public void getItemOffsets(Rect outRect, View view, RecyclerView parent, RecyclerView.State state) {
            super.getItemOffsets(outRect, view, parent, state);
        }
    });
```

还可以参考：[DividerItemDecoration](https://gist.github.com/alexfu/0f464fc3742f134ccd1e)

#### 绑定事件

RecyclerView 没有 ListView 的 OnItemClick 等方法，所以，类似方法需要自己处理。

1. 可以直接给itemView或者其子view绑定事件，绑定可以在viewHolder中进行事件绑定，也可以在adapter中进行。
不过viewHolder中无法直观获取到原始的Item数据，需要进一步的处理（比如给itemView设置tag）才能实现获取原始数据的目的，所以怎么使用需要自己权衡。

```java
    class RvViewHolder extends RecyclerView.ViewHolder implements View.OnClickListener {

        public TextView tv;

        public RvViewHolder(View itemView) {
            super(itemView);
            tv = (TextView) itemView.findViewById(R.id.tv);
            itemView.setTag(this);
            itemView.setOnClickListener(this);
        }

        @Override
        public void onClick(View v) {
            int vId = v.getId();
            if (vId == R.id.tv) {
                Toast.makeText(itemView.getContext(), getPosition() + "", Toast.LENGTH_SHORT).show();
            }
        }
    }
```

2. 可以使用

```java
    addOnItemTouchListener(RecyclerView.OnItemTouchListener listener)
```

来进行全局处理。当然，缺点就是需要处理事件细节，比较繁琐。

## demo

[demo](http://git.oschina.net/xesam/AndroidLollipop)



