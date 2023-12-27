# subtitle-tools
Repository dedicated to storing subtitle related scripts &amp; tools. Some would be migrated from cossig-subtitles/subtitle-tools.

这个储存库包含有方便字幕制作者的一些脚本和工具。有一些是从原本的 [COSSIG-Subtitles](https://github.com/COSSIG/COSSIG-Subtitles)/subtitle-tools 迁移来的。


**请务必注意：自动化工具只能帮助你制作字幕，不能替代你工作。请字幕制作者务必认真审查工具生成的字幕文件或者字幕工程文件，以免乐极生悲。**


## formatting / 字幕格式化
将中文字幕编辑为大致符合[**标准**](https://github.com/COSSIG/COSSIG-Subtitles/blob/main/SUBTITLE-STANDARD.md)的格式。主要是去除句号和逗号。

现在支持 srt 字幕（.srt）和 ArcTime 工程文件 （.atpj）。formatting 文件夹中的两个 Python 脚本分别对应两种格式。

脚本本身存在一些已知的问题，而且问题触发时会影响字幕格式和可读性。请字幕制作者务必在运行脚本之后仔细查看生成的字幕文件或工程文件。


### 使用本工具：
请确保你安装了 [Python 3](https://www.python.org/downloads/)。目前，两个脚本均不需要第三方库。

## auto_timeline / 自动打轴
运行脚本，输入音频 / 视频文件，程序会自动听写并输出对应的英文字幕。现在只支持输出 Aegisub (.ass) 格式字幕。

### 使用本工具：
请确保你安装了 [Python 3](https://www.python.org/downloads/)。

目前，这个工具依赖于：

* Python 第三方库： [openai-whisper](https://github.com/openai/whisper/) - AI 语音识别 

* Python 第三方库： [pysubs2](https://github.com/tkarabela/pysubs2) - 字幕输出

* 命令行工具： [ffmpeg](https://ffmpeg.org/) - 音视频处理

妥善安装以上三者之后，`timeline.py` 才能够运行。注意 openai-whisper 本身依赖于 ffmpeg 和 rust。

在第一次运行本工具时，程序可能会先下载语言识别模型。这会耗费一些时间。