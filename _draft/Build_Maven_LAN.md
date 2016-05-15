# Android Studio下构建Maven私服

## 对Maven的理解

#### Maven仓库的分类

本地Maven仓库和远程Maven仓库（中央仓库，第三方仓库，私服）

#### jcenter和MavenCenter

略

## 搭建Maven私服

#### 一、下载并安装Maven环境

需要注意的是：后面需要修改Settings
setting文件3.0之前在C:\Users\xxx\.m2下，其实AndroidStudio通过JCenter下载的jar即放在这个文件夹下。3.0之后在Maven目录的conf下

#### 二、下载并安装Nexus

安装完后，需要进入系统对应的文件夹下（我的即在nexus-2.11.4-01\bin\jsw\windows-x86-64，不同系统在不同文件夹下），第一次需要依次执行安装，注册Windows服务，开启服务。
以后再使用前只需要开启服务（start-nexus.bat）就OK。

在浏览器中输入:127.0.0.1:8081/nexus，如果正确响应，说明安装成功。

在当前页面输入账户名密码（默认admin/admin123）

登录进去看到已经建立了十几个仓库。

点击工具栏add -> 选择hosted repository，然后填入repository id，和repository name-> 保存，这样就可以建立新的仓库了。

我们都知道引用repository时，需要groupid，artifactId，以及版本号。因此需要一个Group。

点击工具栏add -> 选择repository group，然后填入group id等。

系统默认给我们一个public group，同时我们还可以自建几个group用来管理repository。于是我们采取public group包含自建group的方式，这样团队其他人只需要引用public group，而无需关心Nexus内部是如何组织repository的。

一定要更改settings文件，特别是但不仅仅你更改了Maven的存储目录，建立Nexus需要在maven中添加镜像，具体见下：

    <mirrors>
		<mirror>
			<!--This sends everything else to /public -->
			<id>nexus</id>
			<mirrorOf>*</mirrorOf>
			<url>http://localhost:8081/nexus/content/groups/public/</url>
		</mirror>
	</mirrors>

以及

    <profiles>
		<profile>
			<id>nexus</id>
			<!--Enable snapshots for the built in central repo to direct -->
			<!--all requests to nexus via the mirror -->
			<repositories>
				<repository>
					<id>central</id>
					<url> http://central</url>
					<releases>
						<enabled>true</enabled>
					</releases>
					<snapshots>
						<enabled>true</enabled>
					</snapshots>
				</repository>
			</repositories>
			<pluginRepositories>
				<pluginRepository>
					<id>central</id>
					<url> http://central</url>
					<releases>
						<enabled>true</enabled>
					</releases>
					<snapshots>
						<enabled>true</enabled>
					</snapshots>
				</pluginRepository>
			</pluginRepositories>
		</profile>
	</profiles>

	<!-- activeProfiles | List of profiles that are active for all builds. |
		<activeProfiles> <activeProfile>alwaysActiveProfile</activeProfile> <activeProfile>anotherAlwaysActiveProfile</activeProfile>
		</activeProfiles> -->

	<activeProfiles>
		<!--make the profile active all the time -->
		<activeProfile>nexus</activeProfile>
	</activeProfiles>

原settings文件，会在每一个可能修改的位置添加注释，说明这里可以改什么。非常人性化


#### 三、打包工程并上传至Nexus

两种方式：

1、手动打包和上传

略

2、自动打包和上传（当然包含半自动的，也略）

由于我们是在Android Studio下，因此gradle代替maven势在必行。

网上各种复杂的gradle代码，实际上关键步骤只有：

1）引用maven插件

`apply plugin: 'maven'`

以及

2）

    uploadArchives {

         repositories.mavenDeployer {
             repository(url: 'http://localhost:8081/nexus/content/repositories/wom/') {//仓库地址
                 authentication(userName: "admin",//用户名
                         password: "admin123")//密码
             }

             pom.project {

                 name 'chelaile-test-library'
                 packaging 'arr'
                 description 'who are you'
                 url 'http://127.0.0.1:8081/nexus/content/repositories/wom/'//仓库地址
                 groupId "try"
                 artifactId 'chelaileTest'
                 version 1.7
             }
         }
    }

甚至，

            pom.project {

                 name 'chelaile-test-library'
                 packaging 'arr'
                 description 'who are you'
                 url 'http://127.0.0.1:8081/nexus/content/repositories/wom/'//仓库地址
                 groupId "try"
                 artifactId 'chelaileTest'
                 version 1.7
             }

都可以用 `pom.groupId` 等代替。

#### 四、使用Library

也很简单

    allprojects {
        repositories {
            jcenter()
            maven {
                url "http://localhost:8081/nexus/content/groups/public/"
            }
        }
    }

注意

>  maven {
>      url "http://localhost:8081/nexus/content/groups/public/"
>  }

然后在dependency里加入compile语句。注意这里的格式：

> compile 'try:jar-test:2.0'

groupId:artifactId:版本号 这是gradle构建repository的优势，简单的命令，而无需冗长的xml格式。


## Caution

##### Num 1

写gradle的时候，会出现部分代码呈现灰色，报错无法获知来源，可以无视。


##### Num 2

由于AS的ADT默认支持jcenter，所以在structrue中，永远找不到你想要的jar。

因此直接手动输入compile...

##### Num 3

引入库的问题

分jar和aar格式，aar即是包含资源文件，Minifest文件等，于是我们需要注意去掉可能与被引入工程冲突的代码。

同时如果上传的工程含有对其他jar包的引用，在引用该工程时，会同时引入其他支持的jar包。


