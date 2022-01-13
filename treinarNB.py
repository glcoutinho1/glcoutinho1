#treinarNB.py

from yellowbrick.classifier import ConfusionMatrix, ClassificationReport, DiscriminationThreshold
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import GridSearchCV

def treinarGNB(X_train, y_train, X_test, y_test, cn, nome):
    clf = GaussianNB()
    params = {'var_smoothing' : [1e-9, 1e-5, 1e-14]}    
    grid_clf = GridSearchCV(clf, params, n_jobs=-1, cv=10)
    
    y_pred = grid_clf.fit(X_train, y_train).predict(X_test)
    
    visualizer = ConfusionMatrix(grid_clf.best_estimator_, classes=cn)
    visualizer.score(X_test, y_test)
    visualizer.finalize()
    visualizer.set_title('Matriz de Confusão Dataset: ' + nome)
    visualizer.ax.set_ylabel("Real")
    visualizer.ax.set_xlabel("Previsto")
    plt.show()
    
    visualizer = ClassificationReport(grid_clf.best_estimator_, classes=cn, support=True)
    visualizer.fit(X_train, y_train)      
    visualizer.score(X_test, y_test)      
    visualizer.finalize()
    visualizer.set_title('Relatório de Classificação Dataset: ' + nome)
    plt.show()

    visualizer = DiscriminationThreshold(estimator=grid_clf.best_estimator_, classes=cn)
    visualizer.fit(X_train, y_train)
    visualizer.finalize()
    visualizer.set_title('Limiar de Discriminação Dataset: ' + nome)
    plt.show()
    
    print("Melhores parâmetros: ", grid_clf.best_params_)
    print("Acurácia (base de treinamento):", grid_clf.best_estimator_.score(X_train, y_train))
    print("Acurácia (base de teste)      :", accuracy_score(y_test, y_pred))
    print("\n-----------------------------------------Fim")
    
    return y_pred