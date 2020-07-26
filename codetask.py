import argparse
import csv
from collections import defaultdict
from typing import Dict, List, Tuple


def read_csv(input_file_path: str) -> Tuple[List[Dict], List[str]]:
    row_list = []
    with open(input_file_path, 'r', newline="") as bf:
        csvf = csv.DictReader(bf, delimiter=',', quotechar='"')
        field_names = csvf.fieldnames
        for row in csvf:
            row_list.append(row)
        return row_list, field_names


def mapping_file(row_list: List[Dict]) -> Tuple[Dict, Dict]:
    low_strip = striping_lowering_review
    aspect_review_dict = defaultdict(set)
    review_aspect_dict = defaultdict(set)
    for row in row_list:
        aspect = low_strip(row["Aspect"])
        review = low_strip(row["Review"])
        aspect_review_dict[aspect].add(review)
        review_aspect_dict[review].add(aspect)
    return aspect_review_dict, review_aspect_dict


def get_organize_data(aspect_review_dict: Dict, review_aspect_dict: Dict) -> List[Dict]:
    final_list = list()
    for aspect1, reviews1 in aspect_review_dict.items():
        second_aspect_dict = second_aspect_set(review_aspect_dict, reviews1)
        aspect1_count = len(reviews1)
        for aspects2, reviews2 in second_aspect_dict.items():
            if aspect1 != aspects2:
                temp_dict = {"aspect1": aspect1, "count1": aspect1_count, "aspects2": aspects2, "count2": len(reviews2)}
                final_list.append(temp_dict)
    return final_list


def second_aspect_set(review_aspect_dict: Dict, reviews: List[str]) -> Dict:
    second_aspect_dict = defaultdict(set)
    for review in reviews:
        aspects_set = review_aspect_dict[review]
        for aspect in aspects_set:
            second_aspect_dict[aspect].add(review)
    return second_aspect_dict


def striping_lowering_review(text: str) -> str:
    processed_text = text.strip().lower()
    return processed_text


def write_csv(output_file_path: str, final_dataset: List[Dict], field_names:List[str]):
    with open(output_file_path, 'w') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=field_names, delimiter=',', quotechar='"')
        writer.writeheader()
        for row in final_dataset:
            writer.writerow(row)


def main(input_file_path: str, output_file_path: str):
    row_list, header = read_csv(input_file_path)
    aspect_review, review_aspect = mapping_file(row_list)
    final_list = get_organize_data(aspect_review, review_aspect)
    header = final_list[0].keys()
    write_csv(output_file_path, final_list, header)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_file_path", help="input folder path")
    parser.add_argument("--output_file_path", help="output_file_path")
    args = parser.parse_args()
    main(args.input_file_path, args.output_file_path)
