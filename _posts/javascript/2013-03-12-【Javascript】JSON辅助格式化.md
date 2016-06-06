---
layout: post
title:  "【Javascript】JSON辅助格式化"
date:   2013-03-12 13:46:04 +0800
categories: javascript
tag: [javascript]
---

平时服务器端开发人员写好后台之后一般写一份简单的接口说明页面，类似：

{% highlight html %}
<form action="test.php" accept-charset="utf-8">
    <div><label for="">param_1</label><input type="text" name="param_1" value="value_1"/></div>
    <div><label for="">param_2</label><input type="text" name="param_2" value="value_2"/></div>
    <div><label for="">param_3</label><input type="text" name="param_3" value="value_3"/></div>
    <div><label for="">param_4</label><input type="text" name="param_4" value="value_4"/></div>
    <div><input type="submit" value="submit"/></div>
</form>
{% endhighlight %}  

由于结果是以json形式返回的，不容易一眼辨认，所以为了方便，对结果进行了简单的处理：

1,由于不能控制返回结果的页面，所以直接对请求进行了拦截并用ajax方式进行重发。
2,格式化返回的json结果，非json结果直接显示。

注：ubuntu下的chromium在处理overflow的问题上貌似有点不一样，所以结果容器写得有点罗嗦。

具体例子：
{% highlight html %}
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8"/>
</head>
<body>
<div id="page">
    <form action="test.php" accept-charset="utf-8">
        <div><label for="">param_1</label><input type="text" name="param_1" value="value_1"/></div>
        <div><label for="">param_2</label><input type="text" name="param_2" value="value_2"/></div>
        <div><label for="">param_3</label><input type="text" name="param_3" value="value_3"/></div>
        <div><label for="">param_4</label><input type="text" name="param_4" value="value_4"/></div>
        <div><input type="submit" value="submit"/></div>
    </form>
</div>
<script type="text/javascript" src="../js/jQuery.js"></script>
<script type="text/javascript" src="../js/JSONFormat.js"></script>
</body>
</html>
{% endhighlight %}  

显示效果：

![2]({{ site.baseurl }}/image/js_json_format.png)

JSONFormat.js内容：

{% highlight html %}
var JSONFormat = (function(){
    var _toString = Object.prototype.toString;

    function format(object, indent_count){
        var html_fragment = '';
        switch(_typeof(object)){
            case 'Null' :0
                html_fragment = _format_null(object);
                break;
            case 'Boolean' :
                html_fragment = _format_boolean(object);
                break;
            case 'Number' :
                html_fragment = _format_number(object);
                break;
            case 'String' :
                html_fragment = _format_string(object);
                break;
            case 'Array' :
                html_fragment = _format_array(object, indent_count);
                break;
            case 'Object' :
                html_fragment = _format_object(object, indent_count);
                break;
        }
        return html_fragment;
    };

    function _format_null(object){
        return '<span class="json_null">null</span>';
    }

    function _format_boolean(object){
        return '<span class="json_boolean">' + object + '</span>';
    }

    function _format_number(object){
        return '<span class="json_number">' + object + '</span>';
    }

    function _format_string(object){
        if(0 <= object.search(/^http/)){
            object = '<a href="' + object + '" target="_blank" class="json_link">' + object + '</a>'
        }
        return '<span class="json_string">"' + object + '"</span>';
    }

    function _format_array(object, indent_count){
        var tmp_array = [];
        for(var i = 0, size = object.length; i < size; ++i){
            tmp_array.push(indent_tab(indent_count) + format(object[i], indent_count + 1));
        }
        return '[\n'
            + tmp_array.join(',\n')
            + '\n' + indent_tab(indent_count - 1) + ']';
    }

    function _format_object(object, indent_count){
        var tmp_array = [];
        for(var key in object){
            tmp_array.push( indent_tab(indent_count) + '<span class="json_key">"' + key + '"</span>:' +  format(object[key], indent_count + 1));
        }
        return '{\n'
            + tmp_array.join(',\n')
            + '\n' + indent_tab(indent_count - 1) + '}';
    }

    function indent_tab(indent_count){
        return (new Array(indent_count + 1)).join('   ');
    }

    function _typeof(object){
        var tf = typeof object,
            ts = _toString.call(object);
        return null === object ? 'Null' :
            'undefined' == tf ? 'Undefined'   :
                'boolean' == tf ? 'Boolean'   :
                    'number' == tf ? 'Number'   :
                        'string' == tf ? 'String'   :
                            '[object Function]' == ts ? 'Function' :
                                '[object Array]' == ts ? 'Array' :
                                    '[object Date]' == ts ? 'Date' : 'Object';
    };

    function loadCssString(){
        var style = document.createElement('style');
        style.type = 'text/css';
        var code = Array.prototype.slice.apply(arguments).join('');
        try{
            style.appendChild(document.createTextNode(code));
        }catch(ex){
            style.styleSheet.cssText = code;
        }
        document.getElementsByTagName('head')[0].appendChild(style);
    }

    loadCssString(
        '.json_key{ color: purple;}',
        '.json_null{color: red;}',
        '.json_string{ color: #077;}',
        '.json_link{ color: #717171;}',
        '.json_array_brackets{}');

    var _JSONFormat = function(origin_data){
        this.data = 'string' != typeof origin_data ? origin_data :
            JSON && JSON.parse ? JSON.parse(origin_data) : eval('(' + origin_data + ')');
    };

    _JSONFormat.prototype = {
        constructor : JSONFormat,
        toString : function(){
            return format(this.data, 1);
        }
    }

    return _JSONFormat;

})();

function create_result_contatiner(){
    var $result = $('<pre id="result" style=" width: 100%; height: 100%; overflow: scroll; overflow-x: scroll; overflow-y:scroll"></pre>')
    var $result_container = $('<div id="result_container" style="position: fixed; top: 1%; right: 8px; width: 5%; height: 97%; margin: 0; padding: 0;  border:1px solid skyblue; background: #f8f8f8; line-height: 1.2em; font-size: 14px; cursor: pointer;"></div>');
    $result_container.append($result);
    $result_container.hover(function(){
        $(this).stop(true).animate({width:'50%'}, 'slow');
    }, function(){
        $(this).stop(true).animate({width:'5%'}, 'slow');
    });
    $('body').append($result_container);
    return [$result_container, $result];
}

(function request_intercept(args){
    var $result_container = args[0],
        $result = args[1];
    $('form *[type="submit"]').bind('click', function(){
        var _form = $(this).parents('form'),
            _action = (_form.attr('action') || './'),
            _method = (_form.attr('method') || 'get').toLowerCase(),
            _params = {};
        _form.find('input[type="text"]').each(function(){
            var item = $(this);
            _params[item.attr('name')] = item.val();
        });
        $['get' == _method ? 'get' : 'post'](_action, _params, function(response){
            try{
                var j = new JSONFormat(JSON && JSON.parse ? JSON.parse(response) : eval('(' + response + ')'));
                $result.html(j.toString());
            }catch (e){
                $result.html($result.text(response).html());
            }
            $result_container.stop(true).animate({width:'50%'}, 'slow');
        });
        return false;
    });
})(create_result_contatiner());

{% endhighlight %}
