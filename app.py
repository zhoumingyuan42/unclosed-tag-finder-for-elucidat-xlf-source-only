from flask import Flask, render_template, request
import re

app = Flask(__name__)

@app.route("/")
@app.route("/home")

def home():
    return render_template("index.html")

@app.route("/result", methods=['POST','GET'])
def result():
    output = request.form.to_dict()
    name = output["name"]
    message = unclosed_tag_founder(name)

    return render_template("index.html", message = message)


def unclosed_tag_founder(text):
    lines = text.split('\n')
    line_num = 0
    message = "check complete, no unclosed tag found"
    for line in lines :
        line_num = line_num + 1
        if re.search(r"CDATA\[(.*)\]",line):
            #print(line)
            #print(line_num)
            if re.search("\"",line):
                stripped_line = line.replace("\"","")
                #print(stripped_line)
            cleaned_line = re.search(r"CDATA\[(.*)\]",stripped_line).group(1)

            tags = re.findall(r"<[^>]*[^/]>",cleaned_line)
            if len(tags) != 0 :
                open_tags = []
                for i in tags :
                    if not re.search(r"/",i) :
                        open_tags.append(i)
                    else :
                        i = i.replace("/","")
                        i = i.replace(">","")
                        if re.match(i,open_tags[-1]) :
                            #print("tag is closed")
                            open_tags = open_tags[:-1]
                        else :
                            message = f"unclosed tag found on line {line_num} for tag {open_tags[-1]}"
                            break

        else :
            #print("not text")
            continue

    return message


if __name__ == '__main__':
    app.run(debug = True, port = 5001)
