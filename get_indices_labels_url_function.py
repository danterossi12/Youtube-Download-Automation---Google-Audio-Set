import re

# In order for this to work the appropriate files must be in the specified open path.
class Item:
    def __init__(self, address, start_time, end_time, descriptors):
        self.address = "https://www.youtube.com/watch?v=" + address
        self.start_time = start_time
        self.end_time = end_time
        self.descriptors = []
        for elem in descriptors:
            self.descriptors.append(elem.lower())
        self.name = ''

    def get_name(self):
        descriptors = ""
        count = 0
        for thing in self.descriptors:
            letters = ""
            for letter in thing:
                if letter != ' ':
                    letters += letter
            if count == 0:
                descriptors += letters
                count += 1
            else:
                descriptors += '_' + letters
        re.sub(r'\s+', '', descriptors)
        self.name = descriptors

    def clean_descriptors(self):
        for i in range(len(self.descriptors)):
            clean_item = ""
            for j in range(len(self.descriptors[i])):
                if self.descriptors[i][j] != '"':
                    clean_item += self.descriptors[i][j]
            self.descriptors[i] = clean_item
        self.descriptors[0] = self.descriptors[0].strip()

    def match_descriptors(self):
        # HERE
        template = open("class_labels_indices.csv", "r")
        template = template.read()
        template = template.split('\n')
        for i in range(len(self.descriptors)):
            for thing in template:
                splitThing = thing.split(",")
                if self.descriptors[i] == splitThing[1]:
                    self.descriptors[i] = splitThing[2].lower()

    def grab_item_with_substring(self, search_val):
        if search_val.lower() in self.descriptors:
            return True
        return False

    def add_identifier_to_name(self, num):
        self.name += str(num)


def write_url_to_file(file, array):
    for elem in array:
        file.write(elem.address + ', ' + elem.name + ', ' + elem.start_time + ', ' + elem.end_time + '\n')


#def write_indices_to_file(file, array):
    #for elem in array:
     #   file.write(elem.name + ", " + elem.start_time + ', ' + elem.end_time + '\n')


def remove_bad_videos(a):
    good_urls = []
    for elems in a:
        if elems.address != "https://www.youtube.com/watch?v=#NAME?":
            good_urls.append(elems)
    return good_urls


def main():
    # HERE
    url = open("eval_segments.csv", "r")
    urls = url.read()
    urls = urls.split('\n')
    all_items = []

    for elem in urls[3:]:
        a = elem.split(',')
        item_address = a[0]
        item_start_time = a[1]
        item_end_time = a[2]
        list_of_descriptors = []
        for descriptor in a[3:]:
            if descriptor:
                list_of_descriptors.append(descriptor)
        all_items.append(Item(item_address, item_start_time, item_end_time, list_of_descriptors))

    for items in all_items:
        items.clean_descriptors()
        items.match_descriptors()
        items.clean_descriptors()
        items.get_name()
        print(items.address, items.start_time, items.end_time, items.descriptors)

    good_items = remove_bad_videos(all_items)
    # HERE
    requested_subjects = open("requested_subjects.txt", "r")
    requested_subjects = requested_subjects.read()
    requested_subjects = requested_subjects.split('\n')
    desired_videos = []
    search = 0
    while search < len(requested_subjects):
        search_val = requested_subjects[search].strip()
        print("adding " + search_val + "...")
        for video in good_items:
            if video.grab_item_with_substring(search_val) and (video not in desired_videos):
                desired_videos.append(video)
        search += 1

    for i in range(len(desired_videos)):
        counter = 1
        for j in range(len(desired_videos)):
            if desired_videos[i].name == desired_videos[j].name and i != j:
                counter += 1
                desired_videos[j].add_identifier_to_name(counter)

# So You have two options, you can leave this block here and it will write to the files that I sent you, creating them
# in the local directory by calling FILENAME.main().

    #text = open("urls_namingScheme.txt", 'w+')
    #write_url_to_file(text, desired_videos)
    #newtext = open("descriptors_time_indices.txt", "w")
    #write_indices_to_file(newtext, desired_videos)

# Or you can just add this block of code in instead, and have it return the whole class item. To make this change,
# change the name of def main(): to def YourFunctionName():

    return desired_videos


if __name__ == "__main__":
    main()