from src.models.address import AddressModel
from src.repositories.base_implementation import BaseRepositoryImplementation
from src.schemas.address import (
    CreateAddressSchema,
    ResponseAddressSchema,
)


class AddressRepository(BaseRepositoryImplementation):
    def __init__(self):
        super().__init__(
            model=AddressModel,
            create_schema=CreateAddressSchema,
            response_schema=ResponseAddressSchema,
        )

    def count_all_user_addresses(self, user_id: int) -> int:
        """Count all addresses for a user"""
        with self.session_scope() as session:
            return (
                session.query(self.model).filter(self.model.user_id == user_id).count()
            )

    def get_user_addresses(
        self, user_id: int, offset: int = 0, limit: int = 10
    ) -> list[ResponseAddressSchema]:
        """Get all addresses for a user"""
        with self.session_scope() as session:
            addresses = (
                session.query(self.model)
                .filter(self.model.user_id == user_id)
                .offset(offset)
                .limit(limit)
                .all()
            )
            return [self.schema.model_validate(address) for address in addresses]
