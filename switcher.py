from utils.creds_manager import AWSCredentialsManager


if __name__ == '__main__':

    switcher = AWSCredentialsManager()

    counter = 1
    print("WARNING!!! -- The default profile will be overwritten, so make sure you have ALL "
          "your profiles as 'named' profiles!)")
    print("Choose the profile you want to make default: \n")
    loop_size = len(switcher.list_of_profiles)
    while counter < loop_size:
        print(f"{counter} - {switcher.list_of_profiles[counter]}")
        counter += 1

    input_value = input("\nPlease enter the number of your choice: ")
    switcher.save_profile_by_index_to_disk(int(input_value))
