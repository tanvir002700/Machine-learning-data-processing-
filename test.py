from model import NaiveBais

nb = NaiveBais('cleaned_data.csv')

nb.get_predict_accuracy_on_test_data()
nb.get_predict_accuracy_on_train_data()

