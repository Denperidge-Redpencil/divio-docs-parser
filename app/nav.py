from os import environ

created_files = []

class NavItem():
    def __init__(self, filename: str, ) -> None:
        self.filepath, self.filename = filename.rsplit("/", maxsplit=1)
        print("fp: " + self.filepath)
        print("fn: " + self.filename)
    
    def link_to_self_from(self, from_filepath_plus_filename: str):
        # Example: []
        from_filepath_split = from_filepath_plus_filename.split("/")
        to_filepath_split = self.filepath.split("/")
        from_filename = from_filepath_split.pop()
        to_filename = self.filename

        print(f"Linking to {to_filepath_split} from {from_filepath_plus_filename}")


        link = to_filename

     

        # to -1, because range works exclusive
        for i in reversed(range(0, len(from_filepath_split))):
            from_path_part = from_filepath_split[i]
            to_path_part = to_filepath_split[i]

            print("Current link: " + link)

            print(f"{from_path_part} == {to_path_part}")

            if from_path_part == to_path_part:
                break
            else:
                link = f"../{to_path_part}/{link}"
        
        return link



    def markdown_link_to_self_from(self, filepath: str):
        link = self.link_to_self_from(filepath)
        name = link.replace("../", "")

        return f"- [{name}]({link})\n"


