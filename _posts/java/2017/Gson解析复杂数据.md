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

## 对象嵌套
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
2. 我们可以使用默认的 Gson 实现，在本例中，Author 类与 Author 的 json 字符串是一一对应的，因此，这种实现完全没问题。
3. 我们还可以实现一个 AuthorDeserializer 来处理 author 字符串的解析问题。

这里我们使用第二种方式，这种方式的改动最小：

JsonDeserializer 的 deserialize() 方法提供了一个 JsonDeserializationContext 对象，这个对象是基于 Gson 的默认机制，我们可以选择性的将某些对象的反序列化委托给这个对象。JsonDeserializationContext 会解析 JsonElement 并返回对应的对象实例:

```java
  Author author = jsonDeserializationContext.deserialize(jsonElement, Author.class);
```

如上例所示，当遇到有 Author 类的解析需求时，jsonDeserializationContext 会去查找用来解析 Author 的 JsonDeserializer，如果有自定义的 JsonDeserializer 被注册过，那么就用自定义的 JsonDeserializer 来解析 Author，如果没有找到自定义的 JsonDeserializer，那就按照 Gson 的默认机制来解析 Author。下面的代码中，我们没有自定义 Author 的 JsonDeserializer，所以 Gson 会自己来处理 Author：

```java
import java.lang.reflect.Type;

import com.google.gson.JsonArray;
import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;

public class BookDeserializer implements JsonDeserializer<Book> {

  @Override
  public Book deserialize(final JsonElement json, final Type typeOfT, final JsonDeserializationContext context)
      throws JsonParseException {
   final JsonObject jsonObject = json.getAsJsonObject();

    final String title = jsonObject.get("title").getAsString();
    final String isbn10 = jsonObject.get("isbn-10").getAsString();
    final String isbn13 = jsonObject.get("isbn-13").getAsString();

    // 委托给 Gson 的 context 来处理
    Author[] authors = context.deserialize(jsonObject.get("authors"), Author[].class);

    final Book book = new Book();
    book.setTitle(title);
    book.setIsbn10(isbn10);
    book.setIsbn13(isbn13);
    book.setAuthors(authors);
    return book;
  }
}
```

除了上面的方式，我们同样可以自定义一个 ArthurDeserialiser 来解析 Author：
```java
import java.lang.reflect.Type;

import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;

public class AuthorDeserializer implements JsonDeserializer {

  @Override
  public Author deserialize(final JsonElement json, final Type typeOfT, final JsonDeserializationContext context)
      throws JsonParseException {
    final JsonObject jsonObject = json.getAsJsonObject();

    final Author author = new Author();
    author.setId(jsonObject.get("id").getAsInt());
    author.setName(jsonObject.get("name").getAsString());
    return author;
  }
}
```

为了使用 ArthurDeserialiser，同样要用到 GsonBuilder：

```java
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

public class Main {

  public static void main(final String[] args) throws IOException {
    // Configure GSON
    final GsonBuilder gsonBuilder = new GsonBuilder();
    gsonBuilder.registerTypeAdapter(Book.class, new BookDeserializer());
    gsonBuilder.registerTypeAdapter(Author.class, new AuthorDeserializer());
    final Gson gson = gsonBuilder.create();

    // Read the JSON data
    try (Reader reader = new InputStreamReader(Main.class.getResourceAsStream("/part2/sample.json"), "UTF-8")) {

      // Parse JSON to Java
      final Book book = gson.fromJson(reader, Book.class);
      System.out.println(book);
    }
  }
}
```
相比委托的方式，自定义 AuthorDeserializer 就根本不需要修改 BookDeserializer 任何代码，Gson 帮你处理了所有的问题。

## 对象引用
考虑下面的 json 文本：
```javascript
{
  'authors': [
    {
      'id': 1,
      'name': 'Joshua Bloch'
    },
    {
      'id': 2,
      'name': 'Neal Gafter'
    }
  ],
  'books': [
    {
      'title': 'Java Puzzlers: Traps, Pitfalls, and Corner Cases',
      'isbn': '032133678X',
      'authors':[1, 2]
    },
    {
      'title': 'Effective Java (2nd Edition)',
      'isbn': '0321356683',
      'authors':[1]
    }
  ]
}
```

这个 json 对象包含两个 book，两个 author，每本书都通过 author 的id 关联到 author，因此，每个 book 的 author 值都只是一个 id 而已。这种结果在网络接口里面非常常见，通过共用对象减少重复定义来减小响应的大小。

这又给解析 json 带来新的挑战，我们需要将 book 和 author 对象组合在一起，但是在解析 json
文本的时候，是以类似树的路径解析的，在解析到 book 的时候，我们只能看到 author 的 id，此时具体的 author 信息却在另一个分支上，在当前的 context 中无法找到所需要的 author。

