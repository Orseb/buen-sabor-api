from typing import List, Optional

from src.models.business_hours import BusinessHoursModel, DayOfWeek
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.business_hours import (
    CreateBusinessHoursSchema,
    ResponseBusinessHoursSchema,
)


class BusinessHoursRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(
            model=BusinessHoursModel,
            create_schema=CreateBusinessHoursSchema,
            response_schema=ResponseBusinessHoursSchema,
        )

    def find_by_day(self, day: DayOfWeek) -> Optional[ResponseBusinessHoursSchema]:
        with self.session_scope() as session:
            model = (
                session.query(self.model)
                .filter(self.model.day == day, self.model.is_active)
                .first()
            )
            if model is None:
                return None
            return self.schema.model_validate(model)

    def find_all_active(self) -> List[ResponseBusinessHoursSchema]:
        with self.session_scope() as session:
            models = session.query(self.model).filter(self.model.is_active).all()
            schemas = []
            for model in models:
                schemas.append(self.schema.model_validate(model))
            return schemas
