from pathlib import Path


class AWSCredentialsManager():
    """
        Class that assists with switching between credentials.
    """

    def __init__(self, path_to_directory_with_credentials: Path = Path().home() / ".aws"):
        # Try to load the credentials from disk.
        # THIS METHOD DOES NOT ERROR CHECK. It expects the file to be well-formed!!
        # It also expects there to be a 'config' file and a 'credentials' file
        # in the directory.
        self.path_to_credentials = path_to_directory_with_credentials / "credentials"
        self.path_to_config = path_to_directory_with_credentials / "config"
        self.dict_of_configs = {}
        self.dict_of_credentials = {}
        self.__load_profiles_from_disk()

    def save_profile_by_index_to_disk(self, index_of_profile):
        if index_of_profile == 0 or index_of_profile >= len(self.list_of_profiles):
            print("CANNOT PROCEED! Invalid index provided.")
            exit(0)
        else:
            self.__change_default_profile_on_disk(self.path_to_config, self.dict_of_configs, index_of_profile)
            self.__change_default_profile_on_disk(self.path_to_credentials, self.dict_of_credentials, index_of_profile)

    def __load_profiles_from_disk(self):
        # load the lines for each profile's credential into a dict
        self.dict_of_credentials = self.__load_profile_lines_from_a_file_to_dict(self.path_to_credentials)
        # load the lines for each profile's config into a dict
        self.dict_of_configs = self.__load_profile_lines_from_a_file_to_dict(self.path_to_config)
        self.list_of_profiles = list(self.dict_of_configs.keys())
        # Ensure that the credentials and config files match in terms of profiles
        if set(self.dict_of_configs.keys()) != set(self.dict_of_credentials.keys()):
            print("CANNOT PROCEED! The config and credentials files don't have the same profiles configured.")
            exit(0)

    def __change_default_profile_on_disk(self,
                                         path_to_file: Path,
                                         dict_with_profiles,
                                         index_of_profile_to_make_default):
        list_of_lines = []
        list_of_lines_copy = []

        with open(path_to_file, mode='r') as f:
            list_of_lines = f.readlines()

        line_counter = 0
        loop_size = len(list_of_lines)
        done_setting_the_default = False

        # first we do a loop to copy like-for-like any blank lines or comments
        while line_counter < loop_size:
            line = list_of_lines[line_counter].strip()
            if line == "" or line.startswith('#'):
                list_of_lines_copy.append(list_of_lines[line_counter])
                line_counter += 1
            elif line.startswith('['):
                break
            else:
                print("CANNOT PROCEED! Found an unexpected character in one of the files.")
                exit(0)
        # If we've reached here, the current line index is the first line starting with
        # '[' which we expect to be the default profile
        line = list_of_lines[line_counter].strip()
        if line == "[default]":
            # append the literal '[default]' line
            list_of_lines_copy.append(list_of_lines[line_counter])
            # update the dictionary with the new default
            new_default = dict_with_profiles[self.list_of_profiles[index_of_profile_to_make_default]]
            dict_with_profiles["[default]"] = new_default
            # add the lines from the new default to the copy being created that will be written to disk
            list_of_lines_copy.extend(new_default)
        else:
            print("CANNOT PROCEED! Did not find the [default] profile to be the first entry.")
            exit(0)
        # Now in, the original list we need to move the line cursor forward until we find the first
        # line that is the next profile.
        # This means that comments and blank lines are not supported in the [default] section.
        while line_counter < loop_size:
            line_counter += 1
            line = list_of_lines[line_counter].strip()
            if line.startswith('['):
                break
        # Now we should be able to copy the rest of the file as-is
        while line_counter < loop_size:
            list_of_lines_copy.append(list_of_lines[line_counter])
            line_counter += 1

        with open(path_to_file, mode='w') as f:
            f.writelines(list_of_lines_copy)

    @staticmethod
    def __load_profile_lines_from_a_file_to_dict(path_to_file: Path) -> dict:
        dict_to_return = {}
        # load the lines for each profile into a dict
        with open(path_to_file, mode='r') as f:
            list_of_lines = f.readlines()
            current_profile = ""
            while len(list_of_lines) > 0:
                line = list_of_lines.pop(0).strip()
                if line == "" or line.startswith('#'):
                    # ignore blank lines and comments
                    continue
                elif line.startswith('['):
                    # found a line which specifies a named profile
                    current_profile = line.strip("[]").strip()
                    # in the 'config' file, each profile other than 'default' starts with
                    # the word 'profile', so we need to get rid of that.
                    if current_profile.startswith("profile "):
                        current_profile = current_profile.replace("profile ", "")
                    # start an entry in the dictionary of credentials. Each entry
                    # will be 'remember' a list of relevant lines for that profile,
                    # so the list is started here.
                    dict_to_return[current_profile] = []
                    continue
                else:
                    # below we append the line to the current profile being tracked
                    # the inline if/else checks if the line has been stripped of its end-of-line
                    # carriage return, and if it has, it re-adds it
                    dict_to_return[current_profile].append(f"{line}\n" if (not line.endswith("\n")) else line)
                    continue
        return dict_to_return
