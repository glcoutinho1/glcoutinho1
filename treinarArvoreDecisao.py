#treinarArvoreDecisao.py

from yellowbrick.classifier import ConfusionMatrix, ClassificationReport, DiscriminationThreshold
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import GridSearchCV

def treinarArvore(X_train, y_train, X_test, y_test, cn, nome):
    clf = DecisionTreeClassifier(random_state=0, class_weight='balanced')
    
    #parametros do GridSearch
    params = {'criterion' : ['gini', 'entropy'],
              'max_depth' : [10, 20, 30, 40],
              'min_samples_split' : list(range(2, 10))}
    
    grid_clf = GridSearchCV(clf, params, n_jobs=-1, cv=10)
    
    y_pred = grid_clf.fit(X_train, y_train).predict(X_test)
    
    visualizer = ConfusionMatrix(estimator=grid_clf.best_estimator_, classes=cn)
    visualizer.score(X_test, y_test)
    visualizer.finalize()
    visualizer.set_title('Matriz de Confusão Dataset: ' + nome)
    visualizer.ax.set_ylabel("Real")
    visualizer.ax.set_xlabel("Previsto")
    plt.show()
    
    visualizer = ClassificationReport(estimator=grid_clf.best_estimator_, classes=cn, support=True)
    visualizer.fit(X_train, y_train)      
    visualizer.score(X_test, y_test)      
    visualizer.finalize()
    visualizer.set_title('Relatório de Classificação Dataset: ' + nome)
    plt.show()

    visualizer = DiscriminationThreshold(estimator=grid_clf.best_estimator_, classes=cn, fbeta=1, random_state=0)
    visualizer.fit(X_train, y_train)
    visualizer.finalize()
    visualizer.set_title('Limiar de Discriminação Dataset: ' + nome)
    plt.show()
    
    print("Melhores parâmetros: ", grid_clf.best_params_)
    print("Acurácia (base de treinamento):", grid_clf.score(X_train, y_train))
    print("Acurácia (base de teste)      :", accuracy_score(y_test, y_pred))
    print("Profundidade                  :", grid_clf.best_estimator_.get_depth())
    print("\n-----------------------------------------Fim")
    
    return y_pred, grid_clf.best_estimator_