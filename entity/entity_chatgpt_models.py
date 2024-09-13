from pydantic import BaseModel


class Models(BaseModel):
    class Data(BaseModel):
        class Permission(BaseModel):
            id: str
            object: str
            created: int
            allow_create_engine: bool
            allow_sampling: bool
            allow_logprobs: bool
            allow_search_indices: bool
            allow_view: bool
            allow_fine_tuning: bool
            organization: str
            group: str | None
            is_blocking: bool

        id: str
        object: str
        created: int
        owned_by: str
        permission: list[Permission]
        root: str
        parent: str | None

    data: list[Data]
    object: str
