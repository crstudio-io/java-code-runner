from sqlalchemy import create_engine, select, ScalarResult
from sqlalchemy.orm import sessionmaker

from models import TestCase, Problem, Solution


class TutorRepo:
    def __init__(self):
        self.session_maker = sessionmaker(
            autoflush=True,
            bind=create_engine("postgresql://tutor:password@localhost/tutor")
        )
        self.session = None

    def __call__(self):
        self.session = self.session_maker()
        return self

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        self.session = None

    def find_restrictions(self, prob_id: int) -> tuple:
        statement = select(Problem).where(Problem.id == prob_id)
        problem = self.session.scalar(statement)
        return problem.timeout, problem.memory

    def find_test_cases(self, prob_id: int) -> ScalarResult[TestCase]:
        statement = select(TestCase).where(TestCase.prob_id == prob_id)
        test_cases = self.session.scalars(statement)
        return test_cases

    def update_solution_status(self, sol_id: int, status: str):
        solution = self.session.scalar(select(Solution).where(Solution.id == sol_id))
        solution.status = status
        self.session.commit()

    def update_solution_score(self, sol_id: int, score: int):
        solution = self.session.scalar(select(Solution).where(Solution.id == sol_id))
        solution.score = score
        self.session.commit()


if __name__ == '__main__':
    tutor_repo = TutorRepo()
    with tutor_repo() as session:
        restrictions = session.find_restrictions(1)
        print(restrictions)

        for test_case in session.find_test_cases(1):
            print(test_case.input)
            print(test_case.output)

    # engine = create_engine("postgresql://tutor:password@localhost/tutor")
    # SessionMaker = sessionmaker(autoflush=True, bind=engine)
    # with SessionMaker() as s:
    #     stmt = select(TestCase).where(TestCase.id == 1)
    #     print(s.scalar(stmt).input)
    #     stmt = select(Problem).where(Problem.id == 1)
    #     for test_case in s.scalar(stmt).test_cases:
    #         print(test_case.input)
    #         print(test_case.output)
