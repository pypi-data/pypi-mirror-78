import random
import torch
from torchtext import data
from torchtext import datasets

from aiops.config import cache_dir_for_torch_text, logger
from aiops.constants import SEED


class DataSets:

    def __init__(self, tokenizer) -> None:
        super().__init__()
        self.tokenizer = tokenizer
        self.text_processor = self.tokenizer.get_text_processor()
        self.label_processor = self.tokenizer.get_label_processor()


class TorchTextInbuiltClassificationDataSets(DataSets):

    def __init__(self, tokenizer) -> None:
        super().__init__(tokenizer)

    def trec_split(self, overwrite_labels_by=dict(ABBR="urg", DESC="urg", ENTY="urg", HUM="urg", LOC="urg", NUM="urg"), **kwargs):
        train_data_trec, test_data_trec = datasets.TREC.splits(self.text_processor, self.label_processor, fine_grained=False, root=cache_dir_for_torch_text, **kwargs)
        train_data_trec, valid_data_trec = train_data_trec.split(random_state=random.seed(SEED))
        for ex in (train_data_trec + valid_data_trec + test_data_trec):
            ex.label = overwrite_labels_by.get(ex.label)
        return train_data_trec, valid_data_trec, test_data_trec

    def imdb_split(self, overwrite_labels_by=dict(pos="green", neg="amber"), **kwargs):
        train_data_imdb, test_data_imdb = datasets.IMDB.splits(self.text_processor, self.label_processor, root=cache_dir_for_torch_text, **kwargs)
        train_data_imdb, valid_data_imdb = train_data_imdb.split(random_state=random.seed(SEED))
        for ex in (train_data_imdb + test_data_imdb + valid_data_imdb):
            ex.label = overwrite_labels_by.get(ex.label)
        return train_data_imdb, test_data_imdb, valid_data_imdb


class DomainSpecificClassificationDataSet(DataSets):

    def __init__(self, tokenizer, path, format='json') -> None:
        super().__init__(tokenizer)
        loaded_tabular_dataset = data.TabularDataset(
            path=path,
            format=format,
            fields=dict(text=('text', self.text_processor), label=('label', self.label_processor))
        )

        self.dataset = data.Dataset(
            loaded_tabular_dataset.examples,
            fields=dict(text=self.text_processor, label=self.label_processor)
        )


class FiveClassesClassificationDataSet(DataSets):

    def __init__(self, tokenizer, path, format='json') -> None:
        super().__init__(tokenizer)
        self.inbuilt_dataset = TorchTextInbuiltClassificationDataSets(tokenizer)
        self.domain_dataset = DomainSpecificClassificationDataSet(tokenizer, path, format)

    def get_merged_dataset(self):
        logger.info("trec data loading.....")
        train_data_trec, valid_data_trec, test_data_trec = self.inbuilt_dataset.trec_split()
        logger.info("imdb data loading.....")
        train_data_imdb, valid_data_imdb, test_data_imdb = self.inbuilt_dataset.imdb_split()

        logger.info("merging data for training.....")
        merged_train_data_examples_list = train_data_trec.examples + train_data_imdb.examples + self.domain_dataset.dataset.examples
        merged_train_data = data.Dataset(merged_train_data_examples_list, fields=[("text", self.text_processor), ("label", self.label_processor)])

        logger.info("merging data for validation.....")
        merged_valid_data_examples_list = (valid_data_trec.examples + valid_data_imdb.examples)
        merged_valid_data = data.Dataset(merged_valid_data_examples_list, fields=[("text", self.text_processor), ("label", self.label_processor)])

        logger.info("merging data for testing.....")
        merged_test_data_examples_list = (test_data_trec.examples + test_data_imdb.examples)
        merged_test_data = data.Dataset(merged_test_data_examples_list, fields=[("text", self.text_processor), ("label", self.label_processor)])

        return merged_train_data, merged_valid_data, merged_test_data


class FOUR(DataSets):

    def __init__(self, tokenizer, path, format='json') -> None:
        super().__init__(tokenizer)
        self.inbuilt_dataset = TorchTextInbuiltClassificationDataSets(tokenizer)
        self.domain_dataset = DomainSpecificClassificationDataSet(tokenizer, path, format)

    def get_train_and_valid_datasets(self, train_ratio=0.8):
        logger.info("get_train_and_valid_datasets.......")
        logger.info("imdb data loading.....")
        train_data_imdb, valid_data_imdb, _ = self.inbuilt_dataset.imdb_split()

        total_examples = len(self.domain_dataset.dataset.examples)
        training_examples_count = int(train_ratio * total_examples)
        merged_train_data_examples_list = self.domain_dataset.dataset.examples[:training_examples_count] + train_data_imdb.examples
        merged_train_data = data.Dataset(merged_train_data_examples_list, fields=[("text", self.text_processor), ("label", self.label_processor)])

        merged_valid_data_examples_list = self.domain_dataset.dataset.examples[training_examples_count:] + valid_data_imdb.examples
        merged_valid_data = data.Dataset(merged_valid_data_examples_list, fields=[("text", self.text_processor), ("label", self.label_processor)])

        return merged_train_data, merged_valid_data

    def get_train_and_valid_domain_dataset(self, train_ratio=0.8):
        logger.info("get_train_and_valid_domain_dataset.......")
        total_examples = len(self.domain_dataset.dataset.examples)
        training_examples_count = int(train_ratio * total_examples)
        merged_train_data_examples_list = self.domain_dataset.dataset.examples[:training_examples_count]
        merged_train_data = data.Dataset(merged_train_data_examples_list, fields=[("text", self.text_processor), ("label", self.label_processor)])

        merged_valid_data_examples_list = self.domain_dataset.dataset.examples[training_examples_count:]
        merged_valid_data = data.Dataset(merged_valid_data_examples_list, fields=[("text", self.text_processor), ("label", self.label_processor)])

        return merged_train_data, merged_valid_data

    def get_train_and_valid_and_test_dataset_from_three(self, train_ratio=0.8):
        logger.info("trec data loading.....")
        train_data_trec, valid_data_trec, test_data_trec = self.inbuilt_dataset.trec_split(overwrite_labels_by=dict(ABBR="amber", DESC="amber", ENTY="amber", HUM="amber", LOC="amber", NUM="amber"))
        logger.info("imdb data loading.....")
        train_data_imdb, valid_data_imdb, test_data_imdb = self.inbuilt_dataset.imdb_split(overwrite_labels_by=dict(pos="green", neg="amber"))

        total_examples = len(self.domain_dataset.dataset.examples)
        training_examples_count = int(train_ratio * total_examples)

        logger.info("merging data for training.....")
        merged_train_data_examples_list = self.domain_dataset.dataset.examples[:training_examples_count] + train_data_trec.examples + valid_data_trec.examples
        merged_train_data = data.Dataset(merged_train_data_examples_list, fields=[("text", self.text_processor), ("label", self.label_processor)])

        logger.info("merging data for validation.....")
        merged_valid_data_examples_list = self.domain_dataset.dataset.examples[training_examples_count:] + train_data_trec.examples + valid_data_imdb.examples
        merged_valid_data = data.Dataset(merged_valid_data_examples_list, fields=[("text", self.text_processor), ("label", self.label_processor)])

        logger.info("merging data for testing.....")
        merged_test_data_examples_list = (test_data_trec.examples + test_data_imdb.examples)
        merged_test_data = data.Dataset(merged_test_data_examples_list, fields=[("text", self.text_processor), ("label", self.label_processor)])

        return merged_train_data, merged_valid_data, merged_test_data
