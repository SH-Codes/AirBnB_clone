#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(arg):
    """Parses input arguments into a list."""
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.

    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel": BaseModel,
        "User": User,
        "State": State,
        "City": City,
        "Place": Place,
        "Amenity": Amenity,
        "Review": Review
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid."""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Create a new instance of BaseModel and saves it to JSON file."""
        argl = parse(arg)
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            new_instance = HBNBCommand.__classes[argl[0]]()
            new_instance.save()
            print(new_instance.id)

    def do_show(self, arg):
        """Show the string representation of an instance."""
        argl = parse(arg)
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(argl[0], argl[1])
            if key not in storage.all():
                print("** no instance found **")
            else:
                print(storage.all()[key])

    def do_destroy(self, arg):
        """Delete an instance based on the class name and id."""
        argl = parse(arg)
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        else:
            key = "{}.{}".format(argl[0], argl[1])
            if key not in storage.all():
                print("** no instance found **")
            else:
                del storage.all()[key]
                storage.save()

    def do_all(self, arg):
        """Show all instances or all instances of a class."""
        argl = parse(arg)
        objects = storage.all()
        if len(argl) > 0:
            if argl[0] not in HBNBCommand.__classes:
                print("** class doesn't exist **")
                return
            objects = {key: obj for key, obj in objects.items()
                       if isinstance(obj, HBNBCommand.__classes[argl[0]])}
        print([str(obj) for obj in objects.values()])

    def do_count(self, arg):
        """Count the number of instances of a class."""
        argl = parse(arg)
        if len(argl) == 0:
            print("** class name missing **")
            return
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        objects = storage.all()
        count = sum(1 for obj in objects.values()
                    if isinstance(obj, HBNBCommand.__classes[argl[0]]))
        print(count)

    def do_update(self, arg):
        """Update an instance with the given id and class name."""
        argl = parse(arg)
        if len(argl) < 2:
            print("** class name missing **")
            return
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return
        if len(argl) < 3:
            print("** instance id missing **")
            return
        key = "{}.{}".format(argl[0], argl[1])
        if key not in storage.all():
            print("** no instance found **")
            return
        obj = storage.all()[key]
        if len(argl) < 4:
            print("** attribute name missing **")
            return
        if len(argl) < 5:
            print("** value missing **")
            return
        attr_name = argl[2]
        attr_value = argl[3]
        if hasattr(obj, attr_name):
            attr_value = type(getattr(obj, attr_name))(attr_value)
        setattr(obj, attr_name, attr_value)
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()

