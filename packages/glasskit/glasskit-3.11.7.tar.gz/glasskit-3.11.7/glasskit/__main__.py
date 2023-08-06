import argparse
import os
import re
import jinja2
import venv
import shutil
from subprocess import Popen
from glasskit.uorm.models.meta import snake_case


PROJECT_NAME_EXPRESSION = re.compile(r"^[a-zA-Z0-9_]+$")
FIELD_TYPE_MAP = {
    "any": "Field",
    "str": "StringField",
    "string": "StringField",
    "int": "IntField",
    "bool": "BoolField",
    "boolean": "BoolField",
    "float": "FloatField",
    "list": "ListField",
    "dict": "DictField",
    "oid": "ObjectIdField",
    "object_id": "ObjectIdField",
    "datetime": "DatetimeField",
    "date": "DatetimeField",
    "ts": "DatetimeField",
}


def find_project_name():
    project_name = None
    for dirname in os.listdir("."):
        if os.path.isdir(dirname):
            contents = list(os.listdir(dirname))
            if "controllers" in contents:
                project_name = dirname
                break
    return project_name


def copy_sources(src_dir, dst_dir, appname):
    context = {"appname": appname}
    for srcname in os.listdir(src_dir):

        srcname = os.path.join(src_dir, srcname)
        if srcname.endswith("__pycache__") or srcname.endswith(".pyc"):
            continue

        dstname = os.path.join(dst_dir, os.path.basename(srcname))
        dstname = dstname.replace("__appname__", appname)

        if os.path.isdir(srcname):
            os.makedirs(dstname)
            copy_sources(srcname, dstname, appname)
        elif os.path.isfile(srcname):
            if srcname.endswith(".tmpl"):
                dstname = dstname[:-5]
                with open(srcname) as tmplfile:
                    tmpl = jinja2.Template(tmplfile.read())
                    with open(dstname, "w") as outfile:
                        outfile.write(tmpl.render(context))
            else:
                shutil.copy(srcname, dstname)


def glasskit_directory():
    return os.path.abspath(os.path.dirname(__file__))


def run_create(args):
    appname = args.project_name[0]
    dirname = appname
    if not PROJECT_NAME_EXPRESSION.match(dirname):
        raise ValueError(f"Invalid project name {dirname}")
    dirname = os.path.abspath(f"./{dirname}")

    project_templates_dir = os.path.join(glasskit_directory(), "project_templates")

    os.makedirs(dirname, exist_ok=False)
    copy_sources(project_templates_dir, dirname, appname)

    print("creating virtualenv")
    curr_dir = os.path.abspath(os.curdir)
    try:
        os.chdir(dirname)
        venv.create(args.venv, with_pip=True)
        python_path = os.path.join(os.curdir, "venv/bin/pip3")
        p = Popen([python_path, "install", "-r", "requirements.txt"])
        p.wait()
        os.chmod("glass.py", 0o755)
    finally:
        os.chdir(curr_dir)


def run_new_model(args):
    project_name = find_project_name()
    if project_name is None:
        raise RuntimeError(
            "project name is not detected. are you inside your project folder?"
        )

    class_name = args.model_name[0]
    model_filename = snake_case(class_name) + ".py"
    model_filename = os.path.join(project_name, f"models/{model_filename}")

    fields = []
    for field_desc in args.fields:
        field_desc = field_desc.split(":")
        field_type = "string"
        if len(field_desc) > 1:
            field_type = field_desc[1]
        field_desc = field_desc[0]

        if field_type not in FIELD_TYPE_MAP:
            raise TypeError(f'invalid field type "{field_type}"')
        fields.append((field_desc, FIELD_TYPE_MAP[field_type]))
    model_imports = ", ".join({fd[1] for fd in fields})
    tmplfilename = os.path.join(glasskit_directory(), "unit_templates/model.py.tmpl")
    with open(tmplfilename) as tmplfile:
        tmpl = jinja2.Template(tmplfile.read())

    os.makedirs(os.path.dirname(model_filename), exist_ok=True)
    with open(model_filename, "w") as modelf:
        modelf.write(
            tmpl.render(
                {
                    "classname": class_name,
                    "model_imports": model_imports,
                    "fields": fields,
                }
            )
        )
    print(f"File {model_filename} created")


