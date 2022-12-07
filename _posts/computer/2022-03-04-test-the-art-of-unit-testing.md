---
layout: post
title:  "单元测试的艺术-第三版 简记"
date:   2022-03-04 09:00:00 +0800
categories: computer
tag: [computer]
---
本文是《The Art of Unit Testing with example in JavaScript, 3rd Edition》一书的读书简记，此书前两版有中文版本：第一版使用 C 语言描述，第二版使用 C# 语言描述。
第三版暂未出版中文版，使用 Javascript/Typescript 语言描述，使用的主要测试框架的 [Jest](https://jestjs.io/)
<!-- more -->

作者对 Unit of Work 的定义：

*A unit of work is the sum of actions that take place between the invocation of an entry point up until a noticeable end result through one or more exit points. The entry point is the thing we trigger. *

A unit of work can be a single function, multiple functions, multiple functions or even multiple modules or components. But it always has an entry point which we can trigger from the outside, and it always ends up doing something useful.

这里就引出了全文的核心概念——**Entry Points & Exit Points**：

**Exit points are end results of a unit of work.**

![1]({{ site.baseurl }}/assets/the_art_of_unit_testing_3rd/EntryPoints&ExitPoints.png)

Three different types of end results: 

1. The invoked function returns a useful value (not undefined). 
2. There’s a noticeable change to the state or behavior of the system before and after invocation that can be determined without interrogating private state. 
3. There’s a callout to a third-party system over which the test has no control. 

根据适用测试技术的不同，上述又可以分为：

1. Return-value based exit points (direct outputs) of all the exit point types, should be the easiest to test. You trigger an entry point, you get something back, you check the value you get back.
2. State based tests (indirect outputs) require a little more gymnastics usually. You call something, then you do another call to check something else (or call the previous thing again) to see if everything went according to plan.

整个单元测试的侧重点是“Exit Points”。

Characteristics of a good unit test:

1. It should be easy to read and understand the intent of the test author. 
2. It should be easy to read and write 
3. It should be automated and repeatable. 
4. It should be useful and provide actionable results. 
5. Anyone should be able to run it at the push of a button. 
6. When it fails, it should be easy to detect what was expected and determine how to pinpoint the problem.

Great unit tests should also exhibit the following properties: 

1. It should run quickly. 
2. It should be consistent in its results . 
3. It should have full control of the code under test. 
4. It should be fully isolated. 
5. It should run in memory without requiring system files, networks, databases It should be as synchronous and linear as possible when it makes sense.

To start off, ask yourself the following questions about the tests you’ve written/executed up to now:

1. Can I run and get results from a test I wrote two weeks or months or years ago? 
2. Can any member of my team run and get results from tests I wrote two months ago? 
3. Can I run all the tests I’ve written in no more than a few minutes? 
4. Can I run all the tests I’ve written at the push of a button?
5. Do the tests I wrote always report the same outcome (given no code changes on my team)? 
6. Do my tests pass when there are bugs in another team’s code? 
7. Do my test show the same result when run on different machines or environments? 
8. Do my tests stop working if there’s no database, network or deployment? 
9. If I delete, move or change one test, do other tests remain unaffected? 
10. Can I easily set up the needed state for a test without relying on outside resources like a database or a 3rd party, with very little code?

关于 legacy code 的调侃：

*A client once defined legacy code in a down-to-earth way: “code that works.” Many people like to define legacy code as “code that has no tests.”*

这些自省的问题，都围绕者单元测试的核心原则：

1. Readability. 
2. Maintainability.
3. Trust.

做个简单的总结：

A unit test is an automated piece of code that invokes the unit of work trough an entry point, and then checks one of its exit points. A unit test is almost always written using a unit testing framework. It can be written easily and runs quickly. It’s trustworthy, readable & maintainable. It is consistent as long as the production code we control has not changed.

### TDD

最佳实践之一：TDD（我的补充：可以参考 《Java测试驱动开发》等等书籍）。

The technique of TDD is quite simple: 
1. Write a failing test to prove code or functionality is missing from the end product. 
2. Make the test pass by adding functionality to the production code that meets the expectations of your test. 
3. Refactor your code. 

Technically, one of the biggest benefits of TDD nobody tells you about is that by seeing a test fail, and then seeing it pass without changing the test, you’re basically testing the test itself. If you expect it to fail and it passes, you might have a bug in your test or you’re testing the wrong thing. If the test failed and now you expect it to pass, and it still fails, your test could have a bug, or it’s expecting the wrong thing to happen.

Three core skills needed for successful TDD：
1. Writing Good Tests.
2. Writing Test First.
3. SOLID Design.

### Unit testing frameworks & Jest

Jest acted in several capacities for us: 
1. It acted as a test library to use when writing the test 
2. It acted as an assertion library for asserting inside the test (‘expect’) 
3. It acted as the test runner 
4. It acted as the test reporter for the test run.

What unit testing frameworks offer:

1. Structure.
2. Repeatability.
3. Confidence through time savings.

Unit tests usually are made of three main “steps”: **Arrange, Act and Assert**. 

1. Arrange: setup the scenario under test.
2. Act: invoke the entry point with inputs.
3. Assert: check the exit point. 

This is colloquially called the ‘**AAA**’ Pattern.

Put three pieces of information in test names, so that the reader of the test will be able to answer most of their mental questions just by looking at the name of the test. These three parts include: 

1. The unit of work under test.
2. The scenario or inputs to the unit.
3. The expected behavior or exit point.

A nice acronym for this: **U.S.E**: 

1. Unit under test.
2. Scenario.
3. Expectation.

作者的心得：*It’s human nature to put things in the easiest place possible, especially if everyone else before you have done so as well.*

### Stub & Mock

There are two main types of dependencies that our unit of can use.

1. Outgoing Dependencies: dependencies that represent an exit point of our unit of work.
2. Dependencies: dependencies that are not exit points. They do not represent a requirement on the eventual behavior of the unit of work. They are merely there to provide test-specific specialized data or behavior into the unit of work. 

#### STUB: 

Break incoming dependencies (indirect inputs). Stubs are fake modules, objects or functions that provide fake behavior or data into the code under test. We do not assert against them. We can have many stubs in a single test. 

Stubs represent waypoints, not exit points. They do not represent exit points because the data or behavior flow into the unit of work. They are points of interaction, but they do not represent an ultimate outcome the the unit of work ends up doing. Instead they are an interaction on the way to achieve the end result we care about, so we don’t treat them as exit.

#### MOCK

Break outgoing dependencies (outputs, exit points). Mocks are fake modules, objects or functions that we assert were called in our tests. A Mock represents an exit point in a unit test. Because of this, it is recommended to have no more than a single mock per test.

概念参考：

    Dependencies： 
    The things that make our testing lives & code maintainability difficult, since we cannot control them from our tests. 

    Control：
    The ability to instruct a dependency how to behave. Whoever is creating the dependencies is said to be in control over them since they have the ability to configure them before they are used in the code under test. 

    Inversion of Control： 
    Designing the code to remove the responsibility of creating the dependency internally and externalizing it instead. 

    Dependency Injection ：
    The act of sending a dependency through the design interface to be used internally by apiece of code. The place where you inject the dependency is the injection point. 

    Seam ：
    Seams are where two pieces of software meet and something else can be injected. They are a place where you can alter behavior in your program without editing in that place. 


### Interaction testing

Interaction testing is checking how a unit of work interacts and sends messages to a dependency beyond its control. Mock functions or objects are used to assert that a call was made correctly to an external dependency.

常用技巧：

    Standard:
    Introduce Parameter 

    Functional:
    Convert to partial application function 
    Convert to Factory Function 

    Modular:
    Abstract Module Dependency 

    Object Oriented: 
    Inject Untyped Object Inject Interface

A simple rule of thumb: 

**It should be OK to have multiple stubs in a test, but you don’t usually want to have more than a single mock per test – because that means you’re testing more than requirements in a single test.**

I use the word “Fake” to denote anything that isn’t real. Another common word for this sort of thing is “Test Double”. Fake is shorter so I like it.
I highly recommend to use only fake interfaces that answer both of these conditions: 

1. You control those interfaces (they are not made by a 3rd party). 
2. They are adapted to the needs of your unit of work or component.

这里作者吐槽了一下 spy 的设计（或者说命名），作者这个特性引发了滥用：

Both in test frameworks, to “take over” existing objects and functions and “spy” on them. By spying on them we can later check if they were called, how many times and with which arguments. 
This essentially can turn parts of real objects into mock functions, while keeping the rest of the object as a real object. This can create more complicated tests that are more brittle, but can sometimes be a viable option, especially if you’re dealing with legacy code.

Spy was originally designed as the idea that you can look at a real function and “spy” on it without altering its behavior. **Whenever you see someone mention “spy” think “partial mock/stub” because chance are that’s what they’re trying to achieve. When in doubt, think of “Spy” as “Partial Mock/Stub”**

Isolation Frameworks 的定义：

*An isolation framework is a set of programmable APIs that allow the dynamic creation, configuration and verification of mocks and stubs, either in object or function form; Using a framework, these tasks can often be simpler, faster, and shorter than hand-coding them.*

Because JavaScript supports multiple paradigms of programming design, we can split the frameworks in our world to two main flavors: 

1.  Loose JS Isolation Frameworks: 

        Vanilla JS friendly loose-typed isolation frameworks. These usually also lend themselves better to more functional style code because they require less “ceremony” and boilerplate code to do their work. 

2. Typed JS Isolation Frameworks: 

        More Object Oriented/TypeScript friendly isolation frameworks. Very useful when dealing with whole classes and interfaces.


What type of dependencies will you need to fake mostly? 

1. Module dependencies (imports, requires).
2. Functional (single and higher order functions, simple parameters and values) .
3. Full objects, object hierarchies and interfaces.

Distinct advantages to using isolation frameworks: 

1. Easier modular faking. 
2. Easier simulation of values or errors. 
3. Easier fakes creation.


A few things to watch out for: 

1. You don’t need mock objects most of the time.
2. Unreadable test code.
3. Verifying the wrong things.(A lot of people new to tests end up verifying things just because they can, not because it makes sense.)
4. Having more than one mock per test.
5. Over specifying the tests.

**Testing interactions is a double-edged sword: test it too much, and you start to lose sight of the big picture—the overall functionality; test it too little, and you’ll miss the important interactions between units of work.** 

Here are some ways to balance this effect:

1. Use stubs instead of mocks when you can.
2. Avoid using stubs as mocks if humanly possible.

### Async

Make the code more unit-testable:

1. Extract Entry Point. Extracting the parts that are pure logic into their own function and treating those functions as entry points for our tests. 
2. Extract Adapter: Extracting the thing that is inherently asynchronous and abstracting it away so that we can replace it with something that is synchronous.

#### Extract Entry Point

In this pattern, we take a specific piece of async work, and split it into the two pieces:
1. The async part (which stays intact)
2. The callbacks that are invoked when the async execution finishes. Those are extracted as new functions which eventually become entry points for a purely logical unit of work that we can invoke with pure unit tests.

![1]({{ site.baseurl }}/assets/the_art_of_unit_testing_3rd/ExtractEntryPoint.png)

#### Extract Adapter

We look at the asynchronous piece of code just like we look at any dependency we’d like to replace in our tests to gain more control. 
Instead of extracting the logical code into its own set of entry points, we’re extracting the asynchronous code (our dependency) and abstracting it away under an adapter, which we can later inject just like any other dependency.

![1]({{ site.baseurl }}/assets/the_art_of_unit_testing_3rd/ExtractAdapter.png)

### Dealing with Timers 

Two patterns of getting around them directly: 

1. Directly Monkey patching the function.Monkey patching is a way for a program to extend or modify supporting system software locally (affecting only the running instance of the program).
2. Using test frameworks to disable and control them.


### 写好单元测试

The tests that you write should have three properties that together make them good:

1. Trustworthiness—Developers will want to run trustworthy tests, and they’ll accept the test results with confidence. Trustworthy tests don’t have bugs, and they test the right things. 
2. Maintainability—Unmaintainable tests are nightmares because they can ruin project schedules, or they may be sidelined when the project is put on a more aggressive schedule. Developers will simply stop maintaining and fixing tests that take too long to change or that need to change very often on very minor production code changes. 
3. Readability—This means not just being able to read a test but also figuring out the problem if the test seems to be wrong. Without readability, the other two pillars fall pretty quickly. Maintaining tests becomes harder, and you can’t trust them anymore because you don’t understand them.


### Trustworthiness

Why Tests Fail？

1. A real bug has been uncovered in the production code.
2. Buggy (lying) test.
3. Out of Date test (feature changed).
4. Conflicting test (with another test).
5. Flaky Test.
6. Smelling a false sense of trust in passing tests

降低测试代码自身的出错可能性：

1. write your code in a test driven manner.
2. remove the amount of logic related code that exists in the test.

*大家跟我一起喊：No ifs, switches, loops or other forms of logic if I can help it.*

又一条准则：

**Avoid dynamically creating the expected value in your asserts, use hardcoded values when possible.**

Out of Date test (feature changed)：

1. Adapt the test to the new functionality.
2. Write a new test for the new functionality and remove the old test because it has now become irrelevant.

Here are some reasons I reduce my trust in tests even if they are passing:

1. Tests that don’t assert anything.
2. Not understanding the tests.
3. Mixing Unit & Integration (Flaky) Tests.
4. Having logic inside unit tests.
5. Testing multiple concerns (entry/exit points).
6. Tests that keep changing.


对开发经理/项目经理的话: Code coverage shouldn’t ever be a goal on its own. It doesn’t mean “code quality”. In fact, it often causes your developers to write meaningless tests that will cost even more time to maintain. Instead, measure “Escaped Bugs” ,“Time to Fix” and well as other metrics.

The test-break-up rule: 

**if the first assert fails, do you still care what the result of the next assert is?? If you do, you should probably separate the test into two tests.**

Here are some ways to reduce the costs associated with handling flaky tests: 

1. Agree on what flaky means to your organization.
2. Place any test deemed “flaky” in a special category or folder of tests that can be run separately. 
3. Prune and remove flakiness from quarantined tests.

Dealing with flaky tests:

1. Quarantine.
2. Fix.
3. Convert.
4. Kill.

### Maintainability

Ask these questions if we ever want to get down to the root causes: 

1. When do we notice that a test might require a change? (When tests fail) 
2. Why do tests fail?
3. Which test failures “force” us to change the test? 
4. When do we “choose” to change a test even if we are not forced to?

The basic concept to keep in mind is that **a test should always run in its own little world, isolated from even the knowledge that other tests out there may do similar or different things**.

CONSTRAINED TEST ORDER（意味着测试之间存在依赖）

Refactoring this we can take a few steps: 

1. Extract a helper function for adding a user 
2. Reusing this function form multiple tests 
3. Reset the user cache between tests.

Refactoring to increase maintainability

1. Avoid Testing private or protected methods.
2. Remove duplication.
3. Avoid setup methods( in a maintainable manner).
4. Using parameterized tests to remove duplication.
5. Avoid overspecification.

if you see a private method, find the public use case in the system that will exercise it.Sometimes if a private method is worth testing, it might be worth making it public, static, or at least internal and defining a public contract against any code that uses it. In some cases, the design may be cleaner if you put the method in a different class altogether.

Here are ways unit tests are often over specified:

1. A test asserts purely internal state in an object under test. 
2. A test uses multiple mocks. 
3. A test uses stubs also as mocks. 
4. A test assumes specific order or exact string matches when it isn’t required.

The real exit point depends on the type of test we wish to perform:

1. For a value based test, which I would highly recommend to lean towards when possible, we look for a return value from the called function.
2. For a state based test we look for a sibling function (a function that exists at the same level of scope as the entry point.
3. For a 3d party test we would have to use a mock, and that would require us to find out where is the “fire and forget” location inside the code.


### Readability

There are several facets to readability: 

1. Naming unit tests 
2. Naming variables 
3. Creating good assert messages 
4. Separating asserts from actions

Three important pieces of information are present in the name of the test:

1. The entry point to the unit of work (or, the name of the feature you’re testing) 
2. The scenario under which you’re testing the entry point 
3. The expected behavior of the exit point

Variable names and values are just as much about explaining to the reader what they should NOT care about as it is about explaining what IS important.

readability! readability! readability!

作者在书中不止一个地方提到了测试框架的 setup 特性，并表示这个特性也导致了太多的滥用：

I like that each test is self- encapsulating its own state. The nested describe structure acts as a good way to know where we are, but the state is all triggered from inside the ‘it’ blocks. Not outside of them.

Factory methods & Parameterized tests can help maintainability even more.


### 书中提到的参考书籍

《XUnit Test Patterns》http://xunitpatterns.com/