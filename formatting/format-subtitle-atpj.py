# !!!注意!!!
# 本脚本仅用于减少打轴人员工作量，本脚本不能代替人为审查。
# 请务必在运行脚本后人工查看字幕。

# 测试时使用的软件版本：Arctime Pro 4.1
# 如果工程文件的构成方式在之后版本中发生改变，本脚本将可能不再兼容

# 已知的问题：

# 使用本脚本会让原本的 json 文件发生一些格式上的微妙改变，如：
#   >冒号后会多出空格
# 这和 python json 库的实现有关。
# 目前而言，Arctime 能够正确地读取这些格式上有改变的文件


import urllib.parse as urlparse
import json

#TODO:
# properly replace Chinese commas and full stops with spaces - DONE
# properly remove spaces at the beginnings and endings of a sentence - DONE
# properly replace “——” or “—” with " - " - DONE
# Search and replace functionalities

#  The atpj files use "+" to represent spaces
#  which is different from what you get from urllib.parse function "quote"


def read_project_file(file_dir: str):  # returns: string
    project_file = open(file_dir, "r")
    project_file_text = project_file.read()
    project_file.close()

    return project_file_text


# subtitles: dict["BLOCKS"] => list
# text for subtitles: ["text"] for each item (dict) in ["BLOCKS"]

# Automatic format: punctuations
# get ["BLOCKS"], get ["text"], replace ["text"], rewrite ["BLOCKS"], write file
# will go for unoptimised solution first


def format_text(subtitle_blocks: list[dict]):  # returns: list[dict] (["BLOCKS"])
    for block_index in range(len(subtitle_blocks)):
        block = subtitle_blocks[block_index]

        # THIS MAY CAUSE ISSUES - need to check how arctime deals with actual plus signs in the subtitle
        text_quoted = block["text"].replace("+", " ")
        text_unquoted = urlparse.unquote(text_quoted)

        # "If" clause: in case of an empty subtitle block.
        if len(text_quoted) > 0:

            # replace unwanted punctuations.
            # Do not move this block of logic to behind the spaces processing
            # or you may still end with extra spaces at the beginning or the end of a sentence,
            # considering that
            text_unquoted = text_unquoted.replace("，", " ")
            text_unquoted = text_unquoted.replace("。", " ")
            text_unquoted = text_unquoted.replace("；", " ")
            text_unquoted = text_unquoted.replace("……", "…")

            # Replacing dashes and likes
            # the next part is dumb and I know it is dumb and I will do it in a more clever way but not today

            # ATTENTION: the code will not be able to recognise words such as "avant-garde" that contain dashes themselves
            # in predictable future,
            # and may mis-replace dashes in such words.
            # Manual check is MANDATORY.

            # KNOWN ISSUE: you end up with " - - " if there is something like "——" in text
            replaceable_dash_styles = [" —— ", " ——", "—— ", " — ", " —", "— ", "—"]
            for style in replaceable_dash_styles:
                text_unquoted = text_unquoted.replace(style, "——")

            #TODO: some actual stuff to see if spaces are properly attached to a "-"
            # and deal with mis-attached spaces
            text_unquoted = text_unquoted.replace("——", " - ")

            # remove extra spaces at the beginning or the end of each sentence
            while text_unquoted[0] == " " or text_unquoted[-1] == " ":
                if text_unquoted[0] == " ":
                    text_unquoted = text_unquoted[1:]
                else:
                    text_unquoted = text_unquoted[:-1]

            # deal with duplicated spaces
            while "  " in text_unquoted:
                text_unquoted = text_unquoted.replace("  ", " ")

            # You don't simply quote() the text again, as arctime uses "+" and the urllib.parse.quote() function will
            # replace pluses ("+"s) and spaces (" "s) with hex codes as well

            text_unquoted_lst = text_unquoted.split()
            text_quoted_lst = []

            # I am sure that there is a better way to do this
            for word in text_unquoted_lst:
                text_quoted_lst.append(urlparse.quote(word))

            text_quoted = "+".join(text_quoted_lst)

            # do the following reassign properly?
            # text not properly replaced??
            block["text"] = text_quoted
            subtitle_blocks[block_index] = block

    return subtitle_blocks


# The routine
# No exception handling as for now.
if __name__ == "__main__":
    proj_file_dir: str = input("Input .atpj file directory:")
    proj_file_text: str = read_project_file(proj_file_dir)

    proj_file_dict: dict = json.loads(proj_file_text)
    subtitle_blocks: list[dict] = proj_file_dict["BLOCKS"]

    subtitle_blocks = format_text(subtitle_blocks)
    proj_file_dict["BLOCKS"] = subtitle_blocks

    # looks good so far

    proj_output_text: str = json.dumps(proj_file_dict)
    proj_output_file = open("./review.atpj", "w")
    proj_output_file.write(proj_output_text)
    proj_output_file.close()
