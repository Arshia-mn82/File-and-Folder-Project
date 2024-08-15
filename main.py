class File:
    """
    Represents a file in the file system.

    Attributes:
    -----------
    name : str
        The name of the file.
    data : list of str
        The content of the file, split into lines.

    Methods:
    --------
    read():
        Returns the content of the file as a single string with lines joined by newline characters.
    append(content):
        Appends a new line of content to the file.
    """
    def __init__(self, name, data=""):
        self.name = name
        self.data = data.splitlines()

    def read(self):
        """
        Returns the content of the file as a single string with lines joined by newline characters.
        
        Returns:
        --------
        str
            The content of the file.
        """
        return "\n".join(self.data)

    def append(self, content):
        """
        Appends a new line of content to the file.

        Parameters:
        -----------
        content : str
            The content to append to the file.
        """
        self.data.append(content)

class Folder:
    """
    Represents a folder in the file system.

    Attributes:
    -----------
    name : str
        The name of the folder.
    contents : dict
        A dictionary containing the items (files and subfolders) within the folder, 
        where the keys are item names and the values are the items.

    Methods:
    --------
    add(item):
        Adds a file or folder to the current folder.
    remove(name):
        Removes a file or folder from the current folder by name.
    get(name):
        Retrieves an item (file or folder) from the current folder by name.
    list_contents():
        Lists the names of all items in the current folder.
    """
    def __init__(self, name):
        self.name = name
        self.contents = {}

    def add(self, item):
        """
        Adds a file or folder to the current folder.

        Parameters:
        -----------
        item : File or Folder
            The item to add to the folder.
        """
        self.contents[item.name] = item

    def remove(self, name):
        """
        Removes a file or folder from the current folder by name.

        Parameters:
        -----------
        name : str
            The name of the item to remove.
        """
        if name in self.contents:
            del self.contents[name]

    def get(self, name):
        """
        Retrieves an item (file or folder) from the current folder by name.

        Parameters:
        -----------
        name : str
            The name of the item to retrieve.

        Returns:
        --------
        File or Folder
            The item with the specified name.

        Raises:
        -------
        ValueError
            If the item with the specified name is not found.
        """
        if name in self.contents:
            return self.contents[name]
        raise ValueError("Item not found")

    def list_contents(self):
        """
        Lists the names of all items in the current folder.

        Returns:
        --------
        list of str
            The names of the items in the folder.
        """
        return [item.name for item in self.contents.values()]


class FileSystem:
    def __init__(self):
        """Initializes the file system with a root folder."""
        self.root = Folder("root")
        self.current_folder = self.root

    def get_full_path(self):
        """
        Returns the full path from the root to the current folder as a string.
        """
        path_parts = []
        folder = self.current_folder
        while folder != self.root:
            path_parts.append(folder.name)
            folder = self.find_parent(folder)
        path_parts.append(self.root.name)
        return "/".join(reversed(path_parts))

    def change_directory(self, path):
        """
        Changes the current directory to the specified path.
        
        Parameters:
        -----------
        path : str
            The path to the new folder, e.g., 'folder1/folder2'.
        """
        if path == "/":
            self.current_folder = self.root
        else:
            parts = path.strip("/").split("/")
            if path.startswith("/"):
                folder = self.root
            else:
                folder = self.current_folder

            for part in parts:
                if part == "..":
                    # Go up one directory
                    if folder == self.root:
                        raise ValueError("Already at the root directory.")
                    folder = self.find_parent(folder)
                elif part in folder.contents and isinstance(folder.contents[part], Folder):
                    folder = folder.contents[part]
                else:
                    raise ValueError(f"Invalid path: '{path}' does not exist or is not a folder.")

            self.current_folder = folder

