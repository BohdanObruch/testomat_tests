from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class TestAttributes(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    suite_id: str | None = Field(default=None, alias="suite-id")
    title: str | None = None
    description: str | None = Field(
        default=None,
        validation_alias=AliasChoices("description", "descriprion"),
    )
    state: str | None = None
    code: str | None = None
    file: str | None = None
    sync: bool | None = None
    to_url: str | None = Field(default=None, validation_alias=AliasChoices("to_url", "to-url"))
    tags: list[str] | None = None
    has_examples: bool | None = Field(default=None, alias="has-examples")
    params: list[str] | None = None
    run_statuses: list[str] | None = Field(default=None, alias="run-statuses")
    attachments: list[str] | None = None
    jira_issues: list[str] | None = Field(default=None, alias="jira-issues")
    assigned_to: str | None = Field(default=None, alias="assigned-to")
    created_by: str | int | None = Field(default=None, alias="created-by")
    created_at: str | None = Field(default=None, alias="created-at")
    updated_at: str | None = Field(default=None, alias="updated-at")
    comments_count: int | None = Field(default=None, validation_alias=AliasChoices("comments_count", "comments-count"))


class CaseModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")

    id: str | None = None
    type: str | None = None
    attributes: TestAttributes | None = None

    @property
    def title(self) -> str | None:
        if not self.attributes:
            return None
        return self.attributes.title

    @property
    def suite_id(self) -> str | None:
        if not self.attributes:
            return None
        return self.attributes.suite_id

    def get_url(self, project_id: str) -> str:
        """Get the URL path for this test case."""
        return f"/projects/{project_id}/tests/{self.id}"


class TestResponse(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    data: CaseModel
