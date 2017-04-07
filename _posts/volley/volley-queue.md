## 各种队列

private final Map<String, Queue<Request<?>>> mWaitingRequests = new HashMap<String, Queue<Request<?>>>();
private final Set<Request<?>> mCurrentRequests = new HashSet<Request<?>>();
private final PriorityBlockingQueue<Request<?>> mCacheQueue = new PriorityBlockingQueue<Request<?>>();
private final PriorityBlockingQueue<Request<?>> mNetworkQueue = new PriorityBlockingQueue<Request<?>>();

同样的请求也可能存在多次


## Request

@Override
public int compareTo(Request<T> other) {
    Priority left = this.getPriority();
    Priority right = other.getPriority();

    // High-priority requests are "lesser" so they are sorted to the front.
    // Equal priorities are sorted by sequence number to provide FIFO ordering.
    return left == right ?
            this.mSequence - other.mSequence :
            right.ordinal() - left.ordinal();
}

优先级的权重更高，其次按照序列号来排列。
