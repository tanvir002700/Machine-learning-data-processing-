import pandas as PANDA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import Imputer
from sklearn.naive_bayes import GaussianNB
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn import metrics


class BaseModel:
    def __init__(self, file_name="", train_model=None, model_name='model'):
        self.file_name = file_name
        self.model_name = model_name
        self.train_model = train_model
        self.data_frame = PANDA.read_csv(file_name)
        self.feature_column_names = self.data_frame.columns[0:-1].values
        self.predicted_class_name = [self.data_frame.columns[-1]]
        self.x = self.data_frame[self.feature_column_names].values
        self.y = self.data_frame[self.predicted_class_name].values
        split_test_size = int((len(self.data_frame.index) * 30) / 100)
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(self.x,
                                                                                self.y,
                                                                                test_size=split_test_size,
                                                                                random_state=42)
        fill_zero = Imputer(missing_values=0, strategy='mean', axis=0)
        self.x_train = fill_zero.fit_transform(self.x_train)
        self.x_test = fill_zero.fit_transform(self.x_test)
        self.train_model.fit(self.x_train, self.y_train.ravel())

        self.prediction_from_train_data = self.train_model.predict(self.x_train)
        self.prediction_from_test_data = self.train_model.predict(self.x_test)

    def show_data_frame_status(self):
        print("{0:0.2f}% in training set".format((len(self.x_train) / len(self.data_frame.index)) * 100))
        print("{0:0.2f}% in test set".format((len(self.x_test) / len(self.data_frame.index)) * 100))

        print("# rows in dataframe {0}".format(len(self.data_frame)))
        for column in self.feature_column_names:
            print("#rows missing in {0} : {1}".format(column, len(self.data_frame.loc[self.data_frame[column] == 0])))

    def get_predict_accuracy_on_test_data(self):
        accuracy = metrics.accuracy_score(self.y_test, self.prediction_from_test_data)
        return accuracy

    def get_predict_accuracy_on_train_data(self):
        accuracy = metrics.accuracy_score(self.y_train, self.prediction_from_train_data)
        return accuracy

    def get_confusion_metrics(self):
        return metrics.confusion_matrix(self.y_test, self.prediction_from_test_data, labels=[1, 0])

    def get_classification_report(self):
        return metrics.classification_report(self.y_test, self.prediction_from_test_data)


class NaiveBayesModel(BaseModel):
    def __init__(self, file_name=""):
        naive_bayes = GaussianNB()
        super().__init__(file_name=file_name, train_model=naive_bayes, model_name='Naive Bayes')


class RandomForestClassifierModel(BaseModel):
    def __init__(self, file_name=""):
        random_forest_classifier_model = RandomForestClassifier(random_state=42)
        super().__init__(file_name=file_name, train_model=random_forest_classifier_model, model_name='Random forest')


class LogisticRegressionModel(BaseModel):
    def __init__(self, file_name=""):
        logistic_regression = LogisticRegression(random_state=42)
        super().__init__(file_name=file_name, train_model=logistic_regression, model_name='Logistic Regression')