有几种方法可以处理这个问题：

1. 第一个方案，分两段解析。第一段：按照 json 的结构将 json 文本解析成对应的 java 对象，此时，每个 book 对象都包含一个 id 的数组。第二段：直接在得到的 java 对象中，将 author 对象关联到 book 对象。这种方式的有点就是提供了最大的扩展性，不过缺点也是非常明显的，这种方式需要额外的一组辅助 java 类来表示对应的 json 文本结构，最后在转换为满足应用需求的 java 对象（即我们定义的 model）。在本例中，我们的 model 只有两个类： Book 与 Author。但是使用分段解析的方式，我们还需要额外定义一个 Book 和 Author，结果总共就有 4 个类了。在本例中还说得过去，对于那些也有几十上百的 model 来说，那就相当复杂了。
2. 另一个方案是给 BookDeserialiser 传递所有的 author 对象集合，当 BookDeserialiser 在解析到 Author 属性的时候，直接通过 id 从 author 集合中取得对应的 Author 对象。这样就省略了中间步骤以及额外的对象定义。
这种方式看起来听好，不过这要求 BookDeserialiser 和 AuthorDeserialiser 共享同一个对象集合。当获取 author 的是偶，BookDeserialiser 需要去访问这个共享对象，而不是像我们先前那样直接从 JsonDeserializationContext 中得到。这样就导致了好几处的改动，包括 BookDeserialiser，AuthorDeserialiser 以及 main 方法。
3. 第三种方案是 AuthorDeserialiser 缓存解析得到的 author 集合，当后面需要通过 id 得到具体 Author 对象的时候，直接返回缓存值。这个方案的好处是通过 JsonDeserializationContext 来实现对象的获取，并且对其他部分都是透明的。缺点就是增加了 AuthorDeserialiser 的复杂度，需要修改 AuthorDeserialiser 来处理缓存。

上述方案都有利有弊，可以针对不同的情况，权衡使用。后文以第三种方案来实现，以避免过多的改动。

## Observation

原理上讲，相较于后两种方案，第一种方案提供了更好的关注点分离，我们可以在外层的 Data 类中实现装配。不过第一种方案的改动太大，这一点前面也说过。做到影响面最小，是我们的目标，也是选用第三种方案的主要原因。

json 对象包含两个数组，因此我们需要一个新的类来反映这种结。

```java
public class Data {

  private Author[] authors;
  private Book[] books;
}
```

这两个属性的顺序决定了两者的解析顺序，不过在我们的实现中，解析顺序无关紧要，随便哪个属性先解析都可以，具体见后文。

AuthorDeserialiser 需要先修改来缓存 author 集合：

```java
import java.lang.reflect.Type;
import java.util.HashMap;
import java.util.Map;

import com.google.gson.JsonDeserializationContext;
import com.google.gson.JsonDeserializer;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParseException;
import com.google.gson.JsonPrimitive;

public class AuthorDeserializer implements JsonDeserializer<Author> {

  private final ThreadLocal<Map<Integer, Author>> cache = new ThreadLocal<Map<Integer, Author>>() {
    @Override
    protected Map<Integer, Author> initialValue() {
      return new HashMap<>();
    }
  };

  @Override
  public Author deserialize(final JsonElement json, final Type typeOfT, final JsonDeserializationContext context)
      throws JsonParseException {

    // Only the ID is available
    if (json.isJsonPrimitive()) {
      final JsonPrimitive primitive = json.getAsJsonPrimitive();
      return getOrCreate(primitive.getAsInt());
    }

    // The whole object is available
    if (json.isJsonObject()) {
      final JsonObject jsonObject = json.getAsJsonObject();

      final Author author = getOrCreate(jsonObject.get("id").getAsInt());
      author.setName(jsonObject.get("name").getAsString());
      return author;
    }

    throw new JsonParseException("Unexpected JSON type: " + json.getClass().getSimpleName());
  }

  private Author getOrCreate(final int id) {
    Author author = cache.get().get(id);
    if (author == null) {
      author = new Author();
      author.setId(id);
      cache.get().put(id, author);
    }
    return author;
  }
}
```

我们来逐一看看：

author 集合缓存在下面的对象中：

```java
private final ThreadLocal<Map<Integer, Author>> cache = new ThreadLocal<Map<Integer, Author>>() {
  @Override
  protected Map<Integer, Author> initialValue() {
    return new HashMap<>();
  }
};
```

本实现使用 Map<String, Object> 作为缓存机制，并保存在 ThreadLocal 中，从而进行线程隔离。当然，可是使用其他更好的缓存方案，这个不关键。
