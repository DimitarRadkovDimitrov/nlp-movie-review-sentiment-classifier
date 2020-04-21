import nltk
import sys
from os import listdir, mkdir
from os.path import join, isdir

def prepare_data_for_feature_one(review_root_folder, output_root_folder):
    # adjectives, nouns, adverbs, verbs
    accepted_tags = {"JJ", "JJR", "JJS", "NN", "NNS", "NNP", "NNPS", "RB", "RBR", "RBS", "VB", "VBD", "VBG", "VBN", "VBP", "VBZ"}
    pos_tag_dataset(review_root_folder, output_root_folder, accepted_tags)

def prepare_data_for_feature_two(review_root_folder, output_root_folder):
    # adjectives and adverbs
    accepted_tags = {"JJ", "JJR", "JJS", "RB", "RBR", "RBS"}
    pos_tag_dataset(review_root_folder, output_root_folder, accepted_tags)

def pos_tag_dataset(review_root_folder, output_root_folder, accepted_tags):
    try:
        mkdir(output_root_folder)
        nltk.download('averaged_perceptron_tagger')

        for item in listdir(review_root_folder):
            item_full_path = join(review_root_folder, item)
            if isdir(item_full_path):
                try:
                    new_directory = join(output_root_folder, item)
                    if not isdir(new_directory):
                        mkdir(new_directory)
                    
                    for file in listdir(item_full_path):
                        new_file_path = join(new_directory, file)
                        with open(join(item_full_path, file), "r") as current_file:
                            file_text = current_file.read()
                            tagged_file_text = nltk.pos_tag(file_text.split())
                            print_tagged_tuples_to_file(tagged_file_text, new_file_path, accepted_tags)

                except OSError:
                    print("Feature sub directory creation failed")
    except OSError:
        print("Feature directory already created")

def print_tagged_tuples_to_file(tagged_token_tuples, output_file_path, accepted_tags):
    with open(output_file_path, "w+") as output_file:
        for key, value in tagged_token_tuples:
            if value in accepted_tags:
                output_file.write(key + " ")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: pipenv run python " + sys.argv[0] + " <review_root_folder>")
        exit()
    
    input_folder_container = sys.argv[1]
    output_folder_container_f1 = input_folder_container.rstrip("/") + "_feature_1"
    output_folder_container_f2 = input_folder_container.rstrip("/") + "_feature_2"

    prepare_data_for_feature_one(input_folder_container, output_folder_container_f1)
    prepare_data_for_feature_two(input_folder_container, output_folder_container_f2)