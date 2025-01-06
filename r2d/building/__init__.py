def build_line(line: str, imports, parent=None):
    line = line.removeprefix("\t")
    line = line.removeprefix("    ")

    splitted = line.split(" ")

    out = ""
    ret_obj = None

    if splitted[0] == "sceneObj":
        name = splitted[1]
        try:
            klass, file = splitted[2].split("/")
        except ValueError:
            klass, file = 'r2d.' + splitted[2], None

        pos = "".join(splitted[3:])
        if file:
            if f"from {file} import {klass}" not in imports: imports.append(f"from {file} import {klass}")
        out += f"{name} = {klass}(win, '{name}', {pos})\n"
        parent = name

        ret_obj = name

    
    if splitted[0] == "component":
        klass = splitted[1]
        args = ", ".join(splitted[2:])

        if "/" in klass:
            second = klass.split("/")[1]
            first = klass.split("/")[0]
            if f"from {second} import {first}" not in imports: imports.append(f"from {second} import {first}")
            klass = klass.split("/")[0]
        else:
            klass = "r2d." + klass

        comma = ", " if args else ""
        out += f"{klass}({parent}{comma}{args})\n"

    if splitted[0] == "end":
        parent = None
        out += "\n"

    return out, imports, parent, ret_obj


def build_file(text, imports):
    out = ""
    parent = None
    ret_objs = []

    for line in text.split("\n"):
        line_out, imports, parent, ret_obj = build_line(line, imports, parent)
        if ret_obj:
            ret_objs += [ret_obj]
        out += line_out

    return imports, out, ret_objs

def build_all_files(file_list, saveto):
    imports = ["import r2d", "import sys"]
    output = "\n\nsys.path.append('../r2d')\n\nscenes = {}\nr2d.initialise()\n\nwin = r2d.Window()\n"
    for filename in file_list:
        with open(filename) as file:
            contents = file.read()

        new_imports, out, ret_objs = build_file(contents, imports)
        output += out

        scenevalues = "[" + ", ".join(ret_objs) + "]"


        output += "\n\nscenes.update({" + f'"{filename.removesuffix(".r2dscene")}": ' + scenevalues + "})\n\n\n"

        for import_ in new_imports:
            if import_ not in imports:
                imports.append(import_)

    with open(saveto, "w") as file:
        file.write('import sys\n\nsys.path.append(r"../")\n\n' + "\n".join(imports) + output + "\n" + "sceneManager = r2d.SceneManager(win, scenes)\n\nwin.run()")

