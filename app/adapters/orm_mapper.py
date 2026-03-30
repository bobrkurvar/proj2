from app.domain import User, Task, TaskExecutors, RequestsToExecutor


class DomainToOrmMapper:
    domain_model_to_orm_fields_mapper = {
        User: ("id", "username"),
        Task: (
            "id",
            "description",
            "date_of_creation",
            "public",
            "deadline",
            "owner_id",

        ),
        TaskExecutors: ("task_id", "user_id"),
        RequestsToExecutor: ("user_id", "task_id", "owner_request")
    }

    @classmethod
    def fields(cls, domain_model):
        return cls.domain_model_to_orm_fields_mapper[domain_model]
