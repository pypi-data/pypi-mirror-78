from aif360.algorithms.postprocessing.reject_option_classification import RejectOptionClassification
from aif360.algorithms.preprocessing import Reweighing
from aif360.algorithms.inprocessing.adversarial_debiasing import AdversarialDebiasing
from aif360.datasets.binary_label_dataset import BinaryLabelDataset

import tensorflow as tf

def generate_binary_label_dataset(df, label, protected_attribute, favorable_label, unfavorable_label):
    return BinaryLabelDataset(unfavorable_label, favorable_label, df=df, label_names=[label], protected_attribute_names=[protected_attribute])

def Preprocessing(dataset, label, unprivileged_groups, privileged_groups, protected_attribute, favorable_label, unfavorable_label):
    binary_dataset = generate_binary_label_dataset(dataset, label, protected_attribute, favorable_label, unfavorable_label)
    RW = Reweighing(unprivileged_groups=unprivileged_groups, privileged_groups=privileged_groups)
    dataset_transformed = RW.fit_transform(binary_dataset)
    return dataset_transformed.convert_to_dataframe()[0]



class Fair_Model():
    def __init__(self, unprivileged_groups, privileged_groups, label, protected_attribute, favorable_label, unfavorable_label):
        self.sess = tf.Session()
        self.model = AdversarialDebiasing(privileged_groups = privileged_groups, unprivileged_groups = unprivileged_groups, scope_name='debiased_classifier', debias=True, sess=self.sess)
        self.protected_attribute = protected_attribute
        self.unprivileged_groups = unprivileged_groups
        self.privileged_groups = privileged_groups
        self.label = label
        self.favorable_label = favorable_label
        self.unfavorable_label = unfavorable_label
            
    def fit(self, training_data):
        training_binary_dataset = generate_binary_label_dataset(training_data, self.label, self.protected_attribute, self.favorable_label, self.unfavorable_label)
        self.model.fit(training_binary_dataset)
        

    def predict(self, test_data):
        test_binary_dataset = generate_binary_label_dataset(test_data, self.label, self.protected_attribute, self.favorable_label, self.unfavorable_label)
        return self.model.predict(test_binary_dataset).convert_to_dataframe()[0]

    def destroy(self):
        self.sess.close()
        tf.reset_default_graph()

def Postprocessing(reweighted_data, pred, label, unprivileged_groups, privileged_groups, protected_attribute, favorable_label, unfavorable_label, threshold=0.01):
    reweighted_binary_dataset = generate_binary_label_dataset(reweighted_data, label, protected_attribute, favorable_label, unfavorable_label)
    prediction_binary_dataset = generate_binary_label_dataset(pred, label, protected_attribute, favorable_label, unfavorable_label)
    ROC = RejectOptionClassification(unprivileged_groups=unprivileged_groups, privileged_groups=privileged_groups, low_class_thresh=threshold)
    ROC.fit(reweighted_binary_dataset, prediction_binary_dataset)

    return ROC.predict(prediction_binary_dataset).convert_to_dataframe()[0]
