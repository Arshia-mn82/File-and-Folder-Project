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

    def find_parent(self, folder):
        """
        Finds the parent folder of the given folder.

        Parameters:
        -----------
        folder : Folder
            The folder whose parent is to be found.

        Returns:
        --------
        Folder
            The parent folder.
        """
        for item in self.root.contents.values():
            if isinstance(item, Folder) and folder in item.contents.values():
                return item
        return self.root  # Return root if no parent found (or handle appropriately)

    def list_directory(self):
        """Lists the contents of the current folder."""
        return self.current_folder.list_contents()

    def create_folder(self, path=None, name=None):
        """
        Creates a new folder at the specified path or in the current directory if no path is provided.

        Parameters:
        -----------
        path : str, optional
            The path where the folder should be created. If not provided, the folder will be created in the current directory.
        name : str
            The name of the new folder.
        """
        if name is None:
            # If only path is provided, treat it as the folder name in the current directory
            name = path
            folder = self.current_folder
        else:
            if path is None:
                # If only name is provided, create the folder in the current directory
                folder = self.current_folder
            else:
                # If both path and name are provided, navigate to the specified path
                folder = self.root if path.startswith("/") else self.current_folder
                path_parts = path.strip("/").split("/")
                for part in path_parts:
                    folder = folder.get(part)
                    if not isinstance(folder, Folder):
                        raise ValueError(f"Invalid path: '{path}' does not exist or is not a folder.")

        if name in folder.contents:
            raise ValueError(f"A file or folder with the name '{name}' already exists.")

        new_folder = Folder(name)
        folder.add(new_folder)

    def create_file(self, path, content=""):
        """
        Creates a new file at the specified path.
        If only a filename is provided, it will create the file in the current directory.

        Parameters:
        -----------
        path : str
            The path where the file should be created, or the filename if no path is provided.
        content : str, optional
            The initial content of the file. Default is an empty string.
        """
        path_parts = path.strip("/").split("/")
        filename = path_parts.pop()

        folder = self.current_folder
        if path_parts:
            folder = self.root if path.startswith("/") else self.current_folder
            for part in path_parts:
                folder = folder.get(part)
                if not isinstance(folder, Folder):
                    raise ValueError(f"Folder '{part}' does not exist.")

        if filename in folder.contents:
            raise ValueError(f"File '{filename}' already exists.")
        folder.contents[filename] = File(filename, content)

    def read_file(self, path):
        """
        Reads the contents of the specified file.

        Parameters:
        -----------
        path : str
            The path to the file.
        """
        path_parts = path.strip("/").split("/")
        filename = path_parts.pop()
        folder = self.root if path.startswith("/") else self.current_folder

        for part in path_parts:
            folder = folder.get(part)
            if not isinstance(folder, Folder):
                raise ValueError("Invalid path")

        file = folder.get(filename)
        if isinstance(file, File):
            return file.read()
        else:
            raise ValueError("Specified path is not a file")

    def move(self, source_path, destination_path):
        """
        Moves a file or folder from one location to another.

        Parameters:
        -----------
        source_path : str
            The path of the file or folder to move.
        destination_path : str
            The path where the file or folder should be moved to.
        """
        # Handle absolute paths
        if source_path.startswith("/"):
            src_parts = source_path.strip("/").split("/")
            src_name = src_parts.pop()
            src_folder = self.root
        else:
            src_parts = source_path.strip("/").split("/")
            src_name = src_parts.pop()
            src_folder = self.current_folder

        for part in src_parts:
            src_folder = src_folder.get(part)
            if not isinstance(src_folder, Folder):
                raise ValueError("Invalid source path")

        item = src_folder.get(src_name)

        # Handle absolute paths
        if destination_path.startswith("/"):
            dest_parts = destination_path.strip("/").split("/")
            dest_name = dest_parts.pop()
            dest_folder = self.root
        else:
            dest_parts = destination_path.strip("/").split("/")
            dest_name = dest_parts.pop()
            dest_folder = self.current_folder

        for part in dest_parts:
            dest_folder = dest_folder.get(part)
            if not isinstance(dest_folder, Folder):
                raise ValueError("Invalid destination path")

        src_folder.remove(src_name)
        item.name = dest_name
        dest_folder.add(item)

    def copy(self, source_path, destination_path):
        """
        Copies a file or folder from one location to another.

        Parameters:
        -----------
        source_path : str
            The path of the file or folder to copy.
        destination_path : str
            The path where the file or folder should be copied to.
        """
        # Handle absolute paths
        if source_path.startswith("/"):
            src_parts = source_path.strip("/").split("/")
            src_name = src_parts.pop()
            src_folder = self.root
        else:
            src_parts = source_path.strip("/").split("/")
            src_name = src_parts.pop()
            src_folder = self.current_folder

        for part in src_parts:
            src_folder = src_folder.get(part)
            if not isinstance(src_folder, Folder):
                raise ValueError("Invalid source path")

        item = src_folder.get(src_name)

        # Handle absolute paths
        if destination_path.startswith("/"):
            dest_parts = destination_path.strip("/").split("/")
            dest_name = dest_parts.pop()
            dest_folder = self.root
        else:
            dest_parts = destination_path.strip("/").split("/")
            dest_name = dest_parts.pop()
            dest_folder = self.current_folder

        for part in dest_parts:
            dest_folder = dest_folder.get(part)
            if not isinstance(dest_folder, Folder):
                raise ValueError("Invalid destination path")

        if isinstance(item, File):
            new_item = File(dest_name, item.read())
        else:
            new_item = Folder(dest_name)
            new_item.contents = item.contents.copy()

        dest_folder.add(new_item)

    def delete(self, path):
        """
        Deletes a file or folder at the specified path.

        Parameters:
        -----------
        path : str
            The path of the file or folder to delete.
        """
        path_parts = path.strip("/").split("/")
        name = path_parts.pop()
        folder = self.root if path.startswith("/") else self.current_folder

        for part in path_parts:
            folder = folder.get(part)
            if not isinstance(folder, Folder):
                raise ValueError("Invalid path")

        folder.remove(name)

    def rename(self, path, new_name):
        """
        Renames a file or folder at the specified path.

        Parameters:
        -----------
        path : str
            The path of the file or folder to rename.
        new_name : str
            The new name for the file or folder.
        """
        path_parts = path.strip("/").split("/")
        name = path_parts.pop()
        folder = self.root if path.startswith("/") else self.current_folder

        for part in path_parts:
            folder = folder.get(part)
            if not isinstance(folder, Folder):
                raise ValueError("Invalid path")

        item = folder.get(name)
        folder.remove(name)
        item.name = new_name
        folder.add(item)

    def search(self, name, folder=None):
        """
        Searches for files or folders with a specific name in the current folder or a specified folder.

        Parameters:
        -----------
        name : str
            The name to search for.
        folder : Folder, optional
            The folder to search in. Default is the current folder.
        """
        if folder is None:
            folder = self.current_folder

        results = []

        for item_name, item in folder.contents.items():
            if item_name == name:
                results.append(f"{self.get_full_path()}/{item_name}")
            if isinstance(item, Folder):
                results.extend(self.search(name, item))

        return results

    def search_by_extension(self, extension, folder=None):
        """
        Searches for files with a specific extension in the current folder or a specified folder.

        Parameters:
        -----------
        extension : str
            The file extension to search for, e.g., 'py'.
        folder : Folder, optional
            The folder to search in. Default is the current folder.
        """
        if folder is None:
            folder = self.current_folder

        results = []

        for item_name, item in folder.contents.items():
            if isinstance(item, File) and item_name.endswith(extension):
                results.append(f"{self.get_full_path()}/{item_name}")
            if isinstance(item, Folder):
                results.extend(self.search_by_extension(extension, item))

        return results
