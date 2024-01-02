import os
import argparse
from tqdm import tqdm
from xml.etree import ElementTree as ET

def rename_files(dataset_dir, start_index):
    annotations_dir = os.path.join(dataset_dir, 'Annotations')
    images_dir = os.path.join(dataset_dir, 'JPEGImages')

    jpg_files = sorted(os.listdir(images_dir))
    for i, jpg_file in enumerate(tqdm(jpg_files, desc="Renaming files"), start=start_index):
        xml_file = os.path.splitext(jpg_file)[0] + '.xml'
        xml_path = os.path.join(annotations_dir, xml_file)
        if not os.path.exists(xml_path):
            print(f'No corresponding XML file found for JPG file: {jpg_file}')
            continue
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            filename_tag = root.find('filename')
            new_filename = f'Image_{start_index + i}.jpg'
            filename_tag.text = new_filename
            new_xml_path = os.path.join(annotations_dir, f'Image_{start_index + i}.xml')
            tree.write(new_xml_path)
            if not os.path.exists(new_xml_path):
                print(f'Failed to rename XML file: {xml_file}')
                continue
            os.remove(xml_path)
            os.rename(os.path.join(images_dir, jpg_file), os.path.join(images_dir, new_filename))
        except Exception as e:
            print(f'Error occurred while processing file {jpg_file}: {str(e)}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Rename files in a dataset.')
    parser.add_argument('--dataset', type=str, help='The directory of the dataset.')
    parser.add_argument('--index', type=int, help='The start index for renaming.')
    args = parser.parse_args()
    rename_files(args.dataset, args.index)
