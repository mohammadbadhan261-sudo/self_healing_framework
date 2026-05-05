import numpy as np
from sklearn.ensemble import RandomForestClassifier


class ElementMatcher:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=50,
            random_state=42
        )
        self._train_model()

    # ---------------------------------------
    # TRAINING DATA (SIMULATED UI PATTERNS)
    # ---------------------------------------
    def _train_model(self):

        # Features format:
        # [is_input, is_button, has_text]
        X = np.array([
            [1, 0, 1],  # input field (good)
            [1, 0, 1],  # input field
            [0, 1, 1],  # button
            [0, 1, 1],  # button
            [1, 0, 0],  # empty input (weak match)
            [0, 0, 1],  # text only (weak match)
            [1, 0, 1],  # login input
            [0, 1, 1],  # login button
        ])

        # Labels:
        # 1 = valid match, 0 = invalid match
        y = np.array([1, 1, 1, 1, 0, 0, 1, 1])

        self.model.fit(X, y)

    # ---------------------------------------
    # PREDICTION FUNCTION
    # ---------------------------------------
    def predict(self, features):

        # Ensure correct shape
        features = np.array(features).reshape(1, -1)

        prediction = self.model.predict(features)[0]

        return prediction

    # ---------------------------------------
    # OPTIONAL: PROBABILITY SCORE (FOR FUTURE EXPANSION)
    # ---------------------------------------
    def predict_proba_score(self, features):

        features = np.array(features).reshape(1, -1)

        if hasattr(self.model, "predict_proba"):
            return self.model.predict_proba(features)[0][1]

        return 0.5