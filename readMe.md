# objc-xcode-Hack-Handlers
##overview
It is a set of hack handlers for iOS/Mac os x developers. All of these handlers used to help you handle some problem about objc/Xcode/Svn and so on. I hope you will like it and it will make you relaxed.

### objcMethodFormatter
> a objc method-definition formatter.

#### example
change the method definition from:
   
   
     -(CGFloat) getHeightWithText:(NSString*)text fontSize:(CGFloat)fontSize constraint:(CGSize)cSize minHeight:(CGFloat)mHeight;
    
to

   
    -(CGFloat) getHeightWithText:(NSString*)text
                        fontSize:(CGFloat)fontSize
                      constraint:(CGSize)cSize
                       minHeight:(CGFloat)mHeight;
                       
#### TODO
(1) project path:

```
#TODO: change the path to your xcode project path
GLOBAL_PROJECT_PATH     = '/Users/yanghua/Desktop/weiboDemo'
```
(2) generally, you don't have to change it.it used to match file type. Sometimes, you may want to match other file type you can change it.

```
#want to match 
GLOBAL_INCLUDE = ['*.h', '*.m']
```
(3) if there are some file you don't need to do this format. you just fill into this list.Note:just write the relative path base on project path.

```
#want to exclude               
GLOBAL_EXCLUDE = [] 
```

=======================
### svnMissingFileWarningHandler
> a handler for svn missing-file warning when you use Xcode's build-in source control. It's a Xcode's little bug since version 4.3.x

Note:<br />
the handler works on ***svn client***.So you must install the svn client (it need svn command line).

#### TODO

(1) change your project path 

```
\#TODO: change the path to your xcode project path
GLOBAL_PROJECT_PATH     = '/Users/yanghua/Desktop/weiboDemo'
```
(2) change your log file path
 
```
\#TODO: change the path to the dir where you stone the log file
GLOBAL_LOGFILE_PATH     = '/Users/yanghua/Desktop/tmp.txt'
```
(3) do you want to keep the operate-log file?

```
\#TODO: the flag identify if you want to keep the logfile
\#default is True ,if False the logfile will be delete after running
GLOBAL_KEEP_LOGFILE     = True
```
## Usage
**Note that:** Each of these handlers is substantive. And the python version must be ***3.x+***

(1) command line in Terminal<br />
like that:

```
./XXXXXXX/objcMethodFormatter.py
```
or

```
python3 /XXXXXX/objcMethodFormatter.py
```
**tips**: the 'XXXXX' is the part of file path And you must give these handle-file executable permission with this cmd:

```
sudo chmod u+x /XXXXX/objcMethodFormatter.py
sudo chmod o+x /XXXXX/objcMethodFormatter.py
```
then enter your root password!

(2) Xcode's build-in [pre/post]-action   **(Recommend！)**

step one:

![img1][1]

step two:

![img2][2]

step three:

![img3][3]


[1]:http://img.my.csdn.net/uploads/201303/30/1364629799_9652.png
[2]:http://img.my.csdn.net/uploads/201303/30/1364629810_8739.png
[3]:http://img.my.csdn.net/uploads/201303/30/1364629829_3508.png

## more handlers
> I will make more hack handlers and if you have good ideas you can fork it or contact with me! 

##Contact
=========
any problem, let me know:

1. <yanghua1127@gmail.com>
2. <http://blog.csdn.net/yanghua_kobe>

### enjoy and have fun!