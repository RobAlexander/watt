from common import nan

class Page:
    def __init__(self, page_name):
        self._page_name = page_name
        self._evaluations = {}

    def __repr__(self):
        return self.page_name() + " with evaluations " + \
            ", ".join(str(evaluation) for _, evaluation in self.evaluations().items())

    def page_name(self):
        return self._page_name

    def original_name(self):
        return self._page_name.split(".")[0] + "." + self._page_name.split(".")[-1]

    def applied_mutations(self):
        parts = self._page_name.split(".")
        mutations = []
        for i in range(1, len(parts) - 1, 2):
            mutations.append(parts[i])
        return mutations

    def mutant_order(self):
        return len(self.applied_mutations())

    def evaluations(self):
        return self._evaluations

    def add_evaluation(self, evaluation):
        self._evaluations[evaluation.tool()] = evaluation

class Evaluation:
    def __init__(self, tool, failure=nan, inconclusive=nan, success=nan, skipped=nan, ran=nan):
        self._tool = tool
        self._failure = failure
        self._inconclusive = inconclusive
        self._success = success
        self._skipped = skipped
        self._ran = ran

    def __repr__(self):
        return self.tool() + " with pass rate of " + str(self.success()/self.ran())

    def tool(self):
        return self._tool

    def failure(self):
        if self._failure is nan:
            return self.ran() - self.skipped() - self.success() - self.inconclusive()
        return self._failure

    def inconclusive(self):
        if self._inconclusive is nan:
            return self.ran() - self.skipped() - self.success() - self.failure()
        return self._inconclusive

    def success(self):
        if self._success is nan:
            return self.ran() - self.skipped() - self.failure() - self.inconclusive()
        return self._success

    def skipped(self):
        if self._skipped is nan:
            return self.ran() - self.failure() - self.success() - self.inconclusive()
        return self._skipped

    def ran(self):
        if self._ran is nan:
            return self.skipped() + self.success() + self.inconclusive() + self.failure()
        return self._ran
