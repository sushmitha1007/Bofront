from string import Template
from jira import JIRA
from jira.resources import Component
from template.jira_templates import issue_template
from config.config import jira_config as cfg
# from s3AWSHelper import aws_session


class JiraException(Exception):
    pass


class RepzyJira():
    def __init__(self):
        self.jira = JIRA(basic_auth=tuple(cfg["basic_auth"].values()), server=cfg["server"])
        # self.s3_session = aws_session()

    @staticmethod
    def __get_issue_payload(summary, description, image_link,Components):
        if image_link is not None:
            str_image_urls = " \\n ".join(image_link)
            if description is None:
                description = str_image_urls
            else:
                description = description + "\\n" + str_image_urls
            if summary is None:
                summary = cfg["summary"]
        else:
            if summary is None and description is None:
                raise JiraException(f"cannot create a jira issue with summary:{summary}, description:{description}")
            elif summary is None:
                summary = description.split(sep=".")[0]
        template = Template(str(issue_template))
        # print(template)
        data = template.substitute(project_key=cfg["project_key"], summary=summary, description=description,components=Components,
                                   issuetypename=cfg["issuetypename"])
        print(data)
        payload = eval(data)
        return payload

    def create_issue(self, summary: str = None, description: str = None, image_link: list = None, Components:str = None):
        print(summary)
        print(description)
        print(image_link)
        print("Components",Components)
        payload = self.__get_issue_payload(summary, description, image_link,Components)
        resp = self.jira.create_issue(fields=payload)
        ticket_response = {
            "key": resp.raw["key"],
            "id": resp.raw["id"],
        }
        return ticket_response

    def delete_issue(self, issue_id):
        issue = self.jira.issue(issue_id)
        issue.delete()

    def get_issue_status(self, ticket_id):
        issue = self.jira.issue(ticket_id)
        print(issue.raw["fields"]["status"]["statusCategory"]["name"])


if __name__ == "__main__":
    try:
        jira = RepzyJira()
        from pprint import pprint

        pprint(jira.create_issue(summary="not able to login as a vendor", description="my problem",
                                     Components="MRO"))
        # jira.get_issue_status(10016)
    except JiraException as e:
        print(e)
