class ComplexityAnalyser:

    def __init__(self):
        self.timeComplexityFactor = 0

    def calculate_time_complexity(self, ast):
        self.timeComplexityFactor = 0
        self._analyze(ast, 0)
        return self.timeComplexityFactor

    def _analyze(self, ast, currentNesting):
        for statement in ast:
            if (statement["type"] == "LOOP"):
                currentNesting += 1
                self.timeComplexityFactor += currentNesting

                if ("body" in statement and isinstance(statement["body"], list)):
                    self._analyze(statement["body"], currentNesting)

                currentNesting -= 1