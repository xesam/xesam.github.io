本文主要关注所要解析的 JSON 数据与已定义的 java 对象结构不匹配的情况，主要解决方案就是使用 JsonDeserializer 来自定义从 Json 对象到 Java 对象的映射。

http://www.javacreed.com/gson-deserialiser-example/

## 一个简单的例子
有如下 JSON 对象，其表示一本书的基本信息，同时有两个作者。

```javascript
{
  'title':    'Java Puzzlers: Traps, Pitfalls, and Corner Cases',
  'isbn-10':  '032133678X',
  'isbn-13':  '978-0321336781',
  'authors':  ['Joshua Bloch', 'Neal Gafter']
}
```
这个 JSON 对象包含 4 个字段，其中有一个是数组。这些字段表征了一本书的基本信息。
如果我们直接使用 Gson 来解析：

```java
    Book book = new Gson().fromJson(jsonString, Book.class);
```

会发现 'isbn-10' 这种字段表示在 Java 中是不合法的，因为 Java 的变量名中是不允许含有 '-' 符号的。
对于这个例子，我们可以使用 Gson 的 @SerializedName 注解来处理，不过注解也仅限于此，遇到后文的使用情况，注解就无能为力了。
这个时候，就是 JsonDeserializer 派上用场的时候。

假如 Book 类定义如下：

```java
public class Book {

  private String[] authors;
  private String isbn10;
  private String isbn13;
  private String title;

  // 其他方法省略
}
```

这个 Book 也定义有 4 个字段，与 Json 对象的结构基本类似。为了将 Json 解析为 Java 对象，我们需要自定义一个 JsonDeserializer 然后 注册到 GsonBuilder 上，
使用 GsonBuilder 来获取解析用的 Gson 对象。

因此， 我们先创建一个 BookDeserializer，这个 BookDeserializer 负责将 Book 对应的 Json 对象解析为 Java 对象。

```java
    public class BookDeserializer implements JsonDeserializer<Book> {
            
      @Override
      public Book deserialize(final JsonElement jsonElement, final Type typeOfT, final JsonDeserializationContext context)
          throws JsonParseException {
      
        //todo 解析字段
    
        final Book book = new Book();
        book.setTitle(title);
        book.setIsbn10(isbn10);
        book.setIsbn13(isbn13);
        book.setAuthors(authors);
        return book;
      }
    }
```
在实现具体的解析之前，我们先来了解一下涉及到的各个类的含义。JsonDeserializer 需要一个 Type，也就是解析要得到的对象类型，这里当然就是 Book，
同时 deserialize() 方法返回的就是 Book 对象。
Gson 将 Json 对象解析为 JsonElement 的表示，一个 JsonElement 可以是如下的任何一种：

1. JsonPrimitive ：Java 基本类型的包装类，以及 String
2. JsonObject：类比 Js 中 Object 的表示，或者 Java 中的 Map<String, JsonElement>，一个键值对结构。
3. JsonArray：JsonElement 组成的数组，注意：这里是 JsonElement，说明这个数组是混合类型的。
4. JsonNull：值为 null

开始解析（其实这个解析很直观的，Json 里面是什么类型，就按照上面的类型进行对照解析即可），所以， 我们先将 JsonElement 转换为 JsonObject：

```java
    // jsonElement 是 deserialize() 的参数
    final JsonObject jsonObject = jsonElement.getAsJsonObject();
```
对照 Json 定义，然后获取 JsonObject 中的 title。

```java
    final JsonObject jsonObject = jsonElement.getAsJsonObject();
    JsonElement titleElement = jsonObject.get("title")
```
我们知道 titleElement 具体是一个字符串（字符串属于 JsonPrimitive），因为可以直接转换：

```java
    final JsonObject jsonObject = jsonElement.getAsJsonObject();
    JsonElement titleElement = jsonObject.get("title")
    final String title = jsonTitle.getAsString();
```

此时我们得到了 title 值，其他类似：

```java
    public class BookDeserializer implements JsonDeserializer<Book> {
        @Override
        public Book deserialize(JsonElement jsonElement, Type type, JsonDeserializationContext jsonDeserializationContext) throws JsonParseException {
    
            final JsonObject jsonObject = jsonElement.getAsJsonObject();
    
            final JsonElement jsonTitle = jsonObject.get("title");
            final String title = jsonTitle.getAsString();
    
            final String isbn10 = jsonObject.get("isbn-10").getAsString();
            final String isbn13 = jsonObject.get("isbn-13").getAsString();
    
            final JsonArray jsonAuthorsArray = jsonObject.get("authors").getAsJsonArray();
            final String[] authors = new String[jsonAuthorsArray.size()];
            for (int i = 0; i < authors.length; i++) {
                final JsonElement jsonAuthor = jsonAuthorsArray.get(i);
                authors[i] = jsonAuthor.getAsString();
            }
    
            final Book book = new Book();
            book.setTitle(title);
            book.setIsbn10(isbn10);
            book.setIsbn13(isbn13);
            book.setAuthors(authors);
            return book;
        }
    }
```

整体还是很直观的，我们测试一下：
```java
    public static void main(String[] args) {
        GsonBuilder gsonBuilder = new GsonBuilder();
        gsonBuilder.registerTypeAdapter(Book.class, new BookDeserializer());
        Gson gson = gsonBuilder.create();

        Book book = gson.fromJson("{\"title\":\"Java Puzzlers: Traps, Pitfalls, and Corner Cases\",\"isbn-10\":\"032133678X\",\"isbn-13\":\"978-0321336781\",\"authors\":[\"Joshua Bloch\",\"Neal Gafter\"]}", Book.class);
        System.out.println(book);
    }
```
输出结果：

```shell
Book{authors=[Joshua Bloch, Neal Gafter], isbn10='032133678X', isbn13='978-0321336781', title='Java Puzzlers: Traps, Pitfalls, and Corner Cases'}
```

上面，我们使用 GsonBuilder 来注册 BookDeserializer，并创建 Gson 对象。此处得到的 Gson 对象，在遇到需要解析 Book 的时候，就会使用 BookDeserializer 来解析。
比如我们使用

```java
    gson.fromJson(data, Book.class);
```

来解析的时候，大致流程如下：
1. gson 将输入字符串解析为 JsonElement，同时，这一步也会校验 Json 的合法性。
2. 找到对应的 JsonDeserializer 来解析这个 JsonElement，这里就找到了 BookDeserializer。
3. 执行 deserialize() 并传入必要的参数，本例中就是在 deserialize() 将一个 JsonElement 转换为 Book 对象。
4. 将 deserialize() 的解析结果返回给 fromJson() 的调用者。

## 嵌套的对象
在上面的例子中，一本书的作者都只用了一个名字来表示，但是实际情况中，一个作者可能有很多本书，每个作者实际上还有个唯一的 id 来进行区分。结构如下：

```javascript
{
  'title': 'Java Puzzlers: Traps, Pitfalls, and Corner Cases',
  'isbn': '032133678X',
  'authors':[
    {
      'id': 1,
      'name': 'Joshua Bloch'
    },
    {
      'id': 2,
      'name': 'Neal Gafter'
    }
  ]
}
```
此时我们不仅有个 Book 类，还有一个 Author 类：

```java
public class Author{
    long id;
    String name;
}
```

那么问题来了，谁来负责解析这个 author？有几个选择：

1. 我们可以更新 BookDeserializer，同时在其中解析 author 字段。这种方案耦合了 Book 与 Author 的解析，并不推荐。
2. 




