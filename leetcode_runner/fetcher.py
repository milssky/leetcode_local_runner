from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport

from .dto import Problem, Tests, TestQuestion, Question

def get_client(credentials: dict[str, str]) -> Client: 
    transport = RequestsHTTPTransport(
        url='https://leetcode.com/graphql/',
        headers={**credentials},
        retries=3,
    )
    return Client(transport=transport)


def fetch_problem(client: Client, problem_slug: str) -> Problem:
    query = gql(
        '''
        query getQuestionDetail($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                title
                difficulty
                likes
                dislikes
                isLiked
                isPaidOnly
                stats
                status
                content
                topicTags {
                    name
                }
                codeSnippets {
                    lang
                    langSlug
                    code
                }
                sampleTestCase
            }
        }
        '''
    )
    result = client.execute(query, variable_values={'titleSlug': problem_slug})
    return Problem(**result)


def fetch_problem_test_cases(client: Client, problem_slug: str) -> Tests:
    query = gql(
        '''
        query consolePanelConfig($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                exampleTestcaseList
            }
        }
        '''
    )
    result = client.execute(query, variable_values={'titleSlug': problem_slug})
    return Tests(**result)


def fetch_problem_data(client, problem_slug) -> tuple[Question, list[TestQuestion]]:
    problem = fetch_problem(client, problem_slug)
    test_cases = fetch_problem_test_cases(client, problem_slug)
    return problem.question, test_cases.question.test_cases