def run_new_controller(args):
    project_name = find_project_name()
    if project_name is None:
        raise RuntimeError(
            "project name is not detected. are you inside your project folder?"
        )

    cls_tokens = args.ctrl_class.split(".")
    cls_module_path = ".".join(cls_tokens[:-1])
    cls_name = cls_tokens[-1]

    path_tokens = args.ctrl_path[0].split("/")
    ctrl_path = "/".join(path_tokens[:-1])
    ctrl_name = path_tokens[-1]

    ctrl_filename = os.path.join(
        project_name, "controllers", ctrl_path, f"{ctrl_name}.py"
    )

    context = {
        "cls_module_path": cls_module_path,
        "cls_name": cls_name,
        "ctrl_name": ctrl_name,
        "require_auth": not args.disable_auth,
    }

    tmplfilename = os.path.join(
        glasskit_directory(), "unit_templates/controller.py.tmpl"
    )
    with open(tmplfilename) as tmplfile:
        tmpl = jinja2.Template(tmplfile.read())

    os.makedirs(os.path.dirname(ctrl_filename), exist_ok=True)
    with open(ctrl_filename, "w") as ctrlfile:
        ctrlfile.write(tmpl.render(**context))

    print(f"File {ctrl_filename} created")


def run_new_task(args):
    project_name = find_project_name()
    if project_name is None:
        raise RuntimeError(
            "project name is not detected. are you inside your project folder?"
        )

    class_name = args.class_name[0]
    fields = args.fields
    create_args_list = ", ".join(["cls"] + fields)

    tmplfilename = os.path.join(glasskit_directory(), "unit_templates/task.py.tmpl")
    with open(tmplfilename) as tmplfile:
        tmpl = jinja2.Template(tmplfile.read())

    task_type = snake_case(class_name).upper()

    context = {
        "task_type": task_type,
        "cls_name": class_name,
        "fields": fields,
        "create_args_list": create_args_list,
    }

    task_filename = snake_case(class_name).lower() + ".py"
    task_filename = os.path.join(project_name, "tasks", task_filename)

    with open(task_filename, "w") as outfile:
        outfile.write(tmpl.render(**context))

    print(f"File {task_filename} created")


def main():
    parser = argparse.ArgumentParser(prog="glasskit")
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="sub-command help"
    )

    parser_create = subparsers.add_parser(
        "create", help="bootstrap a new glasskit project"
    )
    parser_create.add_argument(
        "project_name", nargs=1, type=str, help="project name to create"
    )
    parser_create.add_argument(
        "--venv", "-v", type=str, default="venv", help="venv directory name"
    )

    parser_new = subparsers.add_parser(
        "new", help="create a new unit, i.e. model, controller, task"
    )
    parser_new_subparsers = parser_new.add_subparsers(
        dest="unit", required=True, help="unit-type help"
    )
    new_model_parser = parser_new_subparsers.add_parser(
        "model", help="create a new model"
    )

    new_model_parser.add_argument("model_name", nargs=1, type=str, help="model_name")
    new_model_parser.add_argument(
        "fields",
        nargs="*",
        type=str,
        help="field descriptors: field1:any field2 "
        "field3:string "
        "field4:list etc...",
    )

    new_task_parser = parser_new_subparsers.add_parser("task", help="create a new task")
    new_task_parser.add_argument(
        "class_name", nargs=1, type=str, help="name of the task class"
    )
    new_task_parser.add_argument("fields", nargs="*", type=str, help="task fields list")

    new_controller_parser = parser_new_subparsers.add_parser(
        "controller", help="create a new controller"
    )
    new_controller_parser.add_argument(
        "ctrl_path", nargs=1, type=str, help="controller prefix path, i.e. api/v1/users"
    )
    new_controller_parser.add_argument(
        "--disable-auth", "-d", action="store_true", help="disable auth requirement"
    )
    new_controller_parser.add_argument(
        "--class",
        "-c",
        dest="ctrl_class",
        type=str,
        default="glasskit.controller.Controller",
        help="override default controller class",
    )
    args = parser.parse_args()

    if args.command == "create":
        run_create(args)
    elif args.command == "new":
        unit_type = args.unit
        if unit_type == "model":
            run_new_model(args)
        elif unit_type == "controller":
            run_new_controller(args)
        elif unit_type == "task":
            run_new_task(args)
        else:
            raise ValueError(f"unknown unit type f{unit_type}")


if __name__ == "__main__":
    main()
