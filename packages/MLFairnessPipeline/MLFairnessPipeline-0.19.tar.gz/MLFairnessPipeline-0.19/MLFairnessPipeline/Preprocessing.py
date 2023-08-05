from aif360.algorithms.preprocessing import Reweighing
from aif360.datasets.binary_label_dataset import BinaryLabelDataset

def generate_binary_label_dataset(df, label, protected_attribute, favorable_label, unfavorable_label):
    return BinaryLabelDataset(unfavorable_label, favorable_label, df=df, label_names=[label], protected_attribute_names=[protected_attribute])


def Preprocessing(dataset, label, unprivileged_groups, privileged_groups, protected_attribute, favorable_label, unfavorable_label):
    binary_dataset = generate_binary_label_dataset(dataset, label, protected_attribute, favorable_label, unfavorable_label)
    RW = Reweighing(unprivileged_groups=unprivileged_groups, privileged_groups=privileged_groups)
    dataset_transformed = RW.fit_transform(binary_dataset)
    return dataset_transformed.convert_to_dataframe()[0]
