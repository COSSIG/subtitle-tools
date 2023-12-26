# 这个脚本的功能是将已经制作好的 srt 字幕中的中文标点修改（覆写）为符合本项目规范的样式（参见 SUBTITLE-STANDARD.md）
# 请务必不要对原文或者非 srt 格式的字幕使用这个脚本。
# 这个脚本目前不支持批量处理文件，也没有异常处理。会在未来加入这些功能

file_dir = input("请输入你想要处理的文件地址：")
file_in = open(file_dir, mode="r", encoding="utf-8")

file_content = file_in.read()
file_in.close()

file_content = file_content.replace("，", " ")
file_content = file_content.replace("。", " ")
file_content = file_content.replace("；", " ")


file_content = file_content.replace("——\n", " \n")
file_content = file_content.replace(" —— ", " - ")
file_content = file_content.replace("—\n", " \n")
file_content = file_content.replace("—", " - ")

file_content = file_content.replace("……", "…")

# 去除行尾的多余空格
file_content = file_content.replace(" \n", "\n")

# 去除行首的多余空格
file_content = file_content.replace("\n ", "\n")

file_out = open(file_dir, mode="w", encoding="utf-8")
file_out.write(file_content)
file_out.close()
