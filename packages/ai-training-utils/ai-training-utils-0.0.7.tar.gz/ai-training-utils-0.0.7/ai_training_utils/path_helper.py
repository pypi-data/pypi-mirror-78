import argparse

from ai_training_utils.singleton import Singleton


class PathHelper(Singleton):
    output_directory = None
    dataset_directory = None
    logs_directory = None

    def get_output_directory(self) -> str:
        return self.output_directory

    def get_dataset_directory(self) -> str:
        return self.dataset_directory

    def get_logs_directory(self) -> str:
        return self.logs_directory

    def parse_arguments(self) -> None:
        parser = argparse.ArgumentParser(description='Training script')
        parser.add_argument('--dataset_directory', help='The absolute path to the dataset', required=True)
        parser.add_argument('--output_directory', help='The absolute path to the output', required=True)
        parser.add_argument('--logs_directory', help='The absolute path to the logs', required=True)
        args = parser.parse_args()

        self.dataset_directory = args.dataset_directory
        self.output_directory = args.output_directory
        self.logs_directory = args.logs_directory
