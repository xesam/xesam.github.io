---
layout: post
title:  "【杂谈】批量word和PPT文档转pdf"
date:   2012-11-06 13:46:04 +0800
categories: 杂谈
---

由于linux上处理word和ppt比较麻烦，而且有文件格式专利的问题，所以以下操作全部在Windows下面进行。

首先需要安装Microsoft Save as PDF加载项，官方下载地址：http://www.microsoft.com/zh-cn/download/details.aspx?id=7

安装成功后可以手工将文档另存为pdf。

需要引用“Win32::OLE”模块

{% highlight perl %}
use Win32::OLE;
use Win32::OLE::Const 'Microsoft Word';
use Win32::OLE::Const 'Microsoft PowerPoint';
{% endhighlight %}  

word转pdf：

{% highlight perl %}
sub word2pdf{
    my $word_file = $_[0];
    my $word = CreateObject Win32::OLE 'Word.Application' or die $!;
    $word->{'Visible'} = 0;
    my $document = $word->Documents->Open($word_file) || die("Unable to open document ") ; 
    my $pdffile = $word_file.".pdf";
    $document->saveas({FileName=>$pdffile,FileFormat=>wdExportFormatPDF});
    $document -> close ({SaveChanges=>wdDoNotSaveChanges});
    $word->quit();
}
{% endhighlight %}  

ppt转pdf

{% highlight perl %}
sub ppt2pdf{
    my $word_file = $_[0];
    my $word = CreateObject Win32::OLE 'PowerPoint.Application' or die $!;
    $word->{'Visible'} = 1;
    my $document = $word->Presentations->Open($word_file) || die("Unable to open document ") ; 
    my $pdffile = $word_file.".pdf";
    $document->saveas($pdffile,32);
    $document -> close ({SaveChanges=>wdDoNotSaveChanges});
    $word->quit();
}
{% endhighlight %}  

注意事项：

1. PPT转换中如果设置powerpoint不显示，即$word->{'Visible'} = 0，会导致转换失败。
2. 如果使用完整的路径，路径名中不能有空格以及“%”等特殊符号，不然无法打开文档。

转换当前文件夹下的文件：

{% highlight perl %}
use Cwd;

my $dirname = getcwd();
@files = glob "*.doc";
foreach (@files){
    print $dirname.'/'.$_, "\n";
    word2pdf($dirname.'/'.$_);
}
{% endhighlight %}  

如果要同时转换子文件夹的文件，可以先遍历，然后再转换：

{% highlight perl %}
use File::Find;
find(sub {
    word2pdf($File::Find::name) if /\.(doc|docx)/;
    ppt2pdf($File::Find::name) if /\.(ppt|pptx)/;
}, "D:/test");
{% endhighlight %}  

为了避免多次重复打开word，可以先获取所有需要转换的文档，集中转换：

{% highlight perl %}
find(sub {
    push(@file_word, $File::Find::name) if /\.(doc|docx)/;
}, "D:/test");

word2pdf(@file_word);

sub deleteSpace{
    my $filename = $_[0];
    my @temp = split(/\//, $filename);
    my $filename_without_path = pop(@temp);
    $filename_without_path =~ s/\s+//g;
    join('/', @temp).'/'.$filename_without_path;
}

sub word2pdf{
    my @files = @_;
    my $word = CreateObject Win32::OLE 'Word.Application' or die $!;
    $word->{'Visible'} = 0;
    foreach (@files){
        my $new_name = deleteSpace($_);
        rename($_, $new_name);
        print $new_name, "\n";
        my $document = $word->Documents->Open($new_name) || die "can not open document";
        my $pdffile = $new_name.".pdf";
        $document->saveas({FileName=>$pdffile,FileFormat=>wdExportFormatPDF});
        $document -> close ({SaveChanges=>wdDoNotSaveChanges});
    }
    $word->quit();
}
{% endhighlight %}  


也可以换一种实现，先调用chdir到子目录中，然后在子目录中进行转换，可以避免目录有不合法字符导致的转换失败，不过文件名的不合法字符导致的失败也不可避免，所以以上的各种转换，都需要先提出空格以及特殊字符才行，deleteSpace仅仅替换了空格，还需要改进。

